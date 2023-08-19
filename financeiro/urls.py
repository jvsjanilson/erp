from django.urls import path
from financeiro.views import ContaReceberListView, ContaReceberCreate, ContaReceberUpdateView, \
    ContaReceberDeleteView, BaixarContaReceber, EstornarContaReceber

urlpatterns = [
    path("contarecebers/", ContaReceberListView.as_view(), name="contareceber-list"),
    path("contarecebers/create", ContaReceberCreate.as_view(), name="contareceber-create"),
    path("contarecebers/<int:pk>/update/", ContaReceberUpdateView.as_view(), name="contareceber-update"),
    path("contarecebers/<int:pk>/delete/", ContaReceberDeleteView.as_view(), name="contareceber-delete"),
    path("baixarecebers/<int:contareceber>/baixar", BaixarContaReceber.as_view(), name="baixareceber-baixar"),
    path("baixarecebers/<int:contareceber>/estornar", EstornarContaReceber.as_view(), name="baixareceber-estornar"),
]
