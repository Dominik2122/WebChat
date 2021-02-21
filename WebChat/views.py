from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, CreateView, View
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
        chat = self.get_object()
        context['chat'] = self.get_object()
        context['other_chats'] = Chat.objects.filter(members = self.current_user).exclude(id=chat.pk)
        context['current_user'] = self.current_user
        context['form'] = MessageForm
        return context
    def get(self,request,*args, **kwargs):
        self.current_user = request.user
        if request.is_ajax():
            messages = self.get_object().messages.all().values()
            return JsonResponse({'messages': list(messages),
                                'current_user_id': request.user.pk})
        return super().get(request, *args, **kwargs)


def MessageCreate(request, pk):
        if request.is_ajax():
            chat = Chat.objects.filter(pk = int(request.POST.get('chatId'))).first()
            new_message = Message.objects.create(message = request.POST.get('form'), chat = chat, author = request.user)
            new_message.save()
        return HttpResponseRedirect(reverse_lazy('home'))


def ChatCreate(request, pk):
        new_chat = Chat.objects.create()
        new_chat.members.set(User.objects.filter(id__in=[pk,request.user.id]))
        new_chat.save()
        print(new_chat)
        return HttpResponseRedirect(reverse_lazy('WebChat:chat', kwargs={'pk':new_chat.id}))
