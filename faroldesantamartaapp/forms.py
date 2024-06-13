from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, Status, Course, Feedback

class CustomUserChangeForm(UserChangeForm):
    password = None  # Exclude the password field from the form
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'location', 'birth_date')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'bio', 'location', 'birth_date',)
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'teacher', 'students', 'files']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'students': forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = CustomUser.objects.filter(roles__name='Teacher')
        self.fields['students'].queryset = CustomUser.objects.filter(roles__name='Student')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }
