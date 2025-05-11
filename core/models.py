from django.db import models


class AuditTrailModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    created_by = models.CharField(
        max_length=16,
        verbose_name='Created by',
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        blank=True,
        verbose_name='Last modified at',
    )
    modified_by = models.CharField(
        max_length=16,
        verbose_name='Last modified by',
        blank=True,
    )

    class Meta:
        abstract = True
        get_latest_by = '-created_at'


class NoteModel(models.Model):
    note = models.TextField(
        null=True,
        verbose_name='Note')

    class Meta:
        abstract = True
