from django import forms
from .models import CustomUser, CustomUserProfile
from .validators import allow_only_images_validator

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder': 'Masukkan password anda'}))
  confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder': 'Masukkan ulang password anda'}))
  class Meta:
    model = CustomUser
    fields = ['username', 'company_name', 'email', 'password']
    widgets = {
      'username': forms.TextInput(attrs={'placeholder': 'Masukkan username anda'}),
      'company_name': forms.TextInput(attrs={'placeholder': 'Masukkan nama perusahaan anda'}),
      'email': forms.EmailInput(attrs={'placeholder': 'Masukkan email anda'})
    }

  def clean(self):
    cleaned_data = super(UserForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:
      raise forms.ValidationError("Password does not match!")


class UserProfileForm(forms.ModelForm):
  company_prof_pic = forms.FileField(
    widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
    validators=[allow_only_images_validator]
  )
  class Meta:
    model = CustomUserProfile
    fields = ['company_prof_pic', 'company_bio']
