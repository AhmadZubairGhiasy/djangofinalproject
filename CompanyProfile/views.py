import os
from pathlib import Path
from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect
from django.http import FileResponse, HttpResponse,JsonResponse
from .form import CompanyBasicDetailsForm, CompanySummaryForm, SetCompanyLogoForm, SetCompanycoverForm, company_Creation_Form
from .models import Company_db_model
from django.contrib.auth.decorators import login_required



















@login_required(login_url="/user:login")
def Create_Company(request):
    user = request.user
    if Company_db_model.objects.filter(Owner = user):
        return render(request,'ControlUser/message.html',{'message':"Only one company a user can have","error":True,"redirectTo":"/"})

    if request.method =='POST':
        
        form = company_Creation_Form(request.POST)
        if not form.is_valid():
            return render(request,'ControlUser/message.html',{"validation":True,'message':"form is not valide","redirectTo":"/company:create"})
        savingdata = form.save(commit=False)
        savingdata.Owner = user
        print(savingdata.Owner_id)
        savingdata.save()

        return redirect('/')
    form = company_Creation_Form
    return render(request,'CompanyForm.html',{"form":form})
























@login_required(login_url="/user:login")
def get_Company(request):
    id = request.GET.get("id")
    user = request.user
    print(id)
    print(user)
    company =list(Company_db_model.objects.filter(id = id).values())
    print(company)
    #return JsonResponse({"data":list(company)})
    if company:
        #return render(request,'ControlUser/message.html',{"normal":True,'message':f"{company}"})
        return render(request,'getcompany.html',{'company':list(company)[0]})
    return render(request,'ControlUser/message.html',{"normal":True,'message':f"company not found",})
   


















@login_required(login_url="/user:login")
def all_companies(request):
    usercompany = Company_db_model.objects.filter(Owner = request.user)
    if request.method=='POST':
        usersearch = request.POST.get("requestuser")
        companies =Company_db_model.objects.filter(company_name__icontains = usersearch).exclude(Owner = request.user)
        return render(request,'explorecompanies.html',{'companies':companies})
    companies =Company_db_model.objects.all().exclude(Owner = request.user)
    return render(request,'explorecompanies.html',{'companies':companies,"usercompany":usercompany})
    












@login_required(login_url="/user:login")
def delete_Company(request):
    id = request.GET.get("id")
    user = request.user.email
    print(id)
    print(user)
    company =Company_db_model.objects.filter(id = id)
    company.delete()
    return JsonResponse({"message":F"company profile with id : {id} deleted"})
    
    

















@login_required(login_url="/user:login")
def update_Company(request):
    return HttpResponse("update company")



















@login_required(login_url="/user:login")
def setcompanylogo(request):
    company = Company_db_model.objects.get(Owner= request.user)
    if not company:
        return render(request,'ControlUser/message.html',{"validation":True,'message':"you don't have company","redirectTo":"/user:u"})
    if request.method =='POST':
        print("logo: ",request.FILES)
        if not request.FILES:
            return redirect("/company:get/")
        if company.Company_logo:
            path = os.path.join(settings.BASE_DIR,"media/companies",str(company.id),'company_logo.jpg')
            if Path(path).exists():
                 os.remove(path)
            print("deleted old logo at path:",path)
            company.Company_logo.delete()
            company.save()
        form = SetCompanyLogoForm(request.POST,request.FILES,instance=company)
        if not form.is_valid():
            return render(request,'ControlUser/message.html',{"validation":True,'message':"one of the field is not valid","redirectTo":"/user:setphoto"})
        form.save()
        return redirect("/company:get/")
    form = SetCompanyLogoForm()
    return render(request,'CompanyForm.html',{'form':form,"company":company})


















@login_required(login_url="/user:login")
def setcompanycover(request):
    company = Company_db_model.objects.get(Owner= request.user)
    if not company:
        return render(request,'ControlUser/message.html',{"validation":True,'message':"you don't have any company","redirectTo":"/user:u"})
    
    if request.method =='POST':
        print("cover:",request.FILES)
        if not request.FILES:
            return redirect("/company:get/")
        if company.Company_cover_Photo:
            path = os.path.join(settings.BASE_DIR,"media/companies",str(company.id),'company_cover.jpg')
            if Path(path).exists():
                 os.remove(path)
            company.Company_cover_Photo.delete()
            company.save()
            print("deleted old logo at path:",path)
            
        form = SetCompanycoverForm(request.POST,request.FILES,instance=company)
        if not form.is_valid():
            return render(request,'ControlUser/message.html',{"validation":True,'message':"one of the field is not valid","redirectTo":"/user:setphoto"})
        form.save()
        
        return redirect("/company:get/")
    form = SetCompanycoverForm()
    return render(request,'CompanyForm.html',{'form':form,"company":company})

















@login_required(login_url="/user:login")
def getcompanylogo(request):
    compid = request.GET.get("id")
    company=Company_db_model.objects.get(id = compid)
    path = Path(os.path.join(settings.BASE_DIR,"media/companies",str(compid),"company_logo.jpg"))
    print("logo path: ",path)
    if not company.Company_logo:
        path = Path(Path.joinpath(settings.BASE_DIR,"media/users/coverphoto.jpg"))
        return FileResponse(path.open('rb'),content_type="image")
    print(path)
    return FileResponse(path.open('rb'),content_type="image")
















@login_required(login_url="/user:login")
def getcompanycover(request):

    compid = request.GET.get("id")
    company=Company_db_model.objects.get(id = compid)
    path = Path(os.path.join(settings.BASE_DIR,"media/companies",str(compid),"company_cover.jpg"))
    print("cover path: ",path)
    if not company.Company_logo:
        path = Path(Path.joinpath(settings.BASE_DIR,"media/users/coverphoto.jpg"))
        return FileResponse(path.open('rb'),content_type="image")
    print(path)
    return FileResponse(path.open('rb'),content_type="image")













@login_required(login_url="/user:login")
def edit_Company(request):
    company =list(Company_db_model.objects.filter(Owner = request.user))[0]
    print(company)
    #return JsonResponse({"data":list(company)})
    if not company:
        #return render(request,'ControlUser/message.html',{"normal":True,'message':f"{company}"})
        return render(request,'ControlUser/message.html',{"normal":True,'message':f"company not found",})
       
    formtype = request.GET.get("FormType")
    modelid = request.GET.get("id")
    print("form type is: ",formtype)
    print("post request: ",request.POST)
    print("get request: ",request.GET)
    form = False
    user = request.user
    print(id)
    print(user)

    if formtype:
    
        instance = get_object_or_404(Company_db_model,id = modelid)
        if formtype == "EditDetails":
            if request.method =='POST':
                form = CompanyBasicDetailsForm(request.POST,instance=instance)
                print("form is: ",form.save(commit=False))
                if not form.is_valid():
                    return render(request,'ControlUser/message.html',{"validation":True,'message':"company input is not valid","redirectTo":"/company:editcompany/"})
                form.save()
                return redirect('/company:get/') 
            form = CompanyBasicDetailsForm(instance=instance)

        if formtype == "EditSummary":
            if request.method =='POST':
                form = CompanySummaryForm(request.POST,instance=instance)
                if not form.is_valid():
                    return render(request,'ControlUser/message.html',{"validation":True,'message':"company input is not valid","redirectTo":"/company:editcompany/"})
                form.save()
                return redirect('/company:get/')
            form = CompanySummaryForm(instance=instance)

    return render(request,'editcompany.html',{'company':company,'form':form})