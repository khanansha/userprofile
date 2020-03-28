

from django.contrib import admin
from .models import *
from django.contrib.admin import site, ModelAdmin
from django.contrib.admin import DateFieldListFilter
# Register your models here.
from django_admin_listfilter_dropdown.filters import  DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
from django.utils.html import format_html
from django.forms import widgets
from django.contrib.admin import SimpleListFilter
from admin_auto_filters.filters import AutocompleteFilter
import csv
from django.http import HttpResponse
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.admin import ListFilter, FieldListFilter
from django.utils.html import format_html
from django.forms import TextInput, Textarea
from django.db import models
from django import forms
# Register your models here.
class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []

        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)

            output.append(
                f' <a href="{image_url}" target="_blank">'
                f'  <img src="{image_url}" alt="{file_name}" width="150" height="150" '
                f'style="object-fit: cover;"/> </a>')

        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))


class PreferencesInline(admin.TabularInline):
    model = Preferences 
    extra = 1
    can_delete = True
    def has_delete_permission(self, request, obj=None):
        return True
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }
admin.site.register(Registrations)
class ProfileAdmin(admin.ModelAdmin): 
    inlines = [PreferencesInline]

admin.site.register(Profile,ProfileAdmin) 


admin.site.register(OtpVerification) 

