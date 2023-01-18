from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

# def index(request):
#     return redirect('/agenda/')


def login_user(request):
    return render(request, 'login.html')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Credenciais (Usuário e/ou Senha) inválidas.")
    return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).order_by('data_evento')
    if not evento.exists():
        dados = {'mensagem': f'{usuario}, não há agendamentos disponíveis para você.'}
        return render(request, 'agenda.html', dados)
    else:
        dados = {'mensagem': f'Olá, {usuario}. Estes são seus agendamentos:', 'eventos': evento, 'usuario': usuario}
        return render(request, 'agenda.html', dados)
@login_required(login_url='/login/')
def evento(request):
    return render(request, 'evento.html')

