from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lodge/', views.grevance, name = "lodge_grevance"),
    path('view/<int:pk>/', views.post, name = "view_grevance"),
    path('login/',views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),
    path('change_status/<int:pk>/', views.change_status, name='change_status'),
]