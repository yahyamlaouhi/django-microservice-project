from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("/create", views.CustomUserCreateView.as_view(), name="user"),
    path("/token", views.CreateTokenView.as_view(), name="token"),
]
