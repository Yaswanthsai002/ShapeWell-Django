from django.urls import path
from . import views
urlpatterns = [
    path('', views.signup, name='signup'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/',views.signout, name='signout'),
    path('collect/', views.collect, name='collect'),
    path('levelselection/', views.levelselection, name='levelselection'),
    path('beginner/', views.beginner, name='beginner'),
    path('intermediate/', views.intermediate, name='intermediate'),
    path('expert/', views.expert, name='expert'),
    path('profile/', views.profile, name='profile')
]
