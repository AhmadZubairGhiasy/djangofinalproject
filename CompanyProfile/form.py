from django import forms
from .models import Company_db_model

model = Company_db_model
class company_Creation_Form(forms.ModelForm):

    class Meta:
        model = model
        fields = ('company_name','company_name_abravetion','WEBSITE','Location','company_summary')
       
        widgets = {
            'company_name':forms.TextInput(attrs={
                'placeholder':'Enter your companyname here'
            }),
         
            'company_name_abravetion':forms.TextInput(attrs={
                'placeholder':'Enter your company name abravetion here'
            }),
          
            'WEBSITE':forms.URLInput(attrs={
                'placeholder':'Enter your company website here'
            }),
            'Location':forms.TextInput(attrs={
                'placeholder':'Enter your company location here'
            }),
            'company_summary':forms.Textarea(attrs={
                'placeholder':'Enter your company summary here'
            })
        }



class SetCompanyLogoForm(forms.ModelForm):


    class Meta:
        model = model
        fields = ["Company_logo"]
        labels={
            "Company_logo":"select logo"
        }
        widgets = {
            "Company_logo" :forms.FileInput(attrs={
                "id":"img",
                "accept":".jpg,.png"
            })
        }


class SetCompanycoverForm(forms.ModelForm):


    class Meta:
        model = model
        fields = ["Company_cover_Photo"]
        labels={
            "Company_cover_Photo":"select cover"
        }

        widgets = {
            "Company_cover_Photo" :forms.FileInput(attrs={
                "id":"img",
                "accept":".jpg,.png"
            })
        }


class CompanyBasicDetailsForm(forms.ModelForm):


    class Meta:
        model = Company_db_model
        fields = ('company_name','company_name_abravetion','WEBSITE','Location',)
        widgets = {
            'company_name':forms.TextInput(attrs={
                'placeholder':'Enter your companyname here'
            }),
         
            'company_name_abravetion':forms.TextInput(attrs={
                'placeholder':'Enter your company name abravetion here'
            }),
          
            'WEBSITE':forms.URLInput(attrs={
                'placeholder':'Enter your company website here'
            }),
            'Location':forms.TextInput(attrs={
                'placeholder':'Enter your company location here'
            })
        }


class CompanySummaryForm(forms.ModelForm):


    class Meta:
        model = Company_db_model
        fields = ('company_summary',)