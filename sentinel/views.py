import os
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect, JsonResponse
from .nasa import fetch_neos
from django.views.decorators.csrf import csrf_exempt
from .gemini import summarize_asteroid, generate_fun_descriptions, chat_with_quackstronaut, generate_daily_briefing
from .models import FavoriteNEO


# AUTH0 related stuff --------
oauth = OAuth()
oauth.register(
    name='auth0',
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

def login(request):
    return oauth.auth0.authorize_redirect(request, os.getenv("AUTH0_CALLBACK_URL"))

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    user_info = oauth.auth0.get(f'https://{os.getenv("AUTH0_DOMAIN")}/userinfo', token=token).json()

    print("User info:", user_info)

    request.session['user'] = user_info
    return redirect('/')

def logout(request):
    request.session.flush()
    django_logout(request)
    return HttpResponseRedirect(
        f'https://{os.getenv("AUTH0_DOMAIN")}/v2/logout?'
        f'returnTo={os.getenv("AUTH0_LOGOUT_URL")}&'
        f'client_id={os.getenv("AUTH0_CLIENT_ID")}'
    )

# AUTH related stuff ends --------

# Before and After login home page loads on root
def home(request):
    user = request.session.get('user')
    
    # Generate daily briefing for authenticated users
    daily_briefing = None
    if user:
        try:
            # Get today's NEOs for the briefing
            from datetime import date
            today_str = date.today().strftime('%Y-%m-%d')
            current_neos = fetch_neos(today_str, today_str)
            
            # Generate personalized daily briefing
            daily_briefing = generate_daily_briefing(user.get('name', 'Explorer'), current_neos)
        except Exception as e:
            # Fallback briefing if API fails
            daily_briefing = f"🦆 Quack quack, {user.get('name', 'Explorer')}! Welcome back to the CosmoDex space lab! Even when the cosmic data streams are a bit wobbly, there's always something amazing happening in our solar system. Today's a perfect day to explore our asteroid database and maybe discover your new favorite space rock! Ready to dive into some cosmic adventures? 🚀✨"
    
    return render(request, 'sentinel/home.html', context={
        'user': user,
        'daily_briefing': daily_briefing
    })

# neos listing page
def index(request):
    user = request.session.get('user')
    if not user:
        return redirect("/")
    
    # Get date range from request parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    neos = fetch_neos(start_date, end_date)
    
    # Get user's favorited NEOs
    user_favorites = set()
    if user:
        favorites = FavoriteNEO.objects.filter(user_email=user["email"]).values_list('name', flat=True)
        user_favorites = set(favorites)
    
    # Pass current date range to template for form defaults
    from datetime import date, timedelta
    current_start = start_date if start_date else date.today().isoformat()
    current_end = end_date if end_date else (date.today() + timedelta(days=1)).isoformat()
    
    return render(request, 'sentinel/index.html', context={
        'user': user, 
        'neos': neos,
        'user_favorites': user_favorites,
        'current_start_date': current_start,
        'current_end_date': current_end
    })

# favorite neos list
def favorites(request):
    user = request.session.get("user")
    if not user:
        return redirect("/")

    favs = FavoriteNEO.objects.filter(user_email=user["email"])
    return render(request, "sentinel/favorites.html", {"favorites": favs, "user": user})

# details page about each neo
@csrf_exempt
def neo_details(request):
    if request.method == "POST":
        neo = {
            'name': request.POST.get("name"),
            'diameter': request.POST.get("diameter"),
            'speed': request.POST.get("speed"),
            'miss_distance': request.POST.get("miss_distance"),
            'date': request.POST.get("date"),
        }
        # Get AI summary and fun descriptions for this NEO
        summary_text = summarize_asteroid(neo)
        fun_descriptions = generate_fun_descriptions(neo)
        user = request.session.get('user')
        
        # Check if this NEO is already favorited by the user
        is_favorited = False
        if user:
            is_favorited = FavoriteNEO.objects.filter(
                user_email=user["email"],
                name=neo['name']
            ).exists()
        
        return render(request, 'sentinel/neo_details.html', {
            "neo": neo, 
            "summary": summary_text,
            "descriptions": fun_descriptions,
            "user": user,
            "is_favorited": is_favorited
        })
    return redirect('/neos')

# an endpoint that take takes neo details and a question and returns a json response from gemini
@csrf_exempt
def chat_quackstronaut(request):
    if request.method == "POST":
        neo = {
            'name': request.POST.get("name"),
            'diameter': request.POST.get("diameter"),
            'speed': request.POST.get("speed"),
            'miss_distance': request.POST.get("miss_distance"),
            'date': request.POST.get("date"),
        }
        question = request.POST.get("question")
        response = chat_with_quackstronaut(neo, question)
        
        return JsonResponse({
            'response': response,
            'success': True
        })
    return JsonResponse({'success': False})

# saved the current neo as a favorite
@csrf_exempt
def save_favorite(request):
    if request.method == "POST":
        neo_name = request.POST.get("name")
        user = request.session.get("user")

        if user and neo_name:
            try:
                # First, check if this favorite already exists
                existing_favorite = FavoriteNEO.objects.filter(
                    user_email=user["email"],
                    name=neo_name
                ).first()
                
                if existing_favorite:
                    # Update existing record instead of creating duplicate
                    existing_favorite.diameter = request.POST.get("diameter")
                    existing_favorite.speed = request.POST.get("speed") 
                    existing_favorite.miss_distance = request.POST.get("miss_distance")
                    existing_favorite.date = request.POST.get("date")
                    existing_favorite.save()
                else:
                    # Create new favorite
                    FavoriteNEO.objects.create(
                        user_email=user["email"],
                        name=neo_name,
                        diameter=request.POST.get("diameter"),
                        speed=request.POST.get("speed"),
                        miss_distance=request.POST.get("miss_distance"),
                        date=request.POST.get("date"),
                    )
            except Exception as e:
                # Handle any database errors gracefully
                print(f"Error saving favorite: {e}")
                # Continue to redirect even if there's an error
        
        # Redirect back to the referring page or fallback to NEOs list
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
                
    return redirect("/neos")

# Remove a NEO from favorites
@csrf_exempt
def unfavorite(request):
    if request.method == "POST":
        neo_name = request.POST.get("name")
        user = request.session.get("user")

        if user and neo_name:
            try:
                # Find and delete the favorite
                favorite = FavoriteNEO.objects.filter(
                    user_email=user["email"],
                    name=neo_name
                ).first()
                
                if favorite:
                    favorite.delete()
            except Exception as e:
                # Handle any database errors gracefully
                print(f"Error removing favorite: {e}")
                # Continue to redirect even if there's an error
        
        # Redirect back to the referring page or fallback to NEOs list
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
                
    return redirect("/neos")

