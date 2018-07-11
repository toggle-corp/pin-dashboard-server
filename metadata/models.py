from django.db import models


class District(models.Model):
    code = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Gaupalika(models.Model):
    code = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=256)
    district = models.ForeignKey(District,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Place(models.Model):
    code = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Ward(models.Model):
    code = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class GeoSite(models.Model):
    code = models.CharField(max_length=128, unique=True)

    latitude = models.FloatField(default=None, blank=True, null=True)
    longitude = models.FloatField(default=None, blank=True, null=True)

    district = models.ForeignKey(District,
                                 default=None, blank=True, null=True,
                                 on_delete=models.SET_NULL)
    gaupalika = models.ForeignKey(Gaupalika,
                                  default=None, blank=True, null=True,
                                  on_delete=models.SET_NULL)
    place = models.ForeignKey(Place,
                              default=None, blank=True, null=True,
                              on_delete=models.SET_NULL)
    ward = models.ForeignKey(Ward,
                             default=None, blank=True, null=True,
                             on_delete=models.SET_NULL)

    category = models.CharField(max_length=256, blank=True)
    risk_rating = models.CharField(max_length=256, blank=True)
    high_risk_of = models.CharField(max_length=256, blank=True)
    direct_risk_for = models.CharField(max_length=256, blank=True)
    potential_impact = models.CharField(max_length=256, blank=True)
    probability_of_risk = models.CharField(max_length=256, blank=True)

    mitigation_work_by = models.CharField(max_length=256, blank=True)
    status = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.code


class Household(models.Model):
    code = models.CharField(max_length=128)
    geosite = models.ForeignKey(GeoSite,
                                default=None, blank=True, null=True,
                                on_delete=models.SET_NULL)

    district = models.ForeignKey(District,
                                 default=None, blank=True, null=True,
                                 on_delete=models.SET_NULL)
    gaupalika = models.ForeignKey(Gaupalika,
                                  default=None, blank=True, null=True,
                                  on_delete=models.SET_NULL)
    place = models.ForeignKey(Place,
                              default=None, blank=True, null=True,
                              on_delete=models.SET_NULL)
    ward = models.ForeignKey(Ward,
                             default=None, blank=True, null=True,
                             on_delete=models.SET_NULL)

    land_size = models.FloatField(default=None, blank=True, null=True)
    eligibility_source = models.CharField(max_length=256, blank=True)

    eligibility = models.CharField(max_length=256, blank=True)
    application = models.CharField(max_length=256, blank=True)
    result = models.CharField(max_length=256, blank=True)

    total_male = models.IntegerField(default=None, blank=True, null=True)
    total_female = models.IntegerField(default=None, blank=True, null=True)
    men_0_5 = models.IntegerField(default=None, blank=True, null=True)
    men_6_18 = models.IntegerField(default=None, blank=True, null=True)
    men_19_60 = models.IntegerField(default=None, blank=True, null=True)
    men_60_plus = models.IntegerField(default=None, blank=True, null=True)
    women_0_5 = models.IntegerField(default=None, blank=True, null=True)
    women_6_18 = models.IntegerField(default=None, blank=True, null=True)
    women_19_60 = models.IntegerField(default=None, blank=True, null=True)
    women_60_plus = models.IntegerField(default=None, blank=True, null=True)
    other = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return self.code
