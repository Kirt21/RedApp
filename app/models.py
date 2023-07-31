from tkinter import Widget
from django.db import models
from django.contrib.auth.models import UserManager,AbstractUser
    
class User(AbstractUser):
    profile_photo=models.ImageField(upload_to="app/files/propics",blank=True,null=True)
    Bio=models.TextField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.username

class Topic(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Rooms(models.Model):
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    host=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=100)
    desc = models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

class Message(models.Model):
    user_name=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Rooms,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:45]

class Follower(models.Model):
    follower=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    following=models.ForeignKey(Rooms, on_delete=models.SET_NULL,null=True)
    



