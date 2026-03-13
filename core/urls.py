from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('tinder/', views.tinder_view, name='tinder'),
    path('swipe/', views.swipe_view, name='swipe'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('chat/', views.chat_view, name='chat'),
    path('set-search-mode/', views.set_search_mode, name='set_search_mode'),
    path('event/<int:event_id>/join/', views.event_join, name='event_join'),
    path('event/<int:event_id>/leave/', views.event_leave, name='event_leave'),
    path('about/', views.about_view, name='about'),
]
