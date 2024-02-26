from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import PasswordForm, RoomCreationForm, ChatMessageForm, InvitationForm
from .models import Room, RoomStatus, SubChat
from django.db.models import Q


class RoomDetailView(DetailView):
    model = Room
    template_name = 'game/room.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = SubChat.objects.filter(room=self.object).order_by('id')[:10]
        players = self.object.participants.all()
        context['form'] = ChatMessageForm()
        context['form_inv'] = InvitationForm()
        context['messages'] = messages
        context['players'] = players
        return context

    def post(self, request, *args, **kwargs):
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['text']
            sub_chat = SubChat(
                user=request.user,
                room_id=self.kwargs['pk'],
                text=message
            )
            sub_chat.save()
            return redirect(request.path)

        action = request.POST.get('action')
        if action == 'take_participation':
            self.take_participation(request)
        elif action == 'leave_participation':
            self.leave_participation(request)
        elif action == 'send_invitation':
            form_inv = InvitationForm(request.POST)
            if form_inv.is_valid():
                room = self.get_object()
                form_inv.send_invitation_email(room)
                return redirect(request.path)
        return super().get(request, *args, **kwargs)

    def take_participation(self, request):
        room = self.get_object()
        room.take_participation(request)
        return redirect(request.path)

    def leave_participation(self, request):
        room = self.get_object()
        room.leave_participation(request)
        return redirect(request.path)

class RoomCreateView(SuccessMessageMixin, CreateView):
    model = Room
    template_name = ('game/create_room.html')
    success_url = reverse_lazy('homepage')
    form_class = RoomCreationForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = RoomStatus.objects.get(id=1)  # Change 1 to the appropriate default status ID
        form.instance.password = form.cleaned_data['password']  # Set the password
        return super().form_valid(form)


class AllRooms(ListView):
    model = Room
    template_name = 'game/all_rooms.html'
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PasswordForm()
        return context


class MyRooms(ListView):
    model = Room
    template_name = 'game/my_rooms.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return Room.objects.filter(Q(owner=self.request.user) | Q(participants=self.request.user))


def passcheck(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            room_pk = form.cleaned_data['room_id']
            room = Room.objects.get(pk=room_pk)
            if room.is_password_correct(password):
                room.participation(request, password)
                return redirect(reverse_lazy('rooms:RoomDetail', kwargs={'pk': room_pk}))
            else:
                # Return an error response if the password is incorrect
                return HttpResponse('Incorrect password', status=400)
        else:
            # Return an error response if the form is not valid
            return HttpResponse('Invalid form data', status=400)
    else:
        # Return an error response if the request method is not 'POST'
        return HttpResponse('Method Not Allowed', status=405)
