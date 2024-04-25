from django.contrib import admin
from .models import Hashtag

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    pass
