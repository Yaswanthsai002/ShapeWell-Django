from django.urls import path
from . import views
urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/',views.signout, name='signout'),
    path('collect/', views.collect, name='collect'),
    path('levelselection/', views.levelselection, name='levelselection'),
    path('beginner/', views.beginner, name='beginner'),
    path('intermediate/', views.intermediate, name='intermediate'),
    path('expert/', views.expert, name='expert'),
    path('t-knowledge/', views.t_knowledge, name='t-knowledge'),
    path('tree-knowledge/', views.tree_knowledge, name='tree-knowledge'),
    path('warrior2-knowledge/', views.warrior2_knowledge, name='warrior2-knowledge'),
    path('plank-knowledge/', views.plank_knowledge, name='plank-knowledge'),
    path('cobra-knowledge/', views.cobra_knowledge, name='cobra-knowledge'),
    path('downdog-knowledge/', views.downdog_knowledge, name='downdog-knowledge'),
    path('warrior1-knowledge/', views.warrior1_knowledge, name='warrior1-knowledge'),
    path('warrior3-knowledge/', views.warrior3_knowledge, name='warrior3-knowledge'),
    path('triangle-knowledge/', views.triangle_knowledge, name='triangle-knowledge'),
    path('profile/', views.profile, name='profile'),
    path('posedetection/', views.posedetection, name='posedetection'),
    path('result/', views.result, name='result')
]
