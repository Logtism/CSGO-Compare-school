from django.contrib import admin
from .models import Profile


# Adding the profile model to the django admin page
admin.site.register(Profile)
