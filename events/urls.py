from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('events/', views.eventList, name="events"),
    path('add-event/', views.event_add, name="add_event"),
    path('update-event/<int:event_id>/', views.event_update, name="update_event"),
    path('delete-event/<int:event_id>/', views.delete_event, name="delete_event"),
]