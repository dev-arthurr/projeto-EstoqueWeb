from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Saidas
from .forms import SaidaForm

def list_saida(request):
    saidas = Saidas.objects.all()
    template_name = 'list_saida.html'
    context = {
        'saidas': saidas,
    }

    return render(request, template_name, context)

def new_saida(request):
    template = 'form_saida.html'
    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            saida = form.save(commit=False)

            if not saida.preco_unitario:
                saida.preco_unitario = Decimal(str(saida.produto.preco))

            if saida.quantidade > saida.produto.quantidade:
                form.add_error('quantidade', 'Estoque insuficiente')
            else:
                with transaction.atomic():
                    saida.produto.quantidade -= saida.quantidade
                    saida.produto.save()
                    saida.save()
                return redirect('saida:list_saida')
    else:
        form = SaidaForm()
    return render(request, template, {'form': form})