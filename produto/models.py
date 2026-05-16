from django.db import models

# Create your models here.
class Cores(models.Model):
    cor = models.CharField('Cor', max_length=200)

    def __str__(self):
        return self.cor
    
class Produtos(models.Model):
    produto = models.CharField('Produto', max_length=200)
    cor = models.ForeignKey(Cores, on_delete=models.PROTECT, verbose_name='Cor') #nao deixa deletar cor enquanto houver valores
    descricao = models.TextField('Descricao', blank=True) #blank == vazio
    preco = models.FloatField('Preco', default=0)
    quantidade = models.IntegerField('Quantidade', default=0)
    created = models.DateTimeField('Criado em', auto_now_add=True) #salva a data de criacao
    updated = models.DateTimeField('Atualizado em', auto_now=True) #salva a data de atualizacao

    def __str__(self):
        return self.produto
    
    def precoQuantidade(self):
        return self.preco * self.quantidade
    
    class Meta:
        verbose_name = ('Produto')
        verbose_name_plural = 'Produtos'
        ordering = ['produto']