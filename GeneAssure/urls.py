
from django.contrib import admin
from django.urls import path,include
from Geneapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Geneapp.urls')),
    
 
]

from django.conf.urls import handler404
from Geneapp.views import custom_404_view

handler404 = custom_404_view