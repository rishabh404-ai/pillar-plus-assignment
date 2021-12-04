from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UploadCsv(models.Model):
    csv = models.FileField(upload_to='csv/')
    form_name = models.CharField(max_length=100)
    

class FormDetailsModel(models.Model):
    type_choices = (
        ('Text','Text'),
        ('Single select','Single select'),
        ('Number','Number'),
        ('Date','Date')
    )

    field_name= models.CharField(max_length=100)
    Type= models.CharField(choices=type_choices,max_length=50)
    options= models.CharField(max_length=50,null=True,blank=True)
    mandatory= models.BooleanField()

    def __str__(self):
        return self.field_name
    


class FormModel(models.Model):    
    form_name = models.CharField(_("Name of the Form"), max_length=100)
    form = models.ManyToManyField(FormDetailsModel)  

    class Meta:
        verbose_name = ("form_name_and_details")

