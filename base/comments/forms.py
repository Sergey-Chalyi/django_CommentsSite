from django import forms
from comments.models import Comment


class AddCommentForm(forms.ModelForm):
    """
    A Django form for adding comments to a website.

    This form is used to collect and validate user input for creating a new Comment instance.
    The form includes fields for user name, email, comment text, attachment, and parent comment.

    Attributes:
    - model: The Django model class representing the Comment.
    - fields: A list of field names included in the form.

    Methods:
    - None (inherits from forms.ModelForm)

    """

    class Meta:
        model = Comment
        fields = ['user_name', 'email', 'text', 'attachment', 'parent_comment']

