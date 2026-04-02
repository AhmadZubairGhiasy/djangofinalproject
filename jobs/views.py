from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import job_model,job_application_model
from ControlUser.models import User
from CompanyProfile.models import Company_db_model
from .form import jobCreationForm, jobeditform,editdesciform,editsummeryform,editsumbmisionform
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
        return redirect('/job:adminlist/')
    form = jobCreationForm()
    return render(request,'jobform.html',{"form":form})



@login_required(login_url='/user:login')
def delete_job(request):
    id = request.GET.get('id')

    job = job_model.objects.filter(id=id)[0]
    job.delete()
    return redirect('/job:adminlist/')  

@login_required(login_url='/user:login')
def update_job(request):
    id = request.GET.get('id')
    type = request.GET.get('type')
    action = request.GET.get('acton')
    job = job_model.objects.filter(id=id)[0]
    print("type:", type)
    print("action:", action)
    print("id:", id)

    if action == "edit":
        if type == "gen":
            if request.method == 'POST':
                form = jobeditform(request.POST,instance=job)
                if not form.is_valid():
                    return render(request,'ControlUser/message.html',{"validation":True,'message':"form is not valide","redirectTo":f"/job:adminview/?id={id}&type=gen&acton=edit"})
                form.save()
                return redirect(f'/job:adminview/?id={job.id}')
            form = jobeditform(instance=job)
            return render(request,'jobedit.html',{"form":form,"job":job})

        elif type == "jobsum":
            if request.method == 'POST':
                form = editsummeryform(request.POST,instance=job)
                if not form.is_valid():
                    return render(request,'ControlUser/message.html',{"validation":True,'message':"form is not valide","redirectTo":f"/job:adminview/?id={id}&type=jobsum&acton=edit"})
                form.save()
                return redirect(f'/job:adminview/?id={job.id}')
            form = editsummeryform(instance=job)
            return render(request,'jobedit.html',{"form":form,"job":job})

        elif type == "jobdes":
            if request.method == 'POST':
                form = editdesciform(request.POST,instance=job)
                if not form.is_valid():
                    return render(request,'ControlUser/message.html',{"validation":True,'message':"form is not valide","redirectTo":f"/job:adminview/?id={id}&type=jobdes&acton=edit"})
                form.save()
                return redirect(f'/job:adminview/?id={job.id}')
            form = editdesciform(instance=job)
            return render(request,'jobedit.html',{"form":form,"job":job})

        elif type == "jobsubmision":
            if request.method == 'POST':
                form = editsumbmisionform(request.POST,instance=job)
                if not form.is_valid():
                    return render(request,'ControlUser/message.html',{"validation":True,'message':"form is not valide","redirectTo":f"/job:adminview/?id={id}&type=jobsubmision&acton=edit"})
                form.save()
                return redirect(f'/job:adminview/?id={job.id}')
            form = editsumbmisionform(instance=job)
            return render(request,'jobedit.html',{"form":form,"job":job})

    
    
    return render(request,'jobedit.html',{"job":job})


@login_required(login_url='/user:login')
def list_job(request):
   
    jobslist = job_model.objects.all()

    action = request.POST.get('action')
    search_query = request.POST.get('requestjob')
    if action == "search":
        jobslist = jobslist.filter(jobtitle__icontains=search_query) | jobslist.filter(category__icontains=search_query) | jobslist.filter(job_address__icontains=search_query ) | jobslist.filter(job_location_type__icontains=search_query )
    return render(request,'jobslist.html',{"jobslist":jobslist})

@login_required(login_url='/user:login')
def comp_list_job(request):
    user = request.user
    company = Company_db_model.objects.filter(Owner = user)[0]
    jobslist = job_model.objects.filter(company_name = company)
    
    
    action = request.POST.get('action')
    search_query = request.POST.get('requestjob')
    if action == "search":
        jobslist = jobslist.filter(jobtitle__icontains=search_query) | jobslist.filter(category__icontains=search_query) | jobslist.filter(job_location_type__icontains=search_query ) | jobslist.filter(job_address__icontains=search_query )
    return render(request,'compjobslist.html',{"jobslist":jobslist})



@login_required(login_url='/user:login')
def view_job(request):
    id = request.GET.get('id')
    job = job_model.objects.filter(id=id)[0]
    return render(request,'jobreview.html',{"job":job})




@login_required(login_url='/user:login')
def apply_job(request):
    id = request.GET.get('id')
    job = job_model.objects.filter(id=id)[0]
    user = request.user
    #job_application_model.objects.all().delete()  # delete this line after testing
    isapplied = job_application_model.objects.filter(job=job, applicant=user).exists()
    if isapplied:
        return redirect(f'/job:view/?id={id}')
    applicant = job_application_model.objects.create(job=job, applicant=user)
    applicant.save()
    return redirect(f'/job:view/?id={id}')




@login_required(login_url='/user:login')
def applicann_list(request):
    id = request.GET.get('id')
    job = job_model.objects.filter(id=id)[0]
    applicants = job_application_model.objects.filter(job=job)

    action= request.GET.get('action')
    search_query = request.POST.get('requestapplicant')
    if action == "search":

        applicants = applicants.filter(applicant__email__icontains=search_query) | applicants.filter(applicant__full_name__icontains=search_query) | applicants.filter(applicant__Phone__icontains=search_query)
        print(applicants)
        return render(request,'applicant.html',{"applicants":applicants,"job":job})


    return render(request,'applicant.html',{"applicants":applicants,"job":job})


@login_required(login_url='/user:login')
def latest(request):
    jobslist = job_model.objects.order_by('-createat')
   
    return render(request,'jobslist.html',{"jobslist":jobslist})