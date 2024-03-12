from django import forms

from .models import Room, SubChat


class RoomCreationForm(forms.ModelForm):
    name = forms.CharField(label="Game name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Game name',
    }))
    password = forms.CharField(label="Password", required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))
    invited_emails = forms.CharField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    end_date = forms.DateField(label="End Date", widget=forms.DateInput(
        attrs={
            'type': 'date',  # указываем тип поля date
            'class': 'form-control',  # добавляем класс формы
            'placeholder': 'End Date',  # добавляем placeholder
            'autocomplete': 'off',  # отключаем автозаполнение
        }
    ))

    class Meta:
        model = Room
        fields = ['name', 'password', 'invited_emails']


class PasswordForm(forms.Form):
    password = forms.CharField(label='Password', max_length=10, widget=forms.PasswordInput)
    room_id = forms.CharField(widget=forms.HiddenInput())


class ChatMessageForm(forms.ModelForm):
    text = forms.CharField(label='Type your message...', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control flex-grow-1',
     }))

    class Meta:
        model = SubChat
        fields = ['text']

class InvitationForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address',
    }))

    def send_invitation_email(self, Room):
        recipient_email = self.cleaned_data['email']  # Получаем строку с адресом электронной почты из формы
        Room.send_invitation_email([recipient_email])  # Передаем адрес электронной почты в виде списка с одним элементом
