from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.loginpage ,name='loginpage'),
    path('logout/', views.logoutpage ,name='logoutpage'),
    path('register/', views.registerpage ,name='registerpage'),
    path('',views.home,name='home'),#name= of the page
    #''-indicates home page 
    path('room/<str:p>/',views.room,name='room'),
    #path('create-topic/',views.create_topic,name='create-topic'),
    path('create-room/',views.create_room,name='create-room'),
    path('update-room/<str:p>/',views.update_room,name='update-room'),
    path('delete-room/<str:p>/',views.delete_room,name='delete-room'),
    path('delete-message/<str:p>/',views.delete_message,name='delete-message'),
    path('profile/<str:p>/',views.profile,name='profile'),
    path('test/',views.test,name='test'),
    path('follow/',views.follow,name='follow'),
    path('unfollow/',views.unfollow,name='unfollow'),
    # path('update-profile/<str:p>',views.update_profile,name='update-profile'),
]    

