from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
User = get_user_model()
class HomePage(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_users'] = User.objects.all()
        return context
