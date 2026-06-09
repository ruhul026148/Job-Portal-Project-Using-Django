from django.db import models
from django.contrib.auth.models import AbstractUser

# Username, Display name, Email, Password, Confirm Password, User type
class UserCustomModel(AbstractUser):
    USER_TYPE=[
        ('Recruiter','Recruiter'),
        ('Seeker','Seeker')
    ]
    display_name=models.CharField(max_length=100,null=True)
    user_type=models.CharField(choices=USER_TYPE,max_length=20,null=True)

    def __str__(self):
        return f'{self.username}-{self.user_type}'
    
#  Recruiters (Company information) 
#  Jobseekers (Skills set and resume upload option) 

class RecruiterProfileModel(models.Model):
    recruiter=models.OneToOneField(UserCustomModel,on_delete=models.CASCADE,
                                   related_name='recruiter_profile',null=True)
    company_name=models.CharField(max_length=100, null=True)
    address=models.TextField(null=True)
    contact=models.CharField(max_length=20,null=True)
    logo=models.ImageField(upload_to='company_logo',null=True)

    created_at=models.DateField(auto_now_add=True,null=True)
    updated_at=models.DateField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.recruiter}'
    
class SeekerProfileModel(models.Model):
    seeker=models.OneToOneField(UserCustomModel,on_delete=models.CASCADE,
                                   related_name='seeker_profile',null=True)
    address=models.TextField(null=True)
    contact=models.CharField(max_length=20,null=True)
    profile_image=models.ImageField(upload_to='seeker_image',null=True)
    skill_set=models.TextField(null=True)

    created_at=models.DateField(auto_now_add=True,null=True)
    updated_at=models.DateField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.seeker}'
    
class CategoryModel(models.Model):
    name=models.CharField(max_length=100,null=True)

    def __str__(self):
        return f'{self.name}'
    
# Develop a job posting page for recruiters (Title, Number of openings, Category,Job description, Skills set) 

class JobPostingModel(models.Model):
    posted_by=models.ForeignKey(RecruiterProfileModel,on_delete=models.CASCADE,
                                related_name='posted_job',null=True)
    Category=models.ForeignKey(CategoryModel,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=100,null=True)
    number_of_openings=models.PositiveIntegerField(null=True)
    description=models.TextField(null=True)
    skill_set=models.TextField(null=True)
    deadline=models.DateField(null=True)
    salary=models.FloatField(null=True)

    created_at=models.DateField(auto_now_add=True,null=True)
    updated_at=models.DateField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.title}'
    
class ApplyingJobModel(models.Model):
    applied_by=models.ForeignKey(SeekerProfileModel,on_delete=models.CASCADE,
                                related_name='applied_info',null=True)
    applied_job=models.ForeignKey(JobPostingModel,on_delete=models.CASCADE,
                                related_name='applied_job',null=True)
    
    resume=models.FileField(upload_to='seeker_resume',null=True)
    applied_at=models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return f'{self.applied_by}-{self.applied_job}'

    

