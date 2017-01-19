from django.views.generic.edit import FormView

from .forms import MessageForm
from .models import Message


class MessageView(FormView):
    template_name = 'messages.html'
    form_class = MessageForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)

        context['messages'] = Message.objects.order_by('-pk')[:8]

        return context

    def form_valid(self, form):
        form.save()
        return super(MessageView, self).form_valid(form)


message_view = MessageView.as_view()
