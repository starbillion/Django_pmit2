from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# SoftDeletionModel
# https://medium.com/@adriennedomingus/soft-deletion-in-django-e4882581c340



class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)

class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    modified_at = models.DateTimeField(auto_now=True, null=False)
    active = models.BooleanField(default=True)
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()

class Resort(SoftDeletionModel):
    name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=10)
    city = models.CharField(max_length=200)
    picture = models.CharField(max_length=200)
    link = models.URLField()
    # active = models.BooleanField(default=True)
    def __str__(self):
        return self.country_code + ' : ' + self.name

class RoomType(SoftDeletionModel):
    resort = models.ForeignKey('Resort',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField
    # active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.resort.name + ': ' + self.name


class Agency(SoftDeletionModel):
    name = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField
    # active = models.BooleanField(default=True)
    def __str__(self):
        return str(self.order) + ': ' + self.name   

class RoomMapping(SoftDeletionModel):
    resort = models.ForeignKey('Resort', on_delete=models.CASCADE)
    resort_roomtype = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    # active = models.BooleanField(default=True)

class BedTypes (SoftDeletionModel):
    bedtype = models.CharField(max_length=50)

class Trip(SoftDeletionModel):
    reservation_number = models.CharField(max_length=50)
    notes = models.CharField(max_length=500)
    person = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    resort = models.ForeignKey('Resort', on_delete=models.CASCADE)
    roomtype = models.ForeignKey('RoomType', on_delete=models.CASCADE)

    BEDTYPE_CHOICES = (
        ('1king', '1 King Bed'),
        ('2double', '2 Double Beds')
    )
    # bedtype = models.ForeignKey('BedTypes', on_delete=models.CASCADE, null=True)
    bedtype = models.CharField(max_length=50, choices=BEDTYPE_CHOICES)
    checkin = models.DateField()
    checkout = models.DateField()
    adults = models.PositiveSmallIntegerField()
    kids = models.PositiveSmallIntegerField(null=True)
    kid_1 = models.IntegerField (default=0, blank=True)
    kid_2 = models.IntegerField (default=0, blank=True)
    kid_3 = models.IntegerField (default=0, blank=True)
    kid_4 = models.IntegerField (default=0, blank=True)
    original_price = models.IntegerField()  # Set only on initial save (unless full edit to change it)
    current_price = models.IntegerField()  # this is the one they update on edit form
    canada = models.BooleanField(default=False)
    discount = models.SmallIntegerField(default=25, validators=[MaxValueValidator(100), MinValueValidator(0)])
    savings = models.IntegerField(blank=True, null=True)
    kids_ages = models.CharField(max_length=25, null=True)

    # custom_resort and roomtype , flag
    custom_resort = models.CharField(max_length=255)
    custom_roomtype = models.CharField(max_length=255)
    custom_notmatched = models.BooleanField(default=False)
    def __str__(self):
        return str(self.person) + ' ___ ' + str(self.resort) + ': ' + str(self.reservation_number) + ': ' + self.notes  

    def save(self):
        self.savings = (self.original_price) - (self.current_price)
        if self.kids == 0:
            self.kids_ages = ''
        elif self.kids == 1:
            self.kids_ages = str(self.kid_1)
        elif self.kids == 2:
            self.kids_ages = str(self.kid_1) + ', ' + str(self.kid_2)
        elif self.kids == 3:
                self.kids_ages = str(self.kid_1) + ', ' + str(self.kid_2) + ', ' + str(self.kid_3)
        else:
                self.kids_ages = str(self.kid_1) + ', ' + str(self.kid_2) + ', ' + str(self.kid_3) + ', ' + str(self.kid_4)
        super(Trip, self).save()