from django.views.generic import TemplateView, DetailView
from django.contrib.auth import get_user_model
from WebChat.models import Chat, Message
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
User = get_user_model()


class HomePage(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_chats = Chat.objects.filter(members = self.current_user.id) #get all user chats
        user_chats_members = [] #list of users of those chats
        for user_chat in user_chats:
            other_users = list(user_chat.members.all()) #get member of every chat
            for user in other_users:    #loop through members and add their id to list
                user_chats_members.append(user.id)
        other_users = User.objects.exclude(id__in=user_chats_members) #with id of already existing chats, let's create a queryset of users with whom current_user doesnt have a chat
        new_messages = Message.objects.filter(unread = True, chat__in=user_chats)
        new_messages_chats = []
        for new_message in new_messages:
            chat = new_message.chat
            if chat not in new_messages_chats:
                new_messages_chats.append(new_message.chat)
        context['other_users'] = other_users
        context['user_chats'] = user_chats
        context['current_user'] = self.current_user
        context['new_messages_chats'] = new_messages_chats

        return context
    def get(self,request,*args, **kwargs):
        self.current_user = request.user
        return super().get(request, *args, **kwargs)


class SearchView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'WebChat/search_list.html'
    context_object_name = 'chats'
    def get(self,*args, **kwargs):
        request = self.request
        if request.is_ajax():
            search = request.GET.get('search')
            query = search
        if query is not None:
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


        return super().get(request, *args, **kwargs)
