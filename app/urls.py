from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('home/', views.blog, name='blog'),
    path('type_of_user', views.type_of_user, name='type_of_user'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_signin/', views.user_signin, name='user_signin'),
    path('physician_signup/', views.physician_signup, name='physician_signup'),
    path('physician_signin/', views.physician_signin, name='physician_signin'),
    path('nutitionist_signup/', views.nutritionist_signup, name='nutritionist_signup'),
    path('nutitionist_signin/', views.nutritionist_signin, name='nutritionist_signin'),
    path('signout/',views.signout, name='signout'),
    path('collect/', views.collect, name='collect'),
    path('levelselection/', views.levelselection, name='levelselection'),
    path('beginner/', views.beginner, name='beginner'),
    path('intermediate/', views.intermediate, name='intermediate'),
    path('advanced/', views.advanced, name='advanced'),
    path('warrior1-knowledge/', views.warrior1_knowledge, name='warrior1-knowledge'),
    path('tree-knowledge/', views.tree_knowledge, name='tree-knowledge'),
    path('warrior2-knowledge/', views.warrior2_knowledge, name='warrior2-knowledge'),
    path('plank-knowledge/', views.plank_knowledge, name='plank-knowledge'),
    path('cobra-knowledge/', views.cobra_knowledge, name='cobra-knowledge'),
    path('downdog-knowledge/', views.downdog_knowledge, name='downdog-knowledge'),
    path('warrior1-knowledge/', views.warrior1_knowledge, name='warrior1-knowledge'),
    path('warrior3-knowledge/', views.warrior3_knowledge, name='warrior3-knowledge'),
    path('triangle-knowledge/', views.triangle_knowledge, name='triangle-knowledge'),
    path('goddess-knowledge/', views.goddess_knowledge, name='goddess-knowledge'),
    path('profile/', views.profile, name='profile'),
    path('posedetection/', views.posedetection, name='posedetection'),
    path('result/', views.result, name='result')
]