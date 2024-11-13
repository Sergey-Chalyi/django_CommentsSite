from django.core.validators import EmailValidator
from django.db import models

# Create your models here.
class Comment(models.Model):
    user_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(validators=[EmailValidator()], null=False)
    text = models.TextField(null=False)

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user_name} ({self.email})"