from django.db import models


class Project(models.Model):
    key = models.CharField(max_length=128, unique=True)
    last_updated_at = models.IntegerField(
        default=None, null=True, blank=True,
    )

    def __str__(self):
        return self.key
