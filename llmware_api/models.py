from django.db import models

# Create your models here.

class ChatResponse(models.Model):
    chat = models.JSONField(blank = True)