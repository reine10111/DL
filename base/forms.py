from django import forms
from .models import Submission, Task, Member, Admin, Announcement, Comment, GroupContrib
# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['user']
        fields = ['profileimg', 'bio', 'email', 'first_name', 'last_name']

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['user']
        fields = ['profileimg', 'bio', 'email', 'first_name', 'last_name']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['proof']


from .models import *

class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add new task...'}))

    class Meta:
        model = Task
        exclude = ['room', 'user']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'body']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']




class GroupContribForm(forms.ModelForm):
    class Meta:
        model = GroupContrib
        exclude = ('assigned', 'room', 'slug')
        fields = ['title', 'amount', 'due', 'selected_user_ids']

        widgets = {
            'selected_user_ids': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
