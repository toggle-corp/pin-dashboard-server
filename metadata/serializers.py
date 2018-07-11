from rest_framework import serializers
from dashboard.serializers import ListToDictField


class BaseMetadataSerializer(serializers.Serializer):
    landslides_surveyed = serializers.DictField(serializers.IntegerField)
    landslides_risk_rating = serializers.DictField(serializers.IntegerField)

    land_purchased = serializers.FloatField()
    geohazard_affected = serializers.DictField(serializers.IntegerField)
    landless = serializers.DictField(serializers.IntegerField)

    people_relocated = serializers.DictField(serializers.IntegerField)
    total_households = serializers.IntegerField()


class CatPointSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    landslide_code = serializers.CharField()
    landslide_cat = serializers.CharField()
    gp_name = serializers.CharField()

    hh_affected = serializers.IntegerField()
    risk_rating = serializers.CharField()
    high_risk_of = serializers.CharField()
    direct_risk_for = serializers.CharField()
    potential_impact = serializers.CharField()
    risk_probability = serializers.CharField()


class Cat2PointSerializer(CatPointSerializer):
    mitigation_work_status = serializers.CharField()
    mitigation_work_by = serializers.CharField()


class Cat3PointSerializer(CatPointSerializer):
    eligible_households = serializers.IntegerField()
    households_applied = serializers.IntegerField()
    households_relocated = serializers.IntegerField()


class GaupalikaSerializer(BaseMetadataSerializer):
    gaupalika = serializers.CharField(source='gaupalika.code')
    cat2_points = Cat2PointSerializer(many=True)
    cat3_points = Cat3PointSerializer(many=True)


class DistrictDetailSerializer(BaseMetadataSerializer):
    district = serializers.CharField()
    gaupalikas = ListToDictField(
        child=GaupalikaSerializer(many=True),
        key='gaupalika',
    )


class DistrictSerializer(BaseMetadataSerializer):
    district = serializers.CharField(source='district.code')


class CountrySerializer(BaseMetadataSerializer):
    districts = ListToDictField(
        child=DistrictSerializer(many=True),
        key='district',
    )
