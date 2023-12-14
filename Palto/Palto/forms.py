from django import forms

from Palto.Palto import models


# Users


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Objects


class NewAbsenceForm(forms.Form):
    department = forms.ModelChoiceField(queryset=None)
    start = forms.DateTimeField(widget=forms.TextInput(attrs=dict(type='datetime-local')))
    end = forms.DateTimeField(widget=forms.TextInput(attrs=dict(type='datetime-local')))
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, student: models.User, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["department"].queryset = student.studying_departments.all()
