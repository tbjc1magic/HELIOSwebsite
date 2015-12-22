from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.IndexView, name='index'),
    url(r'^ElementFinder$', views.ElementFinder, name='ElementFinder'),
    url(r'^CalculateCurve$', views.CalculateCurve, name='CalculateCurve'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
