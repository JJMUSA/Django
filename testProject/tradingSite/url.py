from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'tradingSite'
urlpatterns =[url(r'^register/$',views.Register.as_view(), name='register'),
              url(r'^homepage/$',views.HomepageView.as_view(), name='homepage'),
              url(r'^commodities/$',views.CommoditiesView.as_view(),name='commodities'),
              url(r'^login/$',views.Login.as_view(), name='login'),
              url(r'^logout/$',views.LogoutView.as_view(), name='logout'),
              url(r'<str:user/portfolio>',views.Portfolio.as_view(), name='portfolio')
              ]