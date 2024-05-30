from django.db import models
from django.utils import timezone

from config import settings


class Chapter(models.Model):
    """
    Chapter class
    """
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(null=True, blank=True, max_length=2000, verbose_name='Description')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update time')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    is_published = models.BooleanField(default=False, verbose_name='Publication Status')
    is_published_requested = models.BooleanField(default=False, verbose_name='Publication request status')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Number of Views')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
        permissions = [
            (
                'set_published',
                'Can publish posts'
            )
        ]


class Material(models.Model):
    """
    Educational material class
    """
    topic = models.CharField(max_length=100, verbose_name='Topic')
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name='Description')
    text = models.TextField(null=True, blank=True, verbose_name='Text')
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update time')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    chapter = models.ForeignKey('education_content.Chapter', on_delete=models.CASCADE)
    is_test_exist = models.BooleanField(default=False, verbose_name='Test exist status')
    is_published = models.BooleanField(default=False, verbose_name='Publication status')
    is_published_requested = models.BooleanField(default=False, verbose_name='Publication request status')
    is_login_required = models.BooleanField(default=True, verbose_name='Login required status')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Number of views')

    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
        permissions = [
            (
                'set_published',
                'Can publish posts'
            )
        ]


class MaterialPhotos(models.Model):
    """
    Material figures
    """
    signature = models.CharField(max_length=300, default='Signature not entered', verbose_name='Signature')
    thin_section = models.ForeignKey('unique_content.FigureThinSection', on_delete=models.CASCADE, default=None,
                                     null=True, blank=True, verbose_name='Thin Section')
    p3din_model = models.ForeignKey('unique_content.FigureFromP3din', on_delete=models.CASCADE, default=None, null=True,
                                    blank=True, verbose_name='Model from p3d.in')
    pano_view = models.ForeignKey('unique_content.Figure360View', on_delete=models.CASCADE, default=None, null=True,
                                  blank=True, verbose_name='360 view')
    map = models.BooleanField(default=False, verbose_name='Map implementation')
    material = models.ForeignKey('education_content.Material', on_delete=models.CASCADE, verbose_name='Material')

    def __str__(self):
        return f'{self.signature}'

    class Meta:
        verbose_name = 'Figure'
        verbose_name_plural = 'Figures'
