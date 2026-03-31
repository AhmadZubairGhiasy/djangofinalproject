from django.db import models
import uuid
from ControlUser.models import User
from ckeditor.fields import RichTextField

def Company_logo_path(instance, filename):
    # instance.id is available AFTER the object is saved
    return f"companies/{instance.id}/company_logo.jpg"

def Company_cover_path(instance, filename):
    # instance.id is available AFTER the object is saved
    return f"companies/{instance.id}/company_cover.jpg"


# Create your models here.
class Company_db_model(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    company_name = models.CharField(max_length=250,blank=True)
    company_name_abravetion = models.CharField(max_length=250,blank=True)
    company_summary = RichTextField(blank=True,null=True)
    create_at = models.DateField( auto_now_add=True)
    Company_logo = models.ImageField(upload_to=Company_logo_path,blank=True)
    Company_cover_Photo = models.ImageField(upload_to=Company_cover_path,blank=True)
    activity_status = models.BooleanField(default=True)
    WEBSITE = models.CharField(blank=True,null=False)
    Location = models.CharField(max_length=250,blank=True)
 
    Owner = models.ForeignKey(
        'ControlUser.User',
        on_delete=models.CASCADE,
        related_name="CompanyProfile",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.company_name
    


