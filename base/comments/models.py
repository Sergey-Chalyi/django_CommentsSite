from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
import os
import bleach
from lxml import etree
import re


def validate_text_file(value):
    ext = value.name.split('.')[-1].lower()
    if ext != 'txt':
        raise ValidationError('Разрешены только текстовые файлы формата .txt')

    if value.size > 102400:  # 100KB в байтах
        raise ValidationError("Максимальный размер текстового файла не может превышать 100KB")


def validate_image_file(value):
    ext = value.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
        raise ValidationError('Разрешены только изображения форматов JPG, PNG, GIF')

def clean_html(content):
    # Разрешаем только указанные теги
    allowed_tags = ['a', 'code', 'i', 'strong']
    allowed_attrs = {
        'a': ['href', 'title'],  # Разрешаем только href и title для тега <a>
    }

    # Очищаем HTML-код, оставляя только разрешенные теги
    cleaned_content = bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs)

    # Проверка на закрытие тегов и корректность XHTML
    try:
        # Парсим HTML с использованием lxml для проверки его корректности
        tree = etree.fromstring(cleaned_content, parser=etree.XMLParser(recover=True))
        return cleaned_content  # Если HTML валиден, возвращаем очищенный контент
    except etree.XMLSyntaxError as e:
        raise ValidationError(f"Неверный HTML: {str(e)}")  # Если ошибка, выводим ошибку


class Comment(models.Model):
    user_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(validators=[EmailValidator()], null=False)
    text = models.TextField(null=False)  # Поле для хранения очищенного текста

    attachment = models.FileField(
        null=True,
        blank=True
    )

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
        if self.attachment:
            ext = self.attachment.name.split('.')[-1].lower()
            if ext == 'txt':
                validate_text_file(self.attachment)
            else:
                validate_image_file(self.attachment)

        if self.text:
            # Очищаем и валидируем HTML в тексте
            self.text = clean_html(self.text)

    def save(self, *args, **kwargs):
        self.full_clean()  # Запускаем валидацию перед сохранением

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
