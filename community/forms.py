# community/forms.py
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'location', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class PostEditForm(forms.ModelForm):
    new_media = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'multiple': False}),
        label='Add more media'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'location', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'tags': forms.TextInput(attrs={'placeholder': 'comma,separated,tags'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

from django import forms
from .models import Pledge, Idea, Feedback

class PledgeForm(forms.ModelForm):
    class Meta:
        model = Pledge
        fields = "__all__" 

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = "__all__" 

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__" 

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })