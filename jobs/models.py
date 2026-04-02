import django
from django.db import models
import uuid
from django.utils import timezone
# Create your models here.

from ckeditor.fields import RichTextField



class locationstype(models.Choices):
    REMOTE= 'remote'
    HYBRID= 'hybrid'
    ONSITE= 'onsite'

class catagory(models.Choices):
    IT= 'Information Technology'
    HR= 'HR'
    DESIGN = 'Design'


class job_model(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    jobtitle = models.CharField(max_length=250)
    vocancyCode = models.CharField(max_length=50,blank=True,null=False)
    vocancynum = models.IntegerField(default=0)
   
    job_location_type = models.CharField(choices=locationstype.choices, default=locationstype.ONSITE)
    category = models.CharField(default=catagory.DESIGN, choices=catagory.choices)
    job_address = models.CharField(max_length=250,blank=True)
    createat = models.DateField(auto_now=True)
    closing_date = models.DateField(null=True,blank=True)
    job_descibstion = RichTextField(default="")
    job_summery = RichTextField(default="")
    submision_guide = RichTextField(default="")
    company_name = models.ForeignKey('CompanyProfile.Company_db_model', on_delete=models.CASCADE,null=False,blank=False)
    

    def __str__(self):
        return self.jobtitle
    

class job_application_model(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    job = models.ForeignKey(job_model, on_delete=models.CASCADE,related_name='jobapp')
    applicant = models.ForeignKey('ControlUser.User', on_delete=models.CASCADE,related_name='applicantuser')
        
    
    class Meta:
        unique_together = ('job', 'applicant')  # no duplicate application

    def __str__(self):
        return f"{self.applicant.email} - {self.job.jobtitle}"
    


class saved_job_model(models.Model):
    job = models.ForeignKey(job_model, on_delete=models.CASCADE,related_name='savedjob')
    user = models.ForeignKey('ControlUser.User', on_delete=models.CASCADE,related_name='saveduser')

    class Meta:
        unique_together = ('job', 'user')  # no duplicate saved job

    def __str__(self):
        return f"{self.user.username} - {self.job.jobtitle}"