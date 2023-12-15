from django import forms

from Palto.Palto import models


# Common
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        file_cleaner = super().clean
        if isinstance(data, (list, tuple)):
            return [file_cleaner(d, initial) for d in data]
        else:
            return file_cleaner(data, initial)


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
    attachments = MultipleFileField(required=False)

    def __init__(self, student: models.User, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["department"].queryset = student.studying_departments.all()
