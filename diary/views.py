from django.shortcuts import render
from django.views import generic

# Create your views here.


class TopPageView(generic.TemplateView):

    template_name = 'diary/top_page.html'
