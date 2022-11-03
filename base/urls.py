from django.urls import path
from django.views.generic.base import RedirectView
from .import views


urlpatterns = [
    path('',  RedirectView.as_view(url='settleup/', permanent=False), name='index'),
    path('iou/', views.add_transactions),
    path('add/', views.add_user),
    path('settleup/', views.settle_up),
    
]