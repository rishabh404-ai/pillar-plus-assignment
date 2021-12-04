from rest_framework import serializers
from .models import *

class FormDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDetailsModel
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):    
    class Meta:
        model = FormModel
        fields = '__all__'

class UploadFormCsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadCsv
        fields = '__all__'

class GeneratedFormModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None     
        fields = '__all__'   