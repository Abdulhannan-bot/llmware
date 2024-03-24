from django.contrib import admin
from .models import Document, ChatResponse
# Register your models here.

class DocumentAdmin(admin.ModelAdmin):
    list_display = ["id","doc", "selected"]

admin.site.register(Document, DocumentAdmin)

class ChatResponseAdmin(admin.ModelAdmin):
    list_display = ["id"]

admin.site.register(ChatResponse, ChatResponseAdmin)