# Create your views here.
from django.views.generic.base import TemplateView

class HomepageView(TemplateView):
    template_name = "home.html"
