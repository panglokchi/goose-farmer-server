from django.urls import path
from goose_farmer_game import views
from knox import views as knox_views

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('test/', views.ExampleView.as_view()),
    path('verify/', views.verificationView.as_view()),
]
