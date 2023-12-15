from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
import uuid
from datetime import date


# Create your models here.
class Room(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    join_code = models.CharField(max_length=7)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create an Admin instance for the owner
        Admin.objects.create(user=self.owner, room=self)

# models.py
from django.contrib.auth.models import User
from django.db import models

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile.jpg')
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile.jpg')
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username

class Announcement(models.Model):
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    body = models.TextField()
    id = models.AutoField(primary_key=True)

    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Admin, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.author.user.username}'s Announcement"

    @classmethod
    def recent_activities(cls, limit=10):
        return cls.objects.order_by('-created_at')[:limit]

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.announcement.title}"


class bills(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amount = models.IntegerField()
    title = models.CharField(max_length=30)
    due = models.DateTimeField(null=True)
    assigned = models.DateField(auto_now=True)
    slug = models.SlugField(null=False, blank=False, default="")

    @classmethod
    def recent_activities(cls, limit=10):
        return cls.objects.order_by('-created_at')[:limit]


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bills = models.ForeignKey(bills, on_delete=models.CASCADE)
    proof = models.FileField(null=True)
    

class Task(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default="")
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class GroupContrib(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=30)
    due = models.DateTimeField(null=True)
    assigned = models.DateField(auto_now=True)
    slug = models.SlugField(null=False, blank=False, default="")
    selected_user_ids = models.ManyToManyField(User, related_name='selected_user_ids')

    @classmethod
    def recent_activities(cls, limit=10):
        return cls.objects.order_by('-created_at')[:limit]

    def save(self, *args, **kwargs):
        if not self.id:
            self.amount = self.amount or 0
        else:
            self.amount = self.amount
        super(GroupContrib, self).save(*args, **kwargs)


    
