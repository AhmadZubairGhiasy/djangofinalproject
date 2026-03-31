from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
import uuid
from django.utils import timezone
from ckeditor.fields import RichTextField

class usermanager(BaseUserManager):
    def create_user(self,email,password=None,**extra_field):
        if not email: raise ValueError("user should have an email")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_field):
        extra_field.setdefault('is_staff',True)
        extra_field.setdefault('is_superuser',True)
        extra_field.setdefault('is_active', True)

        if not extra_field.get("is_staff"): raise ValueError("Super user must have is_staff=True")
        return self.create_user(email,password,**extra_field)



# extro functionalities ------
def user_image_path(instance, filename):
    # instance.id is available AFTER the object is saved
    return f"users/{instance.id}/profile.jpg"

def user_cover_path(instance, filename):
    # instance.id is available AFTER the object is saved
    return f"users/{instance.id}/coverphoto.jpg"

def user_pdf_path(instance, filename):
    # instance.id is available AFTER the object is saved
    return f"users/{instance.id}/resume.pdf"

class genderchoise(models.Choices):
    MALE = 'male'
    FEMALE = 'female'




class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=250, blank=True,null=True)
    employee_title = models.CharField(max_length=250, blank=True)
    job_industry = models.CharField(max_length=250, blank=True,null=True)
    about = RichTextField(blank=True,null=True)
    gender = models.CharField(max_length=50,default=genderchoise.MALE, choices=genderchoise.choices)
    nationality = models.CharField(max_length=50,default='afghan')
    date_birth = models.DateField(blank=True,null=True)
    Phone = models.CharField(max_length=50,blank=True,null=True)
    age = models.PositiveIntegerField(null=True, blank = True)
    profile_photo = models.ImageField(upload_to=user_image_path,null=True,blank=True)
    cover_photo = models.ImageField(upload_to=user_cover_path,null=True,blank=True)
    resume_pdf = models.FileField(upload_to=user_pdf_path,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    create_At = models.DateField(auto_now=False, auto_now_add=False,default=timezone.now)

    objects = usermanager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    def __str__(self):
        return self.email




class Skill(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50,unique=True,blank=False,null=False)
    def __str__(self):
        return self.name
    


class UserSkill(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE,related_name="userskills",blank=True,null=True)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE,related_name="skillforuser",blank=True,null=True)
    level = models.CharField(max_length=20, blank=True)
    skill_disc = RichTextField(blank=True,null=True)

    class Meta:
        unique_together = ('user', 'skill')  # no duplicate assignment

    def __str__(self):
        return f"{self.user} - {self.skill}"


User.add_to_class(
    'Skill',
    models.ManyToManyField(
        Skill,
        through=UserSkill,
        related_name='usersskilssuniqe'
    )
)



class UserProjects(models.Model):
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='projectuser')
    project_name = models.CharField(max_length=50,blank=False,null=False)
    project_description = RichTextField(blank=True,null=True)
    create_at = models.DateField(auto_now=False, auto_now_add=False,default=timezone.now)
    project_link = models.CharField(max_length=250,blank=True,null=True)
    related_industry = models.CharField(max_length=50,blank=True,null=True)
    start = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    end = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)

    class Meta:
        unique_together = ('user', 'project_name','related_industry')

    def __str__(self):
        return self.project_name
  



class UserCertification(models.Model):
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Ceruser')
    certificate_name = models.CharField(max_length=50,blank=False,null=False)
    certificate_description = RichTextField(blank=True,null=True)
    create_at = models.DateField(auto_now=False, auto_now_add=False,default=timezone.now)
    certificate_link = models.CharField(max_length=250,blank=True,null=True)
   
    instatution = models.CharField(max_length=50,blank=True,null=True)
    start = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    end = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)

    class Meta:
        unique_together = ('user', 'certificate_name','instatution') 
    def __str__(self):
        return self.certificate_name
  


 
class UserEdu(models.Model):
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='eduuser')
    SchoolName = models.CharField(max_length=50,blank=False,null=False)
    degreelevel = models.CharField(max_length=50,blank=True,null=True)
    start = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    end = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    school_desc = RichTextField(blank=True,null=True)


    class Meta:
        unique_together = ('user', 'SchoolName','degreelevel')  # no duplicate assignment

    def __str__(self):
        return self.SchoolName
  


 
class UserExp(models.Model):
    id = models.UUIDField(primary_key=True,unique=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='expser')
    title = models.CharField(max_length=50,blank=False,null=False)
    employment_type = models.CharField(max_length=50,blank=True,null=True)
    company_name =models.CharField(max_length=50,blank=True,null=True)
    location = models.CharField(max_length=250,blank=True,null=True)
    start = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    end = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    exp_desc = RichTextField(blank=True,null=True)

    class Meta:
        unique_together = ('user', 'title','company_name','location')

    def __str__(self):
        return f"{self.title} in  {self.company_name}"
  


