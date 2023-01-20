from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(verbose_name='Data de Criação', auto_now=True)  # Insere a data atual para o banco de dados.
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    local = models.CharField(max_length=70, null=True)
    class Meta:
        db_table = 'evento'

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M Hrs')

    def get_date_input(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    def get_evento_atrasado(self):

        if self.data_evento < datetime.now() - timedelta(hours=1):
            return True
        else:
            return False

    def __str__(self):
        return self.titulo


