from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.create_job),
    path('list/',views.list_job),
    path('view/',views.view_job),
    path('adminview/',views.update_job),
    path('adminlist/',views.comp_list_job),
    path('delete/',views.delete_job),
    path('apply/',views.apply_job),
    path('applicants/',views.applicann_list),
    path('latest/',views.latest),
]
