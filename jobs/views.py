from django.shortcuts import render
from django.http import HttpResponse
from .models import job_model
from ControlUser.models import User
from CompanyProfile.models import Company_db_model
from .form import jobCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.



# crud operations for jobs
@login_required(login_url='/user:login')
def create_job(request):
    user = request.user
    company = Company_db_model.objects.filter(Owner = user)[0]
    print(company)
    if request.method == 'POST':
        form = jobCreationForm(request.POST)
        if not form.is_valid():
            return render(request,'ControlUser/message.html',{"validation":True,'message':"form is not valide","redirectTo":"/job:create"})
        savingdata = form.save(commit=False)
        savingdata.company_name = company
        form.save()
        
    form = jobCreationForm()
    return render(request,'jobform.html',{"form":form})



@login_required(login_url='/user:login')
def delete_job(request):
    return HttpResponse("edit job with id "+str(job_id))

@login_required(login_url='/user:login')
def update_job(request):
    return HttpResponse("edit job with id "+str(job_id))


@login_required(login_url='/user:login')
def list_job(request):
   
    jobslist = job_model.objects.all()
    return render(request,'jobslist.html',{"jobslist":jobslist})

@login_required(login_url='/user:login')
def comp_list_job(request):
    return HttpResponse("edit job with id ")

