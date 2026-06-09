from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from JobPortalApp.models import *
from JobPortalApp.forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def register_page(request):
    if request.method=='POST':
        form_data=RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,'Registration SuccessFully')
            return redirect('login_page')
            

    form_data=RegisterForm()
    context={
        'form_data':form_data,
        'form_title':'User Register Form',
        'form_btn':'Register',
        'title':'Registration Page',
    }
    return render(request,'master/base-form.html',context)

def login_page(request):
    if request.method=='POST':
        form_data=AuthenticationForm(request,request.POST)
        if form_data.is_valid():
            user=form_data.get_user()
            if user:
                login(request,user)
                messages.success(request,'Login SuccessFully')
                return redirect('dashboard_page')
        messages.success(request,'Invalid Crendentails')

    form_data=AuthenticationForm()
    context={
        'form_data':form_data,
        'form_title':'User Login Form',
        'form_btn':'Login',
        'title':'Login Page',
    }
    return render(request,'master/base-form.html',context)

@login_required
def logout_page(request):
    logout(request)
    messages.success(request,'Logout SuccessFully')
    return redirect('login_page')

@login_required
def dashboard_page(request):
    try:
        seeker_profile=request.user.seeker_profile
    except:
        messages.error(request,'Please Update Your Profile First')
        return redirect('update_profile_view')
    
    if request.user.user_type == 'Seeker':
        seeker_skills=request.user.seeker_profile.skill_set
        job_data=JobPostingModel.objects.none()

        for skill in seeker_skills.split(','):
            clear_skill=skill.strip()
            job_data |=JobPostingModel.objects.filter(skill_set__icontains=clear_skill)

    context={
        'job_data':job_data
    }


    return render(request,'Dashboard.html',context)

@login_required
def profile_view(request):
    return render(request,'profile.html')

@login_required
def update_profile_view(request):
    current_user=request.user
    if current_user.user_type=='Recruiter':
        try:
            profile_data=RecruiterProfileModel.objects.get(recruiter=current_user)
        except RecruiterProfileModel.DoesNotExist:
            profile_data=None

        if request.method=="POST":
            form_data=RecruiterProfileForm(request.POST,request.FILES,instance=profile_data)
            if form_data.is_valid():
                data=form_data.save(commit=False)
                data.recruiter=current_user
                data.save()
                messages.success(request,'Update Profile SuccessFully')
                return redirect('profile_view')

        form_data=RecruiterProfileForm(instance=profile_data)
    else:
        try:
            profile_data=SeekerProfileModel.objects.get(seeker=current_user)
        except SeekerProfileModel.DoesNotExist:
            profile_data=None

        if request.method=="POST":
            form_data=SeekerProfileForm(request.POST,request.FILES, instance=profile_data)
            if form_data.is_valid():
                data=form_data.save(commit=False)
                data.seeker=current_user
                data.save()
                messages.success(request,'Update Profile SuccessFully')
                return redirect('profile_view')

        form_data=SeekerProfileForm(instance=profile_data)

    context={
        'form_data':form_data,
        'form_title':'User Profile Update Form',
        'form_btn':'Update',
        'title':'Profile Page',
    }
    return render(request,'master/base-form.html',context)


def browse_post_view(request):


    current_user = request.user
    
    search_query=request.GET.get("search_query")

    
    # Login kora user
    if current_user.is_authenticated:

        # Recruiter hole
        if current_user.user_type == 'Recruiter':

            recruiter_profile = getattr(
                current_user,
                'recruiter_profile',
                None
            )

            # profile thakle tar nijer post
            if recruiter_profile:

                job_data = JobPostingModel.objects.filter(
                    posted_by=recruiter_profile
                )

            # profile na thakle empty data
            else:
                job_data = JobPostingModel.objects.none()

        # Normal user hole
        else:
            job_data = JobPostingModel.objects.all()

    # Login na kora visitor
    else:
        job_data = JobPostingModel.objects.all()

    if search_query:
        job_data=JobPostingModel.objects.filter(
            Q(title__icontains=search_query) |
            Q(Category__name__icontains=search_query) |
            Q(posted_by__company_name__icontains=search_query)
        )
        

    context = {
        'job_data': job_data
    }

    return render(request, 'browse-jobs.html', context)

@login_required
def job_post_view(request):
    try:
        recruiter_data=request.user.recruiter_profile
    except:
        messages.error(request,'Please Update Your Profile First')
        return redirect('update_profile_view')
    if request.method=='POST':
        form_data=JobPostingForm(request.POST)
        if form_data.is_valid():
            data=form_data.save(commit=False)
            data.posted_by=recruiter_data
            data.save()
            messages.success(request,'Job Post SuccessFully')
            return redirect('browse_post_view')


    form_data=JobPostingForm()

    context={
        'form_data':form_data,
        'form_title':'Job Posting Info Form',
        'form_btn':'Add Post',
        'title':'Job Posting Page',
    }
    return render(request,'master/base-form.html',context)

@login_required
def update_job_view(request,id):
    recruiter_data=request.user.recruiter_profile
    try:
        job_data=JobPostingModel.objects.get(id=id)
    except:
        messages.error(request, 'Please, Update your profile first.')
        return redirect('update_profile_view') 
    if request.method == "POST":
            form_data=JobPostingForm(request.POST,request.FILES,instance=job_data)
            if form_data.is_valid():
                data=form_data.save(commit=False)
                data.posted_by=recruiter_data
                data.save()
                messages.success(request,'Job Update SuccessFully')
                return redirect('browse_post_view')  
           
    form_data=JobPostingForm(instance=job_data)

    context={
        'form_data':form_data,
        'form_title':'Job Updating Info Form',
        'form_btn':'Update',
        'title':'Job Updating Page',
    }
    return render(request,'master/base-form.html',context)

@login_required
def delete_job_view(request,id):
        try:
            JobPostingModel.objects.get(id=id).delete()
            messages.success(request,'Job delete SuccessFully') 
            return redirect('browse_post_view')
        except:
            messages.error(request,'Job Not Found') 
            return redirect('browse_post_view')

@login_required
def apply_job_view(request, id):
    try:
        seeker_profile=request.user.seeker_profile
        job= JobPostingModel.objects.get(id=id)
    except:
        messages.error(request, 'Please, Update your profile first.')
        return redirect('update_profile_view') 


    if request.method == "POST":
        form_data=ApplyingJobForm(request.POST, request.FILES)
        if form_data.is_valid():
            data=form_data.save(commit=False)
            data.applied_by=seeker_profile
            data.applied_job=job
            data.save()
            messages.success(request,'Job Applied SuccessFully') 
            return redirect('browse_post_view')


    form_data=ApplyingJobForm()
    context={
        'form_data':form_data,
        'form_title':'Job Apply Info Form',
        'form_btn':'Apply',
        'title':'Job Apply Page',
    }
    return render(request,'master/base-form.html',context)

def my_application(request):
    my_application=ApplyingJobModel.objects.filter(applied_by= request.user.seeker_profile)
    context={
        'application_list':my_application,
        'title':'My Job Applylication Page',

        
    }
    return render(request,'my-application.html',context)

def candidate_list(request,id):
    job_data=JobPostingModel.objects.get(id=id)
    candidate_data=ApplyingJobModel.objects.filter(applied_job=job_data)
    context={
        'candidate_data':candidate_data,
        'job_data':job_data,
        'title':'Candidate List Page'

    }
    return render(request,'candidate-list.html',context)





 
    















