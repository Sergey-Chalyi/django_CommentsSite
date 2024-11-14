from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
import os
import bleach
from lxml import etree
import re


def validate_text_file(value):
    """
    Validates a file to ensure it is a text file (.txt) and does not exceed a maximum size of 100KB.

    Parameters:
    value (File): The file to be validated.

    Raises:
    ValidationError: If the file is not a .txt file or exceeds the maximum size.

    Returns:
    None
    """
    ext = value.name.split('.')[-1].lower()
    if ext != 'txt':
        raise ValidationError('Разрешены только текстовые файлы формата .txt')

    if value.size > 102400:  # 100KB
        raise ValidationError("Максимальный размер текстового файла не может превышать 100KB")


def validate_image_file(value):
    """
    Validates an uploaded file to ensure it is an image file (JPG, JPEG, PNG, GIF) and does not exceed a maximum size.

    Parameters:
    value (File): The file to be validated. The file object must have a 'name' attribute representing the file's name.

    Raises:
    ValidationError: If the file is not an image file or exceeds the maximum size.

    Returns:
    None
    """
    ext = value.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
        raise ValidationError('Разрешены только изображения форматов JPG, PNG, GIF')


def clean_html(content):
    """
    Cleans HTML content by removing unallowed tags and attributes, and checking for properly closed tags.

    Parameters:
    content (str): The HTML content to be cleaned.

    Returns:
    str: The cleaned HTML content. If the content is not valid HTML, a ValidationError is raised.

    Raises:
    ValidationError: If the cleaned HTML content is not valid (i.e., contains improperly closed tags).
    """
    allowed_tags = ['a', 'code', 'i', 'strong']
    allowed_attrs = {
        'a': ['href', 'title'],
    }

    # clear HTML from unhallowed tags
    cleaned_content = bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs)

    # check tags for closing
    try:
        # parse
        tree = etree.fromstring(cleaned_content, parser=etree.XMLParser(recover=True))
        return cleaned_content
    except etree.XMLSyntaxError as e:
        raise ValidationError(f"Неверный HTML: {str(e)}")



class Comment(models.Model):
    """
    A model representing a comment in a comments system.

    Attributes:
    user_name (CharField): The name of the user who made the comment.
    email (EmailField): The email address of the user who made the comment.
    text (TextField): The text content of the comment.
    attachment (FileField): An optional file attachment associated with the comment.
    parent_comment (ForeignKey): A self-referential foreign key representing a parent comment.
    time_created (DateTimeField): The date and time when the comment was created.

    Methods:
    __str__(): Returns a string representation of the comment in the format "{pk}_{user_name}_{email}".
    clean(): Validates and cleans the comment's text and attachment fields.
    save(): Overridden to perform additional operations before saving the comment, such as resizing images.
    """

    user_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(validators=[EmailValidator()], null=False)
    text = models.TextField(null=False)

    attachment = models.FileField(null=True, blank=True)

    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    time_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.pk}_{self.user_name}_{self.email}"


    def clean(self):
        """
        Validates and cleans the comment's text and attachment fields.

        If an attachment is provided, the function checks its extension and calls the appropriate validation function.
        If the text field is not empty, the function calls the clean_html function to sanitize the HTML content.
        """
        if self.attachment:
            ext = self.attachment.name.split('.')[-1].lower()
            if ext == 'txt':
                validate_text_file(self.attachment)
            else:
                validate_image_file(self.attachment)

        if self.text:
            self.text = clean_html(self.text)


    def save(self, *args, **kwargs):
        """
        Overridden to perform additional operations before saving the comment, such as resizing images.

        If an attachment is provided and its extension is one of the image formats (JPG, JPEG, PNG, GIF),
        the function opens the image, resizes it if necessary, and saves it back to the file.
        """
        self.full_clean()

        if self.attachment:
            ext = self.attachment.name.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif']:
                img = Image.open(self.attachment)
                if img.height > 240 or img.width > 320:
                    ratio = min(320 / img.width, 240 / img.height)
                    new_size = (int(img.width * ratio), int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                    img.save(self.attachment.path, quality=95, optimize=True)

        super().save(*args, **kwargs)

