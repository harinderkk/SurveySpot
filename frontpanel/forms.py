from django import forms
from frontpanel.models import RoleDetails

class RoleDetailsForm(forms.ModelForm):
	class Meta:  #insert data to individual columns
		model = RoleDetails
		exclude = ['role','name', 'email', 'password','mobile', 'address', 'gender','active','otp','otp_time',
		'verify_link','login_time', 'image']
