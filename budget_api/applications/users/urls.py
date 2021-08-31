from django.urls import path
from .views import CreateUser, ReadUser


urlpatterns = [
    path('create_user', CreateUser.as_view()),
    path('', ReadUser.as_view()),
    path('<int:id>/', ReadUser.as_view()),
]
