import os
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from .nasa import fetch_neos
from django.views.decorators.csrf import csrf_exempt
from .gemini import summarize_asteroid
from .models import FavoriteNEO


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

def index(request):
    user = request.session.get('user')
    neos = fetch_neos()
    return render(request, 'sentinel/index.html', context={'user': user, 'neos': neos})

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

@csrf_exempt
def summary(request):
    if request.method == "POST":
        neo = {
            'name': request.POST.get("name"),
            'diameter': request.POST.get("diameter"),
            'speed': request.POST.get("speed"),
            'miss_distance': request.POST.get("miss_distance"),
            'date': request.POST.get("date"),
        }
        summary_text = summarize_asteroid(neo)
        return render(request, 'sentinel/summary.html', {"summary": summary_text, "neo": neo})
    return redirect('/')

def favorites(request):
    user = request.session.get("user")
    if not user:
        return redirect("/")

    favs = FavoriteNEO.objects.filter(user_email=user["email"])
    return render(request, "sentinel/favorites.html", {"favorites": favs})

@csrf_exempt
def save_favorite(request):
    if request.method == "POST":
        neo_name = request.POST.get("name")
        user = request.session.get("user")

        if user and neo_name:
            # Use get_or_create to prevent duplicates based on user_email and name
            favorite, created = FavoriteNEO.objects.get_or_create(
                user_email=user["email"],
                name=neo_name,
                defaults={
                    'diameter': request.POST.get("diameter"),
                    'speed': request.POST.get("speed"),
                    'miss_distance': request.POST.get("miss_distance"),
                    'date': request.POST.get("date"),
                }
            )
    return redirect("/")

