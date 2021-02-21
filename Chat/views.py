from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from WebChat.models import Chat
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
        context['other_users'] = other_users 
        context['user_chats'] = user_chats
        context['current_user'] = self.current_user

        return context
    def get(self,request,*args, **kwargs):
        self.current_user = request.user
        return super().get(request, *args, **kwargs)
