from django import forms
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .models import Comments

class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_body']