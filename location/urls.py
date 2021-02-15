from django.urls import path
from .views import StateListView

urlpatterns = [
    path('', StateListView.as_view(), name='states'),
]
