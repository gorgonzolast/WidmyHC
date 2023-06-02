from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^hcs/$', hcs),
    url(r'^hcs/(?P<pk>\w+)/$', hcDetail)
]

