from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import (
    views,
    response,
)
from .serializers import CountrySerializer, DistrictDetailSerializer
from .models import (
    GeoSite, Household,
    District, Gaupalika,
)

from fieldsight.loader import Loader


def get_counts(qs):
    count_list = qs.values('name').annotate(count=models.Count('name'))
    return {
        item['name']: item['count']
        for item in count_list
        if item['name']
    }


class CatPoint:
    def __init__(self, geosite):
        self.geosite = geosite
        self.latitude = geosite.latitude
        self.longitude = geosite.longitude

        self.landslide_code = geosite.code
        self.landslide_cat = geosite.category
        self.gp_name = geosite.gaupalika.name
        self.place = geosite.place

        self.households = geosite.household_set.all()
        self.hh_affected = self.households.count()
        self.risk_score = geosite.risk_score
        self.high_risk_of = geosite.high_risk_of
        self.direct_risk_for = geosite.direct_risk_for
        self.potential_impact = geosite.potential_impact
        self.risk_probability = geosite.risk_probability


class Cat2Point(CatPoint):
    def __init__(self, geosite):
        super().__init__(geosite)
        self.mitigation_work_status = geosite.status
        self.mitigation_work_by = geosite.mitigation_work_by or 'N/A'


class Cat3Point(CatPoint):
    def __init__(self, geosite):
        super().__init__(geosite)
        self.eligible_households = self.households\
            .filter(eligibility__contains='Yes').count()
        self.households_relocated = self.households\
            .filter(result__contains='Relocated').count()


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

    def landslides_risk_score(self):
        return get_counts(
            self.gs.annotate(name=models.F('risk_score')),
        )

    def land_purchased(self):
        return self.hh.aggregate(
            total=models.Sum('land_size')
        )['total'] or 0

    def geohazard_affected(self):
        hh = self.hh.filter(eligibility_source='Geohazard')
        return {
            'Eligible': hh.filter(eligibility__contains='Yes').count(),
            'Relocated': hh.filter(result__contains='Relocated').count(),
            'Total': hh.count(),
        }

    def people_relocated(self):
        hh = self.hh.filter(eligibility_source='Geohazard')
        hh = hh.filter(result__contains='Relocated')
        return {
            'male': hh.aggregate(total=models.Sum(
                models.F('total_male')
            ))['total'] or 0,
            'female': hh.aggregate(total=models.Sum(
                models.F('total_female')
            ))['total'] or 0,
            'children_male': hh.aggregate(total=models.Sum(
                models.F('men_0_5') + models.F('men_6_18')
            ))['total'] or 0,
            'children_female': hh.aggregate(total=models.Sum(
                models.F('women_0_5') + models.F('women_6_18')
            ))['total'] or 0,
            'elderly_male': hh.aggregate(total=models.Sum(
                models.F('men_60_plus')
            ))['total'] or 0,
            'elderly_female': hh.aggregate(total=models.Sum(
                models.F('women_60_plus')
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
        hh = self.hh.filter(eligibility_source='Geohazard')
        hh = hh.filter(result__contains='Relocated')
        return hh.count()

    def cat2_points(self):
        return [
            Cat2Point(gs)
            for gs
            in GeoSite.objects.filter(district=self.district,
                                      category__iexact='cat2')
        ]

    def cat3_points(self):
        return [
            Cat3Point(gs)
            for gs
            in GeoSite.objects.filter(district=self.district,
                                      category__iexact='cat3')
        ]


class MetadataView(views.APIView):
    def get(self, request, district=None):
        loader = Loader()

        try:
            loader.fetch_geosites()
            loader.fetch_households()
        except Exception:
            pass

        if district:
            district = get_object_or_404(District, name__iexact=district)
            metadata = Metadata(district)
            serializer = DistrictDetailSerializer(metadata)
        else:
            metadata = Metadata()
            serializer = CountrySerializer(metadata)
        return response.Response(serializer.data)
