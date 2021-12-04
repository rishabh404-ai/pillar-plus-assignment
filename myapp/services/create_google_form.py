from django.db import models
from django.contrib import admin
from django.urls import clear_url_caches
from importlib import import_module
from importlib import reload
from django.conf import settings
from django.core.management import call_command
from django.apps import apps
from django.shortcuts import render
from django.http import HttpResponse
from myapp.serializers import *
from myapp.models import * 
from rest_framework import viewsets, status
from rest_framework.response import Response
import io, csv, pandas as pd
from django.http import HttpResponseRedirect


def read_csv_and_record_form_template_data(file,form_name):
    reader = pd.read_csv(file)
    form_data = FormModel.objects.create(form_name=form_name)
    form_data.save()
    
    lst_of_field_details = []
    for _, row in reader.iterrows():
        if row["type"] == 'Single select':
            options = row['options']
            list_of_options = list(options.split(","))
        else:
            list_of_options = None     

        new_entry = FormDetailsModel(
                    field_name = row['field_name'],
                    Type= row["type"],
                    options= list_of_options,
                    mandatory= row["mandatory"],
                    )
        new_entry.save()           
        form_data.form.add(new_entry) 
            
        form_fields = {}
        form_fields['field_name'] = row['field_name']              
        form_fields['type'] = row['type']
        form_fields['options'] = list_of_options
        form_fields['mandatory'] = row['mandatory']
        lst_of_field_details.append(form_fields)     

    return lst_of_field_details


def generate_form(lst_of_field_details):
    attrs = {'__module__': 'myapp.models'}
    for field in lst_of_field_details:
        if field['type'] == 'Number':
            if field['mandatory'] == True:
                attrs[field['field_name'].lower()] = models.IntegerField()
            else:
                attrs[field['field_name'].lower()] = models.IntegerField(null=True,blank=True)
        elif field['type'] == 'Text':
            if field['mandatory'] == True:
                attrs[field['field_name'].lower()] = models.CharField(max_length=100)
            else:
                attrs[field['field_name'].lower()] = models.CharField(max_length=100,null=True,blank=True)
        elif field['type'] == 'Date':
            if field['mandatory'] == True:
                attrs[field['field_name'].lower()] = models.DateField()
            else:
                attrs[field['field_name'].lower()] = models.DateField(null=True,blank=True)
        elif field['type'] == 'Single select':
            if field['options'] == None:
                pass
            else:             
                set_choices = tuple()
                lst = field['options']
                for value in range(len(lst)):
                    data = (lst[value], lst[value]),
                    set_choices = set_choices + data     

                if field['mandatory'] == True:
                    attrs[field['field_name'].lower()] = models.CharField(choices=set_choices,max_length=50)
                else:
                    attrs[field['field_name'].lower()] = models.CharField(choices=set_choices,max_length=50,null=True,blank=True)    

    return attrs                      



def migrate_and_register_generated_form(attrs,form_name):    
    pillar_plus = type(form_name, (models.Model,), attrs) 
    call_command('makemigrations')
    call_command('migrate')
    admin.site.register(pillar_plus)
    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()
