from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework_swagger import renderers
from .import api

router = routers.DefaultRouter()
router.register(r'api2', api.ApiViewset, base_name='apiimages')

app_name = 'home'
urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^whiteflycount/$', views.whiteflycount, name='whiteflycount'),
#     url(r'^signup/$', views.signup, name='signup'),
#     url(r'^login/$', views.userlogin, name='login'),
#     url(r'^logout/$', views.userlogout, name='logout'),
#     url(r'^upload/$', views.uploadimage, name='upload'),
#     url(r'^downloadcsv/$', views.downloadcsv, name='downloadcsv'),
#     url(r'^downloadzippedfile/$', views.downloadzippedfolder, name='downloadzippedfile'),
    url(r'^api/$', api.upload_image, name='uploadapi'),
]
urlpatterns += router.urls
