""" view-классы приложения about """

from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """ страница 'об авторе' """
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """ страница 'технологии' """
    template_name = 'about/tech.html'
