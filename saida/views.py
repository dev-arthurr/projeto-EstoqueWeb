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

def update_saida(request, pk):
    saida = Saidas.objects.get(pk=pk)
    quantidade = saida.quantidade
    print('==> ', quantidade)

    if request.method == 'POST':
        form = SaidaForm(request.POST, instance=saida)

        if form.is_valid():
            quantidade_nova = form.cleaned_data['quantidade']
            estoque_restaurado = form.cleaned_data['produto'].quantidade + quantidade

            if quantidade_nova > estoque_restaurado:
                form.add_error('quantidade', 'Estoque insuficiente')
                return render(request, 'form_saida.html', {
                    'form': form,
                    'pk': pk
                })
            
            else:
                with transaction.atomic():
                    form.cleaned_data['produto'].quantidade = estoque_restaurado - quantidade_nova
                    form.cleaned_data['produto'].save()
                    form.save()

                return redirect('saida:list_saida')
            
            # print('===>', quantidade, form.cleaned_data['quantidade'])
            # form.save(commit=False)

            # form.cleaned_data['produto'].quantidade = form.cleaned_data['produto'].quantidade \
            # + quantidade - form.cleaned_data['produto'].quantidade
            
            # form.cleaned_data['produto'].save_base()
            # form.save()

            # return redirect('saida:list_saida')
        
    else:
        template_name = 'form_saida.html'
        context = {
            'form': SaidaForm(instance=saida),
            'pk':pk
        }

        return render(request, template_name, context)
    
def delete_saida(request, pk):
    saida = Saidas.objects.get(pk=pk)

    with transaction.atomic():
        saida.produto.quantidade += saida.quantidade
        saida.produto.save()
        saida.delete()

    return redirect('saida:list_saida')
