from django.urls import path
from . import views

urlpatterns = [
    # path('example', views.ExampleView.as_view(), name="example"),
    path('login/', views.loginView, name="login"),
    path('register/', views.registerUserView, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
]