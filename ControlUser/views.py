from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,FileResponse,JsonResponse


from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
# Create your views here.



from django.conf import settings
from pathlib import Path
import os

from django.contrib.auth.forms import AuthenticationForm

from CompanyProfile import form
from .form import UserCreationForm,CustomLoginForm,UserPhotoForm,UserResumeForm,UserSkillForm,UseraboutForm,UsercertForm,UserprojectForm,UsereduForm,UserexpForm,ProfileEditForm,UserCoverPhotoForm
from django.contrib.auth import login,logout
from .models import User,UserProjects,UserCertification,UserSkill,UserEdu,UserExp



# register logic
def register_user(request):

    if request.user.is_authenticated:
        return redirect('/')


    if request.method=='POST':
        print(request.POST)
        form = UserCreationForm( request.POST)
        if not form.is_valid():
            return render(request,'ControlUser/message.html',{"validation":True,'message':"one of the field is not valid","redirectTo":"/user:register"})
            
        
        login(request,form.save())
        return redirect('/user:u/')
    form = UserCreationForm
    return render(request,"ControlUser/form.html",{"form":form})



# login logic
def login_user(request):
    

    next_url = request.POST.get("next") or request.GET.get("next")
    
    if request.user.is_authenticated:
        return redirect(next_url or '/user:u/')
    print(next_url)
    if request.method=='POST':
        print(request.POST)
        form = CustomLoginForm(request,data = request.POST)
       
        if not form.is_valid():
            return render(request,'ControlUser/message.html',{"validation":True,'message':"one of the field is not valid","redirectTo":"/user:login"})
            
        
        login(request,form.get_user())
        return redirect(next_url or '/user:u/')
    form =CustomLoginForm
    return render(request,"ControlUser/form.html",{"form":form})


@login_required(login_url="/user:login")
def logout_user(request):
    logout(request)
    return redirect('/user:login/')


# get user logic
@login_required(login_url="/user:login")
def get_user(request):
    form_name = request.GET.get("formName")
    editid = request.GET.get("editid")
    deleteid = request.GET.get("deleteid")
  


    print('formname is:',form_name)
    print("edit id status: ",editid)
    print("delete id status: ",deleteid)



    form = False
    

   

    if form_name:


        if form_name== "userInfo":
            if request.method =='POST':
                form = ProfileEditForm(request.POST,instance=request.user)
                print("expect user to add info: ",form.save())
                if not form.is_valid():
                    return render(request,'ControlUser/message.html',{'validation':True,
                    'message':"invalid entery"
                    })
                form.save()
                
                return redirect('/user:u/')                
            if editid:
               
                form = ProfileEditForm(instance=request.user)


       
        if form_name== "userSkill":
            # create skill logic
            if request.method =='POST':
                if not editid and not deleteid: 
                    form = UserSkillForm(request.POST)
                    skill = form.save(commit=False)

                    if not form.is_valid() or skill.skill ==None:
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"invalid entery"
                        })

                    if not editid and UserSkill.objects.filter(user = request.user , skill = skill.skill).exists():
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"This skill is already added"
                        })

                    skill.user = request.user
                    skill.save()
                    return redirect('/user:u/')                

            
                # edit skill logic
                if editid :
                    instance = get_object_or_404(UserSkill, id=editid)
                    skillname = instance.skill
                    form = UserSkillForm(request.POST,instance = instance)
                    skill = form.save(commit=False)
                    if skill.skill != skillname and UserSkill.objects.filter(user = request.user , skill = skill.skill).exists():
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"This skill is already added"
                        })
                    skill.save()


                    return redirect('/user:u/')
            
            # delete skill logic
            if deleteid:
                instance = get_object_or_404(UserSkill, id=deleteid)
                print("expected instance to delete: ",instance)
                instance.delete()
                return redirect('/user:u/')
            

            # server form display logic
            form = UserSkillForm()

            # server form edit display logic
            if editid:
                instance = get_object_or_404(UserSkill, id=editid)
                print("expected instance to edit: ",instance)
                form = UserSkillForm(instance=instance)

    



        if form_name== "userAbout":
            if request.method =='POST':
                form = UseraboutForm(request.POST,instance=request.user)
                print("expect user to add about: ",form.save())
                if not form.is_valid():
                    return render(request,'ControlUser/message.html',{'validation':True,
                    'message':"invalid entery"
                    })
                form.save()
                
                return redirect('/user:u/')                
            form = UseraboutForm()
            if editid:
               
                form = UseraboutForm(instance=request.user)


    

     
        if form_name== "userEdu": 
            if request.method =='POST':
                # create edu logic
                if not editid and not deleteid:
                    form = UsereduForm(request.POST)
                    edu = form.save(commit=False)

                    if not form.is_valid() or not edu.SchoolName:
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"invalid entery"
                        })
                    elif UserEdu.objects.filter(SchoolName = edu.SchoolName,degreelevel= edu.degreelevel,user = request.user).exists():
                        return render(request,'ControlUser/message.html',{'normal':True,
                        'message':"This education is already added"
                        })
                    elif not edu.start >edu.end and edu.start == edu.end:
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"you start date must be less than end date"
                        })
                    edu.user = request.user
                    edu.save()
                    return redirect('/user:u/')
                # edit edu logic
                if editid :
                    instance = get_object_or_404(UserEdu, id=editid)
                    eduname = instance.SchoolName
                    degreelevel = instance.degreelevel
                    form = UsereduForm(request.POST,instance = instance)
                    edu = form.save(commit=False)
                    if eduname != edu.SchoolName and degreelevel != edu.degreelevel and UserEdu.objects.filter(SchoolName = edu.SchoolName,degreelevel= edu.degreelevel,user = request.user).exists():
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"This education is already added"
                        })
                    elif not edu.start >edu.end and edu.start == edu.end:
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"you start date must be less than end date"
                        })
                    edu.save()
                    return redirect('/user:u/')

            form = UsereduForm()
            if editid:
                instance = get_object_or_404(UserEdu, id=editid)
                print("expected instance to edit: ",instance)
                form = UsereduForm(instance=instance)

            if deleteid:
                instance = get_object_or_404(UserEdu, id=deleteid)
                instance.delete()
                form = False

       
  
       
        if form_name== "userExp":
            if request.method == 'POST':
                if not editid and not deleteid:
                    form = UserexpForm(request.POST) 
                    userexp = form.save(commit=False)
                    if not form.is_valid():
                        return render(request,'ControlUser/message.html',{'validation':True,
                    'message':"invalide entery"
                    })
                    elif UserExp.objects.filter(title = userexp.title, company_name = userexp.company_name,user = request.user).exists():
                        return render(request,'ControlUser/message.html',{'validation':True,
                    'message':"repeated entery"
                    })
                    elif not userexp.start >userexp.end and userexp.start == userexp.end:
                        return render(request,'ControlUser/message.html',{'validation':True,
                    'message':"you start date must be less than end date"
                    })   
                    userexp.user = request.user
                    userexp.save()
                    return redirect('/user:u/')
                
                if editid :
                    instance = get_object_or_404(UserExp, id=editid)
                    exp_title = instance.title
                    company_name = instance.company_name
                    form = UserexpForm(request.POST,instance = instance)
                    userexp = form.save(commit=False)
                    if exp_title != userexp.title and company_name != userexp.company_name and UserExp.objects.filter(title = userexp.title, company_name = userexp.company_name,user = request.user).exists():
                        return render(request,'ControlUser/message.html',{'validation':True,
                    'message':"This experience is already added"
                    })
                    elif not userexp.start >userexp.end and userexp.start == userexp.end:
                        return render(request,'ControlUser/message.html',{'validation':True,
                    'message':"you start date must be less than end date"
                    })   
                    userexp.save()
                    return redirect('/user:u/')
            form = UserexpForm()
            if editid:
                instance = get_object_or_404(UserExp, id=editid)
                print("expected instance to edit: ",instance)
                form = UserexpForm(instance=instance)
            if deleteid:
                instance = get_object_or_404(UserExp, id=deleteid)
                instance.delete()
                form = False


       
    
        
        if form_name== "userCert": 

            if request.method=='POST': 
                if not editid and not deleteid:          
                    form = UsercertForm(request.POST)
                    cert = form.save(commit=False)
                    cert.user = request.user
                    print("expect cert to save: ",cert)
                    if not form.is_valid():
                        return render(request,'ControlUser/message.html',{'validation':True,'message':"invalide entery"})

                    elif UserCertification.objects.filter(certificate_name = cert.certificate_name,instatution= cert.instatution,user = request.user).exists():
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"repeated entery"
                        })
                    elif not cert.start >cert.end and cert.start == cert.end:
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"you start date must be less than end date"
                        })

                    cert.save()
                    return redirect('/user:u/')
                if editid:
                    instance = get_object_or_404(UserCertification, id=editid)
                    cert_name = instance.certificate_name
                    print(cert_name)
                    instatution = instance.instatution
                    print(instatution)
                    form = UsercertForm(request.POST,instance = instance)
                    print(instance.instatution)
                    print(instance.certificate_name)
                    cert = form.save(commit=False)
                    if cert.certificate_name!=cert_name or cert.instatution != instatution:
                        if UserCertification.objects.filter(certificate_name = cert.certificate_name,instatution= cert.instatution,user = request.user).exists():
                            print("entered in the exists condition")
                            return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"This certification is already added"
                        })
                    elif not cert.start >cert.end and cert.start == cert.end:
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"you start date must be less than end date"
                        })
                    cert.save()
                    return redirect('/user:u/')   


            form = UsercertForm()
            if editid:
                instance = get_object_or_404(UserCertification, id=editid)
                print("expected instance to edit: ",instance)
                form = UsercertForm(instance=instance)

            if deleteid:
                instance = get_object_or_404(UserCertification, id=deleteid)
                instance.delete()
                form = False


  
       
        if form_name== "userProject":   
            if request.method=='POST':
                if not editid and not deleteid:
                    form = UserprojectForm(request.POST)
                    project = form.save(commit=False)
                    project.user = request.user
                    print("expect project to save: ",project)
                    if not form.is_valid():
                        return render(request,'ControlUser/message.html',{'validation':True,'message':"invalide entery"})

                    elif UserProjects.objects.filter(project_name = project.project_name,related_industry= project.related_industry,user = request.user).exists():
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"repeated entery"
                        })
                    elif not project.start >project.end and project.start == project.end:
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"you start date must be less than end date"
                        })

                    project.save()
                    return redirect('/user:u/') 
                if editid:
                    instance = get_object_or_404(UserProjects, id=editid)
                    project_name = instance.project_name
                    related_industry = instance.related_industry
                    form = UserprojectForm(request.POST,instance = instance)
                    project = form.save(commit=False)
                    if project.project_name!=project_name or project.related_industry != related_industry:
                        if UserProjects.objects.filter(project_name = project.project_name,related_industry= project.related_industry,user = request.user).exists():
                            return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"This project is already added"
                        })
                    elif not project.start >project.end and project.start == project.end:
                        return render(request,'ControlUser/message.html',{'validation':True,
                        'message':"you start date must be less than end date"
                        })
                    project.save()
                    return redirect('/user:u/')
            form = UserprojectForm()
            if editid:
                instance = get_object_or_404(UserProjects, id=editid)
                print("expected instance to edit: ",instance)
                form = UserprojectForm(instance=instance)
            if deleteid:
                instance = get_object_or_404(UserProjects, id=deleteid)
                instance.delete()
                form = False
   


    id = request.user.id
    CUprojects = UserProjects.objects.filter(user = request.user)
    CUcerts = UserCertification.objects.filter(user = request.user)
    CUskills = UserSkill.objects.filter(user = request.user)
    CUedu = UserEdu.objects.filter(user = request.user)
    CUexp = UserExp.objects.filter(user = request.user)



    context = {
        'form':form,
        'skills': list(CUskills),
        'projects':CUprojects,
        'certs':CUcerts,
        'edus':CUedu,
        'exps':CUexp,
    }
        


 


    return render(request,'ControlUser/users.html',context=context)




@login_required(login_url="/user:login")
def get_user_publicly(request):
  


    id = request.GET.get("id")
    user = get_object_or_404(User, id=id)
    if not user:
        return HttpResponse("user not found")
    CUprojects = UserProjects.objects.filter(user_id = id)
    CUcerts = UserCertification.objects.filter(user_id = id)
    CUskills = UserSkill.objects.filter(user_id = id)
    CUedu = UserEdu.objects.filter(user_id = id)
    CUexp = UserExp.objects.filter(user_id = id)


    context = {
            'u':user,
        'skills': list(CUskills),
        'projects':CUprojects,
        'certs':CUcerts,
        'edus':CUedu,
        'exps':CUexp,
    }
        


 


    return render(request,'ControlUser/publicusers.html',context=context)



@login_required(login_url="/user:login")
def setuserphoto(request):
      
    if request.method =='POST': 
        print("FILES:", request.FILES)


        if request.user.profile_photo:
            path = os.path.join(settings.BASE_DIR,"media/users",str(request.user.id),'profile.jpg')
            os.remove(path)
            print("deleted old photo at path:",path)

        form = UserPhotoForm(request.POST,request.FILES,instance=request.user)
        if not form.is_valid():
            return render(request,'ControlUser/message.html',{"validation":True,'message':"one of the field is not valid","redirectTo":"/user:setphoto"})
        form.save()
        return redirect('/user:u/')
    form =UserPhotoForm()
    return render(request,"ControlUser/form.html",{"form":form})



@login_required(login_url="/user:login")
def getuserphoto(request):
    id = request.GET.get("id")
    user = get_object_or_404(User,id = id)
    path = Path(Path.joinpath(settings.BASE_DIR,"media/users",F"{id}","profile.jpg"))
    print("photo path:",path.exists())
    if not user.profile_photo:
        path = Path(Path.joinpath(settings.BASE_DIR,"media/users/profile.png"))
        return FileResponse(path.open('rb'),content_type="image")
   
    print(path)
    return FileResponse(path.open('rb'),content_type="image")
    #return HttpResponse("hellow")


@login_required(login_url="/user:login")
def getusercoverphoto(request):
    id = request.GET.get("id")
    user = get_object_or_404(User,id = id)
    path = Path(Path.joinpath(settings.BASE_DIR,"media/users",F"{id}","coverphoto.jpg"))
    print("photo path:",path.exists())
    if not user.cover_photo:
        path = Path(Path.joinpath(settings.BASE_DIR,"media/users/coverphoto.jpg"))
        return FileResponse(path.open('rb'),content_type="image")
   
    print(path)
    return FileResponse(path.open('rb'),content_type="image")
    #return HttpResponse("hellow")


@login_required(login_url="/user:login")
def setusercoverphoto(request):
      
    if request.method =='POST': 
        print("FILES:", request.FILES)


        if request.user.cover_photo:
            path = os.path.join(settings.BASE_DIR,"media/users",str(request.user.id),'coverphoto.jpg')
            os.remove(path)
            print("deleted old photo at path:",path)

        form = UserCoverPhotoForm(request.POST,request.FILES,instance=request.user)
        if not form.is_valid():
            return render(request,'ControlUser/message.html',{"validation":True,'message':"one of the field is not valid","redirectTo":"/user:setphoto"})
        form.save()
        return redirect('/user:u/')
    form =UserCoverPhotoForm()
    return render(request,"ControlUser/form.html",{"form":form})





from django.db.models import Q
@login_required(login_url="/user:login")
def getallusers(request):

    if request.method =='POST':
        search = bool(request.GET.get("s"))
        print(request.POST)
        requestusr = request.POST.get('requestuser')
        
        users = User.objects.filter(Q(full_name__icontains=requestusr)|Q(email__icontains=requestusr)|Q(job_industry__icontains=requestusr)).exclude(id=request.user.id)
        
        print(users)
        print("is search: ",search)
        return render(request,'ControlUser/alluserpage.html',{'users':list(users)})
    allusers = User.objects.all()
    users = allusers.exclude(id=request.user.id)
    
    return render(request,'ControlUser/alluserpage.html',{'users':list(users)})
