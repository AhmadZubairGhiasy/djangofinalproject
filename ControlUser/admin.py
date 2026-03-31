from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Skill,UserSkill,UserProjects,UserCertification,UserEdu,UserExp

# Register your models here.
class customeuseradmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'age', 'profile_photo','resume_pdf','Phone','date_birth','about','job_industry','cover_photo')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email' , 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email',)


admin.site.register(User,customeuseradmin)

admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(UserProjects)
admin.site.register(UserCertification)
admin.site.register(UserEdu)
admin.site.register(UserExp)