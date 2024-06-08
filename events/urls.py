from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('', views.eventList, name="events"),
    path('add-event/', views.event_add, name="add_event"),
    path('update-event/<int:event_id>/', views.event_update, name="update_event"),
    path('delete-event/<int:event_id>/', views.eventList, name="delete_event"),
    path('filter/', views.filter_events, name="filter_events"),
]