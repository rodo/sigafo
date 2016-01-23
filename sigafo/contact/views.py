# Create your views here.
from django.views.generic import ListView
from sigafo.utils.view_mixins import ProtectedMixin
from sigafo.contact.models import Contact

class ContactList(ProtectedMixin, ListView):
    model = Contact

    def get_queryset(self):
        try:
            query = self.request.GET['q']
        except:
            query = None

        if query:
            qs = Contact.objects.all()
            contacts = qs.extra(
                where=["lower(unaccent(lastname)) || ' ' || lower(unaccent(firstname)) LIKE %s"],
                params=("%%%s%%" % (query.lower()),))
        else:
            contacts = Contact.objects.all()
        return contacts
