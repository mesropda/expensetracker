from django.contrib import admin
from .models import UserProfile
from .models import Contact
# Register your models here.


admin.site.register(Contact)
admin.site.register(UserProfile)
