from django.conf.urls import patterns, url

from reply import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index')
                       )
