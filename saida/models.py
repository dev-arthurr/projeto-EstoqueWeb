from django.db import models
from decimal import Decimal
from produto.models import Produtos
from django.core.validators import MinValueValidator
# Create your models here.

class Saidas(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE, verbose_name='Produto')
    preco_unitario = models.DecimalField('Preço unitário', max_digits=10, decimal_places=2,
                                        validators=[MinValueValidator(Decimal('0.00'))],
                                        null=True, blank=True) 
    quantidade = models.IntegerField('Quantidade', default=0, validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        if self.preco_unitario is None:
            return None
        
        return self.preco_unitario * self.quantidade