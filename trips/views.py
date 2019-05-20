from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template.loader import get_template
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, JsonResponse
from django.db import models
import datetime

from .forms import AddTrip
from .models import Trip, Resort, RoomType, RoomMapping
from . import views


# retun room list of the specified resort
@login_required
def room_list(request):
    if request.is_ajax():
        resort_id = request.GET.get('resort_id', None)
        data = []
        if RoomType.objects.filter(resort_id=resort_id).exists():
            data = list(RoomType.objects.filter(resort_id=resort_id).values())
        return JsonResponse(data, safe=False)


# Create your views here.
@login_required
def trip_list(request):
    # active trips
    trips = Trip.objects.filter(person=request.user).filter(active=True).order_by('checkin')
    trip_cnt = len(Trip.objects.filter(person=request.user))
    return render(request, 'trip_list.html', {'mytrip_list': trips,'trip_cnt':trip_cnt})


@login_required
def trip_list_archive(request):
    # active trips
    trips = Trip.objects.filter(person=request.user).filter(active=False).order_by('checkin')
    trip_cnt = len(Trip.objects.filter(person=request.user))
    return render(request, 'trip_list.html', {'mytrip_list': trips,'trip_cnt':trip_cnt})


@login_required
def trip_new(request):
    if request.method == "POST":
        form = AddTrip(request.POST)
        if form.is_valid():
            Trip = form.save(commit=False)
            Trip.person = request.user
            Trip.save()
            # return HttpResponseRedirect(reverse('trip_list'))
            messages.success(request, 'Your trip was successfully added!')
            return redirect('trips:all')
    else:
        form = AddTrip()
    return render(request, 'trip_new.html', {'form': form})


@login_required
def trip_new2(request):
    if request.method == "POST":
        # form = AddTrip(request.POST)
        # if form.is_valid():
        #     Trip = form.save(commit=False)
        #     Trip.person = request.user
        #     Trip.save()
        #     # return HttpResponseRedirect(reverse('trip_list'))

        # current date and time
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pricevalue = request.POST.get('pricevalue')
        reservationnum = request.POST.get('reservationnum')
        canada = request.POST.get('canada')
        if canada == None:
            canada = False
        else:
            canada = True
        reservationnotes = request.POST.get('reservationnotes')
        not_listed = request.POST.get('not_listed')
        if not_listed == None:
            not_listed = False
        else:
            not_listed = True
        # if checked "not listed", add new resort names other
        if not_listed == True:
            if Resort.objects.filter(name__exact='other').exists():
                resortsnames = Resort.objects.get(name__exact='other').id
            else:
                new_resort = Resort(created_at = now,
                                    modified_at = now,
                                    active = 0,
                                    name = 'other')
                new_resort.save()
                resortsnames = new_resort.id

            # other named room exists already
            if RoomType.objects.filter(name__exact='other').exists():
                roomtype = RoomType.objects.get(name__exact='other').id
            else:
            #     create new roomtype tired of new resort
                new_roomtype = RoomType(created_at = now,
                                        modified_at = now,
                                        active = 0,
                                        name = 'other',
                                        resort_id = resortsnames)
                new_roomtype.save()
                roomtype = new_roomtype.id

            custom_resort = request.POST.get('custom_resort')
            custom_roomtype = request.POST.get('custom_roomtype')
        else:
            resortsnames = request.POST.get('resortsnames')
            roomtype = request.POST.get('roomtype')
            custom_resort = ''
            custom_roomtype = ''

        d = request.POST.get('date').split("/")
        date = d[2]+'-'+d[0]+"-"+d[1]
        check = request.POST.get('checkout').split("/")
        checkout = check[2]+'-'+check[0]+"-"+check[1]
        adults = request.POST.get('adults')
        childrendrplist = int(request.POST.get('childrendrplist'))
        childone = request.POST.get('childone')

        childtwo = request.POST.get('childtwo')
        childthree = request.POST.get('childthree')
        childfour = request.POST.get('childfour')
        if childone == '':
            childone = 0
        if childtwo == '':
            childtwo = 0
        if childthree =='':
            childthree = 0
        if childfour == '':
            childfour = 0

        discount = request.POST.get('discount')
        new_trip = Trip(created_at = now,
                        modified_at = now,
                        active = 1,
                        checkin = date,
                        checkout = checkout,
                        adults = adults,
                        kids = childrendrplist,
                        original_price = int(pricevalue),
                        current_price = int(pricevalue),
                        reservation_number = reservationnum,
                        notes = reservationnotes,
                        discount = discount,
                        person_id = request.user.id,
                        resort_id = resortsnames,
                        roomtype_id = roomtype,
                        canada = canada,
                        kid_1 = childone,
                        kid_2 = childtwo,
                        kid_3 = childthree,
                        kid_4 = childfour,
                        custom_resort = custom_resort,
                        custom_roomtype = custom_roomtype,
                        custom_notmatched = not_listed,)
        new_trip.save()

        messages.success(request, 'Your trip was successfully added!')
        return redirect('trips:all')
    else:
        form = AddTrip()
        resorts = Resort.objects.filter(active__exact=1).values()
        ages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    return render(request, 'trip_new2.html', {'form': form, 'resorts': resorts,'ages':ages})


@login_required
def trip_edit(request, trip_id):
    # TODO
    if request.method == "POST":

        id = request.POST.get('trip_id')

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pricevalue = request.POST.get('pricevalue')
        reservationnum = request.POST.get('reservationnum')
        canada = request.POST.get('canada')
        if canada == None:
            canada = False
        else:
            canada = True
        reservationnotes = request.POST.get('reservationnotes')
        not_listed = request.POST.get('not_listed')
        if not_listed == None:
            not_listed = False
        else:
            not_listed = True

        if not_listed == False:
            custom_resort = ''
            custom_roomtype = ''
            resortsnames = request.POST.get('resortsnames')
            roomtype = request.POST.get('roomtype')
        else:
            custom_resort = request.POST.get('custom_resort')
            custom_roomtype = request.POST.get('custom_roomtype')

            if Resort.objects.filter(name__exact='other').exists():
                resortsnames = Resort.objects.get(name__exact='other').id
            else:
                new_resort = Resort(created_at=now,
                                    modified_at=now,
                                    active=0,
                                    name='other')
                new_resort.save()
                resortsnames = new_resort.id

            # other named room exists already
            if RoomType.objects.filter(name__exact='other').exists():
                roomtype = RoomType.objects.get(name__exact='other').id
            else:
                #     create new roomtype tired of new resort
                new_roomtype = RoomType(created_at=now,
                                        modified_at=now,
                                        active=0,
                                        name='other',
                                        resort_id=resortsnames)
                new_roomtype.save()
                roomtype = new_roomtype.id

        # if user is staff/superuser
        if request.user.is_superuser:

            d = request.POST.get('date').split("/")
            date = d[2]+'-'+d[0]+"-"+d[1]
            check = request.POST.get('checkout').split("/")
            checkout = check[2]+'-'+check[0]+"-"+check[1]
            adults = request.POST.get('adults')
            childrendrplist = int(request.POST.get('childrendrplist'))
            childone = request.POST.get('childone')

            childtwo = request.POST.get('childtwo')
            childthree = request.POST.get('childthree')
            childfour = request.POST.get('childfour')

            if int(childrendrplist) == 0:
                childone = 0
                childtwo = 0
                childthree = 0
                childfour = 0
            elif int(childrendrplist) == 1:
                childtwo = 0
                childthree = 0
                childfour = 0
            elif int(childrendrplist) == 2:
                childthree = 0
                childfour = 0
            elif int(childrendrplist) == 3:
                childfour = 0
            discount = request.POST.get('discount')

        trip = Trip.objects.get(id=id)
        if trip.person_id == request.user.id:

            trip.modified_at = now
            trip.active = 1
            trip.current_price = int(pricevalue)
            trip.reservation_number = reservationnum
            trip.notes = reservationnotes

            # if user is staff/superuser
            if request.user.is_superuser:
                trip.checkin = date
                trip.checkout = checkout
                trip.adults = adults
                trip.kids = childrendrplist
                trip.original_price = int(pricevalue)

                trip.discount = discount
                trip.person_id = request.user.id
                trip.resort_id = resortsnames
                trip.roomtype_id = roomtype
                trip.canada = canada
                trip.kid_1 = childone
                trip.kid_2 = childtwo
                trip.kid_3 = childthree
                trip.kid_4 = childfour
                trip.custom_resort = custom_resort
                trip.custom_roomtype = custom_roomtype
                trip.custom_notmatched = not_listed
            trip.save()
            messages.success(request, 'Your trip was successfully updated !')
        return redirect('trips:all')
    else:
        trip = Trip.objects.get(id=trip_id)
        resorts = Resort.objects.filter(active__exact=1).values()
        roomtypes = RoomType.objects.all()
        ages = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
        checkin = trip.checkin.strftime("%m/%d/%Y")
        checkout = trip.checkout.strftime("%m/%d/%Y")
    return render(request, 'trip_edit2.html',{'trip':trip, 'resorts': resorts, 'roomtypes': roomtypes,'ages':ages,'checkin':checkin,'checkout':checkout})

@login_required
def duplicate(request, trip_id):
    # TODO
    if request.method == "POST":
        id = request.POST.get('trip_id')
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pricevalue = request.POST.get('pricevalue')
        reservationnum = request.POST.get('reservationnum')
        canada = request.POST.get('canada')
        if canada == None:
            canada = False
        else:
            canada = True
        reservationnotes = request.POST.get('reservationnotes')
        not_listed = request.POST.get('not_listed')
        if not_listed == None:
            not_listed = False
        else:
            not_listed = True
        # if checked "not listed", add new resort names other
        if not_listed == True:
            if Resort.objects.filter(name__exact='other').exists():
                resortsnames = Resort.objects.get(name__exact='other').id
            else:
                new_resort = Resort(created_at=now,
                                    modified_at=now,
                                    active=0,
                                    name='other')
                new_resort.save()
                resortsnames = new_resort.id

            # other named room exists already
            if RoomType.objects.filter(name__exact='other').exists():
                roomtype = RoomType.objects.get(name__exact='other').id
            else:
                #     create new roomtype tired of new resort
                new_roomtype = RoomType(created_at=now,
                                        modified_at=now,
                                        active=0,
                                        name='other',
                                        resort_id=resortsnames)
                new_roomtype.save()
                roomtype = new_roomtype.id

            custom_resort = request.POST.get('custom_resort')
            custom_roomtype = request.POST.get('custom_roomtype')
        else:
            resortsnames = request.POST.get('resortsnames')
            roomtype = request.POST.get('roomtype')
            custom_resort = ''
            custom_roomtype = ''

        d = request.POST.get('date').split("/")
        date = d[2]+'-'+d[0]+"-"+d[1]
        check = request.POST.get('checkout').split("/")
        checkout = check[2]+'-'+check[0]+"-"+check[1]
        adults = request.POST.get('adults')
        childrendrplist = int(request.POST.get('childrendrplist'))
        childone = request.POST.get('childone')

        childtwo = request.POST.get('childtwo')
        childthree = request.POST.get('childthree')
        childfour = request.POST.get('childfour')

        if int(childrendrplist) == 0:
            childone = 0
            childtwo = 0
            childthree = 0
            childfour = 0
        elif int(childrendrplist) == 1:
            childtwo = 0
            childthree = 0
            childfour = 0
        elif int(childrendrplist) == 2:
            childthree = 0
            childfour = 0
        elif int(childrendrplist) == 3:
            childfour = 0

        discount = request.POST.get('discount')

        trip = Trip.objects.get(id=id)
        if trip.person_id == request.user.id:
            new_trip = Trip(created_at = now,
                            modified_at = now,
                            active = 1,
                            checkin = date,
                            checkout = checkout,
                            adults = adults,
                            kids = childrendrplist,
                            original_price = int(pricevalue),
                            current_price = int(pricevalue),
                            reservation_number = reservationnum,
                            notes = reservationnotes,
                            discount = discount,
                            person_id = request.user.id,
                            resort_id = resortsnames,
                            roomtype_id = roomtype,
                            canada = canada,
                            kid_1 = childone,
                            kid_2 = childtwo,
                            kid_3 = childthree,
                            kid_4 = childfour,
                            custom_resort = custom_resort,
                            custom_roomtype = custom_roomtype,
                            custom_notmatched = not_listed,)
            new_trip.save()
            messages.success(request, 'Your trip was successfully duplicated !')

        return redirect('trips:all')

    else:

        trip = Trip.objects.get(id=trip_id)
        resorts = Resort.objects.filter(active__exact=1).values()
        roomtypes = RoomType.objects.all()
        ages = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
        checkin = trip.checkin.strftime("%m/%d/%Y")
        checkout = trip.checkout.strftime("%m/%d/%Y")
    return render(request, 'trip_duplicate.html',{'trip':trip, 'resorts': resorts, 'roomtypes': roomtypes,'ages':ages,'checkin':checkin,'checkout':checkout})
@login_required
def archive(request, trip_id):
    # TODO

    trip = Trip.objects.get(id=trip_id)
    if trip.person_id == request.user.id:
        trip.active = 0
        trip.save()
        messages.success(request, 'Your trip was successfully archived !')
    return redirect('trips:all')

@login_required
def restore_trip(request, trip_id):
    # TODO

    trip = Trip.objects.get(id=trip_id)
    if trip.person_id == request.user.id:
        trip.active = 1
        trip.save()
        messages.success(request, 'Your trip was successfully restored !')
    return redirect('trips:all')