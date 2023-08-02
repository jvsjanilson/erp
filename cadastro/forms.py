from django import forms
from cadastro.models import Produto, Unidade, Marca, Categoria, Contato
from core.forms import *


class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ['codigo', 'nome']
        widgets = {
            'codigo': TextInputBootstrap(),
            'nome': TextInputBootstrap(),
        }



class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome']
        widgets = {
            'nome': TextInputBootstrap(),
        }



class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [ 'nome']
        widgets = {
            'nome': TextInputBootstrap(),
        }



class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        # help_texts = {
        #     'codigo': 'Codigo do produto 13 caracteres',
        # }
        widgets = {
            'codigo': TextInputBootstrap(),
            'nome': TextInputBootstrap(),
            'unidade': SelectBootstrap(),
            'marca': SelectBootstrap(),
            'categoria': SelectBootstrap(),
            'preco_compra': NumberInputBootstap(),
            'preco_venda': NumberInputBootstap(),
            'estoque': NumberInputBootstap(),
            'ativo': CheckboxInputBootstrap(),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['codigo'].required = False


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = '__all__'
        widgets = {
            'razao_social': TextInputBootstrap(),
            'nome_fantasia': TextInputBootstrap(),
            'cpf_cnpj': TextInputBootstrap(),
            'inscricao_estadual': TextInputBootstrap(),
            'inscricao_municipal': TextInputBootstrap(),
            'inscricao_suframa': TextInputBootstrap(),
            'inscricao_cnae': TextInputBootstrap(),
            'endereco': TextInputBootstrap(),
            'numero': TextInputBootstrap(),
            'complemento': TextInputBootstrap(),
            'bairro': TextInputBootstrap(),
            'cep': TextInputBootstrap(),
            'estado': SelectBootstrap(),
            'municipio': SelectBootstrap(),
            'celular': TextInputBootstrap(),
            'fone': TextInputBootstrap(),
            'email': TextInputBootstrap(),
            'ativo': CheckboxInputBootstrap(),
        }
        