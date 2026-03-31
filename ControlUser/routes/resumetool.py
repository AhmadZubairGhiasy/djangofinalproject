#tools for user to upload and manage resume
from ControlUser.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.http import FileResponse,HttpResponse,JsonResponse
from pathlib import Path
import os


# pdf tools
import pdfplumber


#

# app data
from ControlUser.form import UserResumeForm
from django.conf import settings




import requests
import json












@login_required(login_url="/user:login")
def setuserresume(request):
    if request.method =='POST':
                
        if request.user.resume_pdf:
            path = os.path.join(settings.BASE_DIR,"media/users",str(request.user.id),'resume.pdf')
            os.remove(path)
            print("deleted old resume at path:",path)
     
        form = UserResumeForm(request,request.FILES,instance=request.user)
        if not form.is_valid():
            return render(request,'ControlUser/message.html',{"validation":True,'message':"one of the field is not valid","redirectTo":"/user:setphoto"})
        form.save()
        return redirect('/user:u/')
    form =UserResumeForm()
    return render(request,"ControlUser/form.html",{"form":form})




@login_required(login_url="/user:login")
def getuserresume(request):
    id = request.GET.get("id")
    user = get_object_or_404(User,id = id)
    print(id)
    path = Path(Path.joinpath(settings.BASE_DIR,"media/users",F"{id}","resume.pdf"))
    print("photo path:",path.exists())
    if not user.resume_pdf:
        return HttpResponse("This user has not uploaded resume yet.")
    print(path)
    return FileResponse(path.open('rb'),
                        as_attachment=True,
                        filename='resume.pdf',
                        content_type="application/pdf")
    #return HttpResponse("hellow")


import requests
@login_required(login_url="/user:login")
def gendata(request):
    id = request.GET.get("id")
    path = Path(Path.joinpath(settings.BASE_DIR,"media/users",F"{id}","resume.pdf"))
    response = requests.post(
    "https://extraction-api.nanonets.com/api/v1/extract/sync",
    headers={"Authorization": "Bearer 41a4e54b-f2fa-11f0-a8a5-62476a3a77ca"},
    files={"file": open(path, "rb")},
    data={"output_format": "json"}
)

    result = response.json()
    record_id = result["record_id"]
    res = requests.get(
        f"https://extraction-api.nanonets.com/api/v1/extract/results/{record_id}",
        headers={"Authorization": "Bearer 41a4e54b-f2fa-11f0-a8a5-62476a3a77ca"},
    )
    rest = res.json()
    
    data = rest["result"]["json"]["content"]
    user = User.objects.get(id=id)
    user.full_name = data.get("name") or user.full_name
    user.job_industry = data.get("current_role") or user.job_industry
    user.about = data.get("objective") or user.about
    user.Phone = data.get("phone")or user.Phone
    user.save()
    return JsonResponse({"data":data})
    
