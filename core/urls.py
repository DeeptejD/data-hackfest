"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sentinel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('callback/', views.callback, name='callback'),
    path('neo-details/', views.neo_details, name='neo_details'),
    path('chat-quackstronaut/', views.chat_quackstronaut, name='chat_quackstronaut'),
    path("save_favorite/", views.save_favorite, name="save_favorite"),
    path("unfavorite/", views.unfavorite, name="unfavorite"),
    path("neos/favorites/", views.favorites, name="favorites"),
    path("neos/", views.index, name="neos"),
    path("profile/", views.profile, name="profile"),
    path("api/daily-briefing/", views.get_daily_briefing, name="daily_briefing"),
    path("api/neos-data/", views.get_neos_data, name="neos_data"),
    path("api/neo-summary/", views.get_neo_summary, name="neo_summary"),
    path("api/neo-descriptions/", views.get_neo_descriptions, name="neo_descriptions"),
    path('', views.home, name='home'),
]
