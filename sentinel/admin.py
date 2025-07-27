from django.contrib import admin
from .models import FavoriteNEO, UserInteraction, Achievement, UserAchievement

admin.site.register(FavoriteNEO)
admin.site.register(UserInteraction)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
