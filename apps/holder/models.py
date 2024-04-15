import uuid

from django.db import models


class AbstractMediaHolder(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = "медиа-файл"
        verbose_name_plural = "медиа-файлы"

    def __str__(self) -> str:
        return self.name


class ImageHolder(AbstractMediaHolder):
    file = models.ImageField(upload_to="files/images/", max_length=500)

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"


class VideoHolder(AbstractMediaHolder):
    file = models.FileField(upload_to="files/videos/", max_length=500)

    class Meta:
        verbose_name = "видео-файл"
        verbose_name_plural = "видео-файлы"

    def __str__(self) -> str:
        return self.name
