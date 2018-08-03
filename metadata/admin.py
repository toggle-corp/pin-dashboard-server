from django.contrib import admin
from .models import (
    District, Gaupalika,
    GeoSite, Household,
)

[
    admin.site.register(Model) for Model in
    [
        District, Gaupalika,
        GeoSite, Household,
    ]
]
