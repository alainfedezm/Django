from django.contrib import admin
from entries.models import Entry
# Register your models here.

#Register Entry db into /admin
admin.site.register(Entry)
