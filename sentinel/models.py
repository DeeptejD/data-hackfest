from django.db import models

class FavoriteNEO(models.Model):
    user_email = models.EmailField()
    name = models.CharField(max_length=100)
    diameter = models.CharField(max_length=50)
    speed = models.CharField(max_length=50)
    miss_distance = models.CharField(max_length=50)
    date = models.CharField(max_length=50)

    class Meta:
        unique_together = ['user_email', 'name']

    def __str__(self):
        return f"{self.name} - {self.user_email}"


class UserInteraction(models.Model):
    """Track user interactions for achievements"""
    user_email = models.EmailField()
    interaction_type = models.CharField(max_length=50)  # 'chat_question', 'neo_favorited', 'neo_viewed'
    neo_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_email} - {self.interaction_type}"


class Achievement(models.Model):
    """Define available achievements"""
    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10)  # Emoji icon
    category = models.CharField(max_length=50)
    requirement = models.IntegerField()  # Number needed to unlock
    requirement_type = models.CharField(max_length=50)  # 'chat_questions', 'favorites_count', etc.
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Track which achievements users have unlocked"""
    user_email = models.EmailField()
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user_email', 'achievement']
    
    def __str__(self):
        return f"{self.user_email} - {self.achievement.name}"