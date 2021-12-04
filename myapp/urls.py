from django.urls import path
from myapp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('upload-form',views.UploadFormViewSet,basename='upload-form')
router.register('google-form',views.GoogleFormAPIViewSet,basename='google-form')

urlpatterns = [

]+ router.urls
