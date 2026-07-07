from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь войдите в аккаунт.')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте данные.')

    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})
