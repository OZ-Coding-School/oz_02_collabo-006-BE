from django.urls import path
from users.views import UserView, Users

urlpatterns = [
    path('', Users.as_view()),
]