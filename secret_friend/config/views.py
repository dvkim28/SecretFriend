from django.shortcuts import render


def main(request):
    user = request.user
    return render(request, 'game/index.html', {'user': user})