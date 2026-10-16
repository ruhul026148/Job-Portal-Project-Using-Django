from django import forms
from JobPortalApp.models import *
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):

    class Meta:
        model = UserCustomModel

        fields = [
            'username',
            'email',
            'display_name',
            'user_type',
            'password1',
            'password2',
        ]

        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'display_name': 'Full Name',
            'user_type': 'I want to join as',
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username',
                'autocomplete': 'username',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'autocomplete': 'email',
            }),
            'display_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name',
            }),
        }


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model=RecruiterProfileModel
        fields='__all__'
        exclude=['recruiter']

class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model=SeekerProfileModel
        fields='__all__'
        exclude=['seeker']

class JobPostingForm(forms.ModelForm):
    class Meta:
        model=JobPostingModel
        fields='__all__'
        exclude=['posted_by']
        widgets={
            'deadline':forms.DateInput(attrs={
                'type':'date'
            })
        }

class ApplyingJobForm(forms.ModelForm):
    class Meta:
        model=ApplyingJobModel
        fields='__all__'
        exclude=['applied_by','applied_job']
     