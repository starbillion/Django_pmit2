from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'trips'
urlpatterns = [
    path('', views.trip_list, name='all'),
    path('new/', views.trip_new, name='new_trip'),  # duplicate is also new with values filled in
    path('new2/', views.trip_new2, name='new_trip2'),  # duplicate is also new with values filled in

    url(r'^edit_trip/(?P<trip_id>\d+)/$', views.trip_edit, name='edit_trip'),
    url(r'^duplicate/(?P<trip_id>\d+)/$', views.duplicate, name='duplicate'),
    url(r'^archive/(?P<trip_id>\d+)/$', views.archive, name='archive'),
    url(r'^restore_trip/(?P<trip_id>\d+)/$', views.restore_trip, name='restore_trip'),
    # edit needs to handle current_amount, reservation number, notes ONLY
    path('edit/full', views.trip_edit, name='fulledit_trip'),
    # allow everything to be changed.  Must handle cases where something not active anymore
    path('archive/', views.trip_list_archive, name='archive_trip'),
    # this should just be the archive call, select the tab, and show archived

    # return the room types of the specified resort
    url(r'^rooms/', views.room_list, name='rooms'),
]
