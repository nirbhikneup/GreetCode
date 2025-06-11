from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code', 'language']  
        widgets = {
            'code': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your code here...'}),
            'language': forms.TextInput(attrs={'placeholder': 'e.g., Python'}),
        }
