from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.TopPageView.as_view(), name='Top')
]