from django.urls import path
from .views import HashtagCreate

urlpatterns = [
    path('create/', HashtagCreate.as_view(), name='hashtag-create'),
]