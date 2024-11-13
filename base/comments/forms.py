from django import forms

from comments.models import Comment


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_name', 'email', 'text', 'attachment', 'parent_comment']
