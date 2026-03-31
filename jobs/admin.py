from django.contrib import admin
from .models import job_model,job_application_model
# Register your models here.

admin.site.register(job_model)
admin.site.register(job_application_model)