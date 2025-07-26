import os
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect

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
    return render(request, 'sentinel/index.html', context={'user': user})

def login(request):
    return oauth.auth0.authorize_redirect(request, os.getenv("AUTH0_CALLBACK_URL"))

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    user_info = oauth.auth0.get(f'https://{os.getenv("AUTH0_DOMAIN")}/userinfo', token=token).json()

    print("User info:", user_info)

    request.session['user'] = user_info
    return redirect('/')

def logout(request):
    django_logout(request)
    return HttpResponseRedirect(
        f'https://{os.getenv("AUTH0_DOMAIN")}/v2/logout?'
        f'returnTo={os.getenv("AUTH0_LOGOUT_URL")}&'
        f'client_id={os.getenv("AUTH0_CLIENT_ID")}'
    )

# Create your views here.
