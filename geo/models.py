from django.db import models


class Map(models.Model):
    key = models.CharField(max_length=128, unique=True)
    default_object = models.CharField(max_length=128,
                                      default=None, blank=True, null=True)
    file = models.FileField(upload_to='maps',
                            default=None, blank=True, null=True)

    def __str__(self):
        return self.key
