from .serializers import *
from .models import * 
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponseRedirect
from django.apps import apps
from myapp.services.create_google_form import *

# Create your views here.

class UploadFormViewSet(viewsets.ModelViewSet):  
    '''
    API Endpoint to upload a csv and form name to generate a form
    '''

    queryset=  UploadCsv.objects.none()
    serializer_class = UploadFormCsvSerializer   
    form_name = {}

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['csv']
        form_name = serializer.validated_data['form_name'] 
        self.form_name['form_name'] = form_name
        lst_of_field_details = read_csv_and_record_form_template_data(file, form_name)
        form_attrs = generate_form(lst_of_field_details)     
        migrate_and_register_generated_form(form_attrs, form_name)
    
        return HttpResponseRedirect(redirect_to='/google-form')



class GoogleFormAPIViewSet(viewsets.ModelViewSet):
    '''
    Users can only edit/remove/create data entries and not tempalte field names 
    '''    
    
    def get_queryset(self):
        model_name = UploadFormViewSet.form_name['form_name']
        model = apps.get_model('myapp', model_name)   
        return model.objects.all()     

    def get_serializer_class(self):
        model_name = UploadFormViewSet.form_name['form_name']
        model = apps.get_model('myapp', model_name) 
        serializer_class = GeneratedFormModelSerializer
        serializer_class.Meta.model = model
        return serializer_class         


 
          