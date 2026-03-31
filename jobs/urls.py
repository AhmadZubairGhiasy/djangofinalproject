from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.create_job),
    path('list/',views.list_job),
]
