from django.db import models

# Create your models here.

class ChatResponse(models.Model):
    chat = models.JSONField(blank = True)

class Document(models.Model):
    doc = models.FileField(upload_to='docs/')
    selected = models.BooleanField(default=True)