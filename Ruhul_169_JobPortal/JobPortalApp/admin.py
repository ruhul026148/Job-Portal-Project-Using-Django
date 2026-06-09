from django.contrib import admin

from JobPortalApp.models import *
# Register your models here.

admin.site.register([UserCustomModel,RecruiterProfileModel,
                     SeekerProfileModel,CategoryModel,
                     JobPostingModel,ApplyingJobModel])
