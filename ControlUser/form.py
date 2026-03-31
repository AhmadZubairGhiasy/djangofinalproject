from django import forms
from django.contrib.auth import get_user_model
from.models import UserSkill,UserEdu,UserExp,UserCertification,UserProjects
from ckeditor.widgets import CKEditorWidget

User = get_user_model()

class UserCreationForm(forms.ModelForm):
    # declear what extract input should the form has
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder':'Enter Password'
        })
    )
    password2 = forms.CharField(
        label="Renter Password",
        widget=forms.PasswordInput(attrs={
            'placeholder':'Confirm Your Password'
        })
    )

   

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = User
        fields = ("email",)

        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



from django.contrib.auth.forms import AuthenticationForm




class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'w-full border-b-2 outline-none'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'w-full border-b-2 outline-none'
        })
    )




class ProfileEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("full_name","employee_title","job_industry","gender","nationality","date_birth","Phone","age",)

        widgets = {
            'date_birth': forms.DateInput(attrs={
                'type':'date',
                'class': 'w-full py-2 px-3 border rounded-md focus:outline-none',
            }),
        }


class UserPhotoForm(forms.ModelForm):
    # declear what extract input should the form has

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = User
        fields = ("profile_photo",)

        widgets = {
            'profile_photo': forms.ClearableFileInput(attrs={
                'id':'img',
                'required':'true'
            })
        }
        

class UserCoverPhotoForm(forms.ModelForm):
    # declear what extract input should the form has

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = User
        fields = ("cover_photo",)
        
        widgets = {
            'cover_photo': forms.ClearableFileInput(attrs={
                'id':'img',
                'required':'true'
            })
        }
        


class UserResumeForm(forms.ModelForm):
    # declear what extract input should the form has

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = User
        fields = ("resume_pdf",)
        widgets = {
            'resume_pdf': forms.ClearableFileInput(attrs={
                'class': 'w-full py-2 px-3 border rounded-md focus:outline-none',
                'required':'true',
                'id':'img',
                'accept':'.pdf'
            })
        }



class UserSkillForm(forms.ModelForm):
    # declear what extract input should the form has

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = UserSkill
        

        fields = ("skill","level",'skill_disc')
        
        labels = {
            'skill_disc':'Skill Description',
        }
        widgets = {
            'skill':forms.Select(attrs={
                'class':'h-[40px] outline-none rounded-xl',
                'required':'true'
            }),
            'level': forms.NumberInput(attrs={
                'class': 'w-full py-2 px-3 border rounded-md focus:outline-none',
                'max':'5',
                "min":"1",
                "value":"1",
            })
        }
      



class UseraboutForm(forms.ModelForm):
    # declear what extract input should the form has

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = User
        fields = ("about",)

        labels = {
            'about':'add your summary',
        }
       
       
        


class UsereduForm(forms.ModelForm):
    # declear what extract input should the form has

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = UserEdu
        

        fields = ["SchoolName","degreelevel",'start','end','school_desc']
        labels = {
            'degreelevel':'Education level',
            'school_desc':'school desciption',
        }    
    
        widgets = {
            'degreelevel':forms.TextInput(attrs={
                'required':'true'
            }),
            'start':forms.DateInput(attrs={
                'type':'date',
                'required':'true'
            }),
            'end':forms.DateInput(attrs={
                'type':'date',
                'required':'true'
            })

        }

    

class UserexpForm(forms.ModelForm):
   
    class Meta:
        model = UserExp
        

        fields = ("title","company_name",'employment_type','location','start','end','exp_desc',)
        
        labels = {
            'exp_desc':'Experiance Description'
            }
        widgets = {
            'title':forms.TextInput(attrs={
                'required':'true'
            }),
            'company_name':forms.TextInput(attrs={
                'required':'true'
            }),
            'employment_type':forms.TextInput(attrs={
                'required':'true'
            }),
            'location':forms.TextInput(attrs={
                'required':'true'
            }),
            'start':forms.DateInput(attrs={
                'type':'date',
                'required':'true'
            }),
            'end':forms.DateInput(attrs={
                'type':'date',
                'required':'true'
            })}
        
       
  

class UsercertForm(forms.ModelForm):
    # declear what extract input should the form has

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = UserCertification
        fields = ("certificate_name","instatution","certificate_link","start","end",'certificate_description')
       
        widgets = {
             'certificate_name':forms.TextInput(attrs={
                'required':'true'
            }),
             'instatution':forms.TextInput(attrs={
                'required':'true'
            }),
            'certificate_link':forms.URLInput(),
            'start':forms.DateInput(attrs={
                'type':'date',
                'required':'true'
            }),
            'end':forms.DateInput(attrs={
                'type':'date',
                'required':'true'
            })

        }
           




class UserprojectForm(forms.ModelForm):
    # declear what extract input should the form has

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = UserProjects
        

        fields = ("project_name","related_industry","start","end",'project_link','project_description')
       
        widgets = {
            'project_name':forms.TextInput(attrs={
                'required':'true'
            }),
            'related_industry':forms.TextInput(attrs={
                'required':'true'
            }),
            'project_link':forms.URLInput(),
            'start':forms.DateInput(attrs={
                'type':'date',
                'required':'true'
            }),
            'end':forms.DateInput(attrs={
                'type':'date',
                'required':'true'
            })

        }
           
