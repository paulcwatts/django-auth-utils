from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from utils import email_to_username

class RegistrationForm(forms.Form):
    """
    Our form for registering a new account.
    This uses the user's email as their credentials.
    """
    error_css_class = 'error'
    required_css_class = 'required'

    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Repeat password"))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please use a different email address."))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verify that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    def create_user(self):
        if self.errors:
            raise forms.ValidationError("Unable to create user "
                                        "because the data is invalid")
        email = self.cleaned_data['email']
        username = email_to_username(email)
        password = self.cleaned_data['password1']
        return User.objects.create_user(username, email, password)

