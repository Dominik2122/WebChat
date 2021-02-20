from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, CreateView
from .models import Chat, Message
from .forms import MessageForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json
from django.forms.models import model_to_dict

User = get_user_model()

class ChatView(DetailView):
    model = Chat
    template_name = 'WebChat/chat_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat'] = self.get_object()
        context['form'] = MessageForm
        return context
    def get(self,request,*args, **kwargs):
        if request.is_ajax():
            messages = self.get_object().messages.all().values()
            print(list(reversed(messages)))
            messages = self.get_object().messages.all().values()
            return JsonResponse({'messages': list(messages)})
        return super().get(request, *args, **kwargs)

def MessageCreate(request, pk):
        if request.is_ajax():
            chat = Chat.objects.filter(pk = int(request.POST.get('chatId'))).first()
            new_message = Message.objects.create(message = request.POST.get('form'), chat = chat, author = request.user)
            new_message.save()
        return HttpResponseRedirect(reverse_lazy('home'))
