from django.views.generic import ListView

from .models import State, Capital


class StateListView(ListView):
    model = State
    template_name = 'location/home.html'
    context_object_name = 'states'

    def get_queryset(self, **kwargs):
        state_query = self.request.GET.get('state', None)
        capital_query = self.request.GET.get('capital', None)

        if state_query:
            if len(state_query) == 2:
                # Return state matching state abbreviation
                try:
                    queryset = State.objects.filter(abbr=state_query.upper())
                    if queryset:
                        return queryset
                    else:
                        raise AttributeError
                except (AttributeError, IndexError):
                    context = {}
                    context['message'] = 'State not found!'
                    return context
            else:
                # Return state matching state name
                try:
                    queryset = State.objects.filter(
                        name=state_query.replace('_', ' ').title())
                    if queryset:
                        return queryset
                    else:
                        raise AttributeError
                except (AttributeError, IndexError):
                    context = {}
                    context['message'] = 'State not found!'
                    return context
        elif capital_query:
            # Return state matching capital name
            try:
                capital = Capital.objects.filter(
                    name=capital_query.replace('_', ' ').title())
                queryset = State.objects.filter(capital=capital[0])
                if queryset:
                    return queryset
                else:
                    raise AttributeError
            except (AttributeError, IndexError):
                context = {}
                context['message'] = 'Capital not found!'
                return context
        else:
            # Return all states and capitals
            return State.objects.all()
