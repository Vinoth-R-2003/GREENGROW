from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_farmer = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    upi_id = models.CharField(max_length=50, blank=True, help_text="e.g. yourname@upi (required for getting payments)")
    
    # Social features
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    
    # Gamification
    level = models.IntegerField(default=1)
    badges = models.JSONField(default=list, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Rating(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rater} -> {self.seller} ({self.score})"

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent', null=True, blank=True)
    verb = models.CharField(max_length=255) # e.g., "liked your post", "ordered your product"
    target_url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient}: {self.verb}"
