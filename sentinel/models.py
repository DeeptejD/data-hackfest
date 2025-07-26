from django.db import models
class FavoriteNEO(models.Model):
    user_email = models.EmailField()
    name = models.CharField(max_length=100)
    diameter = models.CharField(max_length=50)
    speed = models.CharField(max_length=50)
    miss_distance = models.CharField(max_length=50)
    date = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.user_email}"