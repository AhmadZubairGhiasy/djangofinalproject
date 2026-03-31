from django import forms
from .models import job_model
from ckeditor.widgets import CKEditorWidget
model = job_model

class jobCreationForm(forms.ModelForm):

    # this clase is inherated should be the same name and it declear the model and field to form
    class Meta:
        model = model
       
        fields = (
            "jobtitle",
            "vocancynum",
            "vocancyCode",
            "closing_date",
            "category",
            "job_location_type",
            "job_address",
            "job_summery",
            "job_descibstion",
            "submision_guide",
            )
        widgets = {
            "closing_date": forms.DateInput(attrs={'type': 'date'}),
        }

  
