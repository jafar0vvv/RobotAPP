from django.urls import path
from .views import FormView,SorgulamaView

urlpatterns = [
    path('sorgulama/', FormView.as_view(), name='form'),
    path('sorgulama/sonuclari', SorgulamaView.as_view(), name='sorgulama'),
]