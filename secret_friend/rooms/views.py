
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy

from .forms import RoomCreationForm, PasswordForm
from .models import Room, RoomStatus

class RoomDetailView(DetailView):
    model = Room
    template_name = 'game/room.html'
    context_object_name = 'room'

class RoomCreateView(SuccessMessageMixin, CreateView):
    model = Room
    template_name =('game/create_room.html')
    success_url = reverse_lazy('homepage')
    form_class = RoomCreationForm

    def form_valid(self, form):
        # Set the owner of the room to the current user before saving
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

    def post(self, request, *args, **kwargs):
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            room_pk = request.POST['room_id']  # Получаем room_pk из request.POST
            room = Room.objects.get(pk=room_pk)
            if room.is_password_correct(password):
                return redirect(reverse_lazy('RoomDetailView', kwargs={'pk': room_pk}))
        return super().get(request, *args, **kwargs)



class MyRooms(ListView):
    model = Room
    template_name = 'game/my_rooms.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return Room.objects.filter(owner=self.request.user)

def passcheck(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            room_pk = form.cleaned_data['room_id']
            room = Room.objects.get(pk=room_pk)
            if room.is_password_correct(password):
                return redirect(reverse_lazy('rooms:RoomDetailView', kwargs={'pk': room_pk}))
            else:
                # Return an error response if the password is incorrect
                return HttpResponse('Incorrect password', status=400)
        else:
            # Return an error response if the form is not valid
            return HttpResponse('Invalid form data', status=400)
    else:
        # Return an error response if the request method is not 'POST'
        return HttpResponse('Method Not Allowed', status=405)


