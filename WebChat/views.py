from django.views.generic import DetailView
from .models import Chat, Message
from .forms import MessageForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
User = get_user_model()

class ChatView(LoginRequiredMixin, DetailView):
    model = Chat
    def get_template_names(self):
        chat = self.get_object()
        if self.current_user in chat.members.all():
            return ['WebChat/chat_view.html']
        else:
            return ['index.html']
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
            mess = Message.objects.filter(unread = True, chat = self.get_object()).exclude(author=self.current_user)
            for i in mess:
                i.unread = False
                i.save()
            messages = self.get_object().messages.all().values()
            chats = Chat.objects.all().filter(members= self.current_user)
            chats_id = list(chats.values('pk'))
            ids = []
            for id in chats_id:
                ids.append(id['pk'])
            other_messages = Message.objects.filter(chat__pk__in=ids)
            users_id = {x: User.objects.get(id = x).username for x in range(1,1+len(User.objects.all()))} #just a dict of every user + id
            list_of_other_messages = []
            names = {'', ''}
            for message in list(reversed(other_messages)):
                if message.author.username not in names:
                    if message.author.username != self.current_user.username:
                        names.add(message.author.username)
                        not_changed_message = model_to_dict(message)
                        not_changed_message['changed'] = False
                        not_changed_message['prev-author'] = message.author.username
                        list_of_other_messages.append(not_changed_message)
                    else:
                        chat = message.chat
                        for member in chat.members.all():
                            if member.username != message.author.username:
                                name = member.username
                                if name not in names:
                                    names.add(name)
                                    changed_message = model_to_dict(message)
                                    changed_message['author'] = member.pk
                                    changed_message['prev-author'] = message.author.username
                                    changed_message['changed'] = True
                                    list_of_other_messages.append(changed_message)
            return JsonResponse({'messages': list(messages),
                                'current_user_id': request.user.pk,
                                'other_messages':list_of_other_messages,
                                'users_id' : users_id})
        return super().get(request, *args, **kwargs)

@login_required
def MessageCreate(request, pk):
        if request.is_ajax():
            chat = Chat.objects.filter(pk = int(request.POST.get('chatId'))).first()
            new_message = Message.objects.create(message = request.POST.get('form'), chat = chat, author = request.user, unread = True)
            new_message.save()
        return HttpResponseRedirect(reverse_lazy('home'))

@login_required
def ChatCreate(request, pk):
    chat_exist = list(Chat.objects.filter(members = request.user.pk).filter(members = pk))
    print(chat_exist)
    if len(chat_exist)==0:
        new_chat = Chat.objects.create()
        new_chat.members.set(User.objects.filter(id__in=[pk,request.user.id]))
        new_chat.save()
        return HttpResponseRedirect(reverse_lazy('WebChat:chat', kwargs={'pk':new_chat.id}))
    else:
        return HttpResponseRedirect(reverse_lazy('WebChat:chat', kwargs={'pk': chat_exist[0].id}))
