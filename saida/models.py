from django.db import models
from decimal import Decimal
from produto.models import Produtos
from django.core.validators import MinValueValidator

# Create your models here.

class Saidas(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE, verbose_name='Produto')
    quantidade = models.IntegerField('Quantidade', default=0, validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def preco_unitario(self):
        return self.produto.preco

    @property
    def total(self):
        return Decimal(str(self.preco_unitario)) * self.quantidade
