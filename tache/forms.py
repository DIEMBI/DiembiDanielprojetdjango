from django import forms
from .models import Profile
from django import forms
from .models import Project
from django import forms
from .models import Task
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']  
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'assigned_to', 'project']
class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label="passer", widget=forms.PasswordInput)
    password2 = forms.CharField(label="passer", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("passer")
        password2 = self.cleaned_data.get("passer")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2      