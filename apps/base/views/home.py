from django.views.generic import DeleteView, DetailView, ListView, TemplateView

class Home(TemplateView):
    template_name = "home.html"

