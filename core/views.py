import django.core.exceptions
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.response import Http404, JsonResponse
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
            messages.error(request, "Credenciais inválidas.")
    return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).order_by('data_evento')
    if not evento.exists():
        dados = {'usuario': usuario,
                 'status': False,  # status serve para ocultar ou expor a tabela no html.
                 'mensagem': f'{usuario}, não há agendamentos disponíveis para você.'}
        return render(request, 'agenda.html', dados)
    else:
        dados = {'status': True, 'eventos': evento, 'usuario': usuario}
        return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {'usuario': request.user}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        dados = {}
        titulo = request.POST.get('titulo')
        local = request.POST.get('local')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        id_evento = request.POST.get('id_evento')
        usuario = request.user
        if id_evento:  # Se for uma edição
            try:
                Evento.objects.filter(id=id_evento)\
                    .update(titulo=titulo,
                            local=local,
                            data_evento=data_evento,
                            descricao=descricao,
                            usuario=usuario)
                return redirect('/')
            except django.core.exceptions.ValidationError:
                dados['error'] = 'Campo obrigatório.'
                dados['evento'] = Evento.objects.get(id=id_evento)
                return render(request, 'evento.html', dados)
        else:  # Se for uma criação.
            try:
                Evento.objects.create(titulo=titulo,
                                      local=local,
                                      data_evento=data_evento,
                                      descricao=descricao,
                                      usuario=usuario)
                return redirect('/')
            except django.core.exceptions.ValidationError:
                dados['error'] = 'Campo obrigatório.'
                dados['evento'] = {"titulo": titulo, "local": local, "descricao": descricao}
                return render(request, 'evento.html', dados)
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def json_api(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values("data_criacao", "data_evento", "descricao",
                                                           "id", "local", "titulo", "usuario", "usuario_id")
    return JsonResponse(list(evento), safe=False)