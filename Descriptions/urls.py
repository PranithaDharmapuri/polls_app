from django.urls import path
from . import views

app_name="Descriptions"
urlpatterns=[
    path('home/',views.home,name='home'),
    path('details_des/',views.details_des,name="details_des"),
]