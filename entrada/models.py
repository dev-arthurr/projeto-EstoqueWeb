from django.db import models
from produto.models import Produtos
# Create your models here.

class Entradas(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE, verbose_name='Produto')
    preco = models.FloatField('Preco', default=0)
    quantidade = models.IntegerField('Quantidade', default=0)
    criated = models.DateTimeField('Criado em', auto_now_add=True)
    updated = models.DateTimeField('Atualizado em', auto_now=True)