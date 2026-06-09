from django.urls import path
from JobPortalApp.views import *

urlpatterns = [
    path('register-page/',register_page,name='register_page'),
    path('',login_page,name='login_page'),
    path('logout-page/',logout_page,name='logout_page'),


    path('profile-view/',profile_view,name='profile_view'),
    path('update-profile/',update_profile_view,name='update_profile_view'),



    path('browse-post-view/',browse_post_view,name='browse_post_view'),
    path('job-post-view/',job_post_view,name='job_post_view'),
    path('candidate-list/<int:id>/',candidate_list,name='candidate_list'),
    path('update-job-view/<int:id>/',update_job_view,name='update_job_view'),
    path('delete-job-view/<int:id>/',delete_job_view,name='delete_job_view'),


    path('apply-job-view/<int:id>/',apply_job_view,name='apply_job_view'),
    path('my-application',my_application,name='my_application'),


    path('dashboard-page/',dashboard_page,name='dashboard_page'),
]
