from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# from django.utils.safestring import mark_safe


class RegisterUserForm(UserCreationForm):

    PROFESSION_CHOICES = (
        ("-------", "-------"),
        ("Employee", "Employee"),
        ("Business", "Business"),
        ("Student", "Student"),
        ("Other", "Other")
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form_input_register'}))
    first_name = forms.CharField(max_length=50,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form_input_register'}))
    last_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form_input_register'}))

    profession = forms.ChoiceField(
        choices=PROFESSION_CHOICES, widget=forms.Select(attrs={'placeholder': 'Select', 'class': 'form_input_register'}))

    savings = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': 'Enter Sum', 'class': 'form_input_register'}))
    income = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': 'Enter Sum', 'class': 'form_input_register'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'profession', 'savings', 'income',
                  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form_input_register'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['class'] = 'form_input_register'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form_input_register'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat Password'
