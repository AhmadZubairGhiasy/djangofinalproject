from django.urls import path

from . import views

urlpatterns = [
    path('create/',views.Create_Company),
    path('view/',views.get_Company),
    path('get/',views.edit_Company),
    path('all/',views.all_companies),
    path('delete/',views.delete_Company),
    path('getlogo/',views.getcompanylogo),
    path('setlogo/',views.setcompanylogo),
    path('getcover/',views.getcompanycover),
    path('setcover/',views.setcompanycover),
    
]
