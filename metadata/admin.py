from django.contrib import admin
from .models import (
    District, Gaupalika, Place, Ward, GeoPoint,
    GeoSite, Household,
)

[
    admin.site.register(Model) for Model in
    [
        District, Gaupalika, Place, Ward, GeoPoint,
        GeoSite, Household,
    ]
]
