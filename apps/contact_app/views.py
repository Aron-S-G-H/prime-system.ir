from django.views.generic import TemplateView
from .forms import ContactUsForm
from django.http import JsonResponse
from .models import ContactUs


class ContactUsView(TemplateView):
    template_name = 'contact_app/contact-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactUsForm()
        return context

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ContactUs.objects.create(user=request.user, message=data['message'])
            return JsonResponse({'status': 200})
        else:
            return JsonResponse({'status': 400, 'error_message': form.errors['message']})

