from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("", include("django.contrib.auth.urls")),
]

