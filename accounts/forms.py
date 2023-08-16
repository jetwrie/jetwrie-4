from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(ProfileForm,self).__init__(*args,**kwargs)

		self.fields['username'].help_text = None
	class Meta:
		model = User
		fields = ['username','first_name','last_name','pictures']



class SignupForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('last_name','first_name','pictures','username','password1','password2')