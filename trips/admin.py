from django.contrib import admin

# Register your models here.
from .models import Resort
from .models import RoomType
from .models import Agency
from .models import RoomMapping
from .models import Trip
from .models import BedTypes



admin.site.register(Resort)
admin.site.register(RoomType)
admin.site.register(Agency)
admin.site.register(BedTypes)
admin.site.register(RoomMapping)
admin.site.register(Trip)
