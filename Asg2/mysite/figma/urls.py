from django.urls import path

from . import views

app_name = 'figma' # name spacing the URL's
urlpatterns = [
    path('', views.home, name='home'),
]