from django.views.generic import ListView

from .models import State


class StateListView(ListView):
    model = State
    template_name = 'location/home.html'
    context_object_name = 'states'
