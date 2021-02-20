from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Chat(models.Model):
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages",  on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name = 'messages', on_delete=models.CASCADE)
    class Meta:
        ordering = ["sent_at"]
