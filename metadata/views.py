from django.db import models
from rest_framework import (
    views,
    response,
)
from .serializers import CountrySerializer, DistrictDetailSerializer
from .models import (
    GeoSite, Household,
    District, Gaupalika,
)


def get_counts(qs):
    count_list = qs.values('name').annotate(count=models.Count('name'))
    return {
        item['name']: item['count']
        for item in count_list
        if item['name']
    }


class Metadata:
    # We have not used get_xxx naming specification below
    # so that these attributes will be directly mapped with the serializer
    # fields.
    def __init__(self, district=None, gaupalika=None):
        self.district = district
        self.gaupalika = gaupalika
        self.gs = GeoSite.objects
        self.hh = Household.objects

        if self.gaupalika:
            self.gs = self.gs.filter(gaupalika=gaupalika)
            self.hh = self.hh.filter(gaupalika=gaupalika)
        elif self.district:
            self.gs = self.gs.filter(district=district)
            self.hh = self.hh.filter(district=district)

    def landslides_surveyed(self):
        return get_counts(
            self.gs.annotate(name=models.F('category')),
        )

    def landslides_risk_rating(self):
        return get_counts(
            self.gs.annotate(name=models.F('risk_rating')),
        )

    def land_purchased(self):
        return self.hh.aggregate(
            total=models.Sum('land_size')
        )['total'] or 0

    def geohazard_affected(self):
        hh = self.hh.filter(eligibility_source='Geohazard')
        return {
            'Eligible': hh.filter(eligibility='Yes').count(),
            'Applied': hh.filter(application='Applied').count(),
            'Relocated': hh.filter(result='Relocated').count(),
        }

    def landless(self):
        hh = self.hh.filter(eligibility_source='Landless')
        return {
            'Eligible': hh.filter(eligibility='Yes').count(),
            'Applied': hh.filter(application='Applied').count(),
            'Relocated': hh.filter(result='Relocated').count(),
        }

    def people_relocated(self):
        return {
            'total': self.hh.aggregate(total=models.Sum(
                models.F('total_male') + models.F('total_female')
            ))['total'] or 0,
            'male': self.hh.aggregate(total=models.Sum(
                models.F('total_male')
            ))['total'] or 0,
            'female': self.hh.aggregate(total=models.Sum(
                models.F('total_female')
            ))['total'] or 0,
            'children': self.hh.aggregate(total=models.Sum(
                models.F('men_0_5') + models.F('women_0_5') +
                models.F('men_6_18') + models.F('women_6_18')
            ))['total'] or 0,
            'elderly': self.hh.aggregate(total=models.Sum(
                models.F('men_60_plus') + models.F('women_60_plus')
            ))['total'] or 0,
        }

    def districts(self):
        return [
            Metadata(district) for district in District.objects.all()
        ]

    def gaupalikas(self):
        return [
            Metadata(None, gaupalika)
            for gaupalika
            in Gaupalika.objects.filter(district=self.district)
        ]

    def total_households(self):
        return self.hh.count()


class MetadataView(views.APIView):
    def get(self, request, district=None):
        if district:
            district = District.objects.get(code__iexact=district)
            metadata = Metadata(district)
            serializer = DistrictDetailSerializer(metadata)
        else:
            metadata = Metadata()
            serializer = CountrySerializer(metadata)
        return response.Response(serializer.data)
