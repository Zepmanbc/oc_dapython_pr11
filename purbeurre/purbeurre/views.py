from django.views.generic import TemplateView


class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # kill session 'keep_substitute'. see Issue #2
        if 'keep_substitute' in self.request.session.keys():
            del self.request.session['keep_substitute']
        return context
