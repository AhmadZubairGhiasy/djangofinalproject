from django.http import HttpResponse
from django.shortcuts import render
from jobs.models import job_model
from django.contrib.auth.decorators import login_required

@login_required(login_url='/user:login')
def home(request):
    jobslist = job_model.objects.all()
    return render(request,'jobslist.html',{"jobslist":jobslist})