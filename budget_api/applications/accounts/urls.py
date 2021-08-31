from django.urls import path
from .views.account_movement import AccountMovement
from .views.account_open_and_details import AccountView


urlpatterns = [
    # account openning
    path('', AccountView.as_view()),
    # account movement
    path('movement', AccountMovement.as_view()),
]
