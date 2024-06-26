from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=160)

    def __str__(self):
        return self.name


class Channel(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)
    # many to many relationship with the User model
    # the related name is participants, which means we can access the participants of a channel by calling channel.participants
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    # once the user is deleted, all the messages will be deleted
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # once the channel is deleted, all the messages will be deleted
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[:50]
