# tracker/forms.py
from django import forms
from .models import Assignment
from django.utils import timezone


class AssignmentCreateForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control form-control-lg'
            }
        ),
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 8,
            'class': 'form-control',
        }),
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required + nice labels
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['deadline'].required = True

        self.fields['title'].label = "Assignment Title"
        self.fields['description'].label = "Description"
        self.fields['deadline'].label = "Deadline"
