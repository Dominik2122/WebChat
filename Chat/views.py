from django.views.generic import TemplateView, DetailView
from django.contrib.auth import get_user_model
from WebChat.models import Chat, Message
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
User = get_user_model()


class HomePage(TemplateView):
    template_name = 'index.html'
    def get(self,request,*args, **kwargs):
        if self.request.user.is_authenticated:
            self.current_user = request.user
            if request.is_ajax():
                mess = Message.objects.filter(unread = True).exclude(author=self.current_user).reverse()
                read_mess = Message.objects.all().reverse()
                chat_list = []
                true_chat_list  = []
                for message in mess:
                    chat = message.chat
                    if self.current_user in list(chat.members.all()):
                        if chat.pk not in chat_list:
                            chat_list.append(chat.pk)
                            true_chat_list.append({chat.pk : [message.author.pk, message.message]})
                read_chat_list = []
                read_true_chat_list  = []
                for message in read_mess:
                    chat = message.chat
                    if self.current_user in list(chat.members.all()):
                        if chat.pk not in read_chat_list:
                            read_chat_list.append(chat.pk)
                            if message.author.username == self.current_user.username:
                                new_author = chat.members.all().exclude(id = self.current_user.pk).first()
                                read_true_chat_list.append({chat.pk : [message.author.pk, message.message, new_author.pk]})
                            else:
                                read_true_chat_list.append({chat.pk : [message.author.pk, message.message]})

                users_id = {x: User.objects.get(id = x).username for x in range(1,1+len(User.objects.all()))}

                return JsonResponse({'unreadChats':chat_list, 'usersId' : users_id, 'chat_info':true_chat_list, 'readChats':read_chat_list, 'readChatsinfo': read_true_chat_list})
        else:
            return redirect('accounts:login')
        return super().get(request, *args, **kwargs)


class SearchView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'WebChat/search_list.html'
    context_object_name = 'chats'
    def get(self,*args, **kwargs):
        request = self.request
        search = request.GET.get('search')
        query = search
        if request.is_ajax():
            search = request.GET.get('search')
            query = search
        if query != None:
            search1 = User.objects.filter(username__icontains = query).exclude(username = request.user.username)
            search = list(search1)
            users_chats = Chat.objects.filter(members = request.user.pk).filter(members__in=search)
            list_of_users_and_chats = {}
            existing_chats_userspk = []
            for chat in users_chats:
                member = chat.members.all().exclude(id = request.user.pk).first()
                existing_chats_userspk.append(member.pk)
                list_of_users_and_chats[member.pk] =  chat.pk
            new_users = User.objects.filter(username__icontains = query).exclude(username = request.user.username).exclude(pk__in = existing_chats_userspk)

            return JsonResponse({'all_users': list(search1.values()),
                                'chats': list(users_chats.values()),
                                'chatUserList':list_of_users_and_chats})
        else:
            return HttpResponseRedirect(reverse('home'))

        return super().get(request, *args, **kwargs)
