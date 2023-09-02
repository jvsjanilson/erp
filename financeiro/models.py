from django.db import models
from core.models import GenericoModel
from financeiro.choices import SituacaoFinanceiro
from cadastro.models import CondicaoPagamento, Contato
from django.core.validators import MinValueValidator
from django.db.models import Sum
from decimal import Decimal
from core.validators import alfa_numerico, valor_limite_pago
from django.utils import timezone


class ContaReceber(GenericoModel):
    documento = models.CharField('Documento', max_length=20, validators=[alfa_numerico])
    parcela = models.IntegerField('Parcela', default=1, validators=[MinValueValidator(limit_value=1)])
    contato = models.ForeignKey(Contato, on_delete=models.RESTRICT, verbose_name='Cliente')
    data_emissao = models.DateField('Data Emissão', default=timezone.now)
    data_vencimento = models.DateField('Data Vencto', default=timezone.now)
    valor_titulo = models.DecimalField('Vlr. Titulo', max_digits=15, decimal_places=2, default=0,
                                       validators=[MinValueValidator(limit_value=Decimal('0.01'),
                                                                     message='Informe um valor maior que 0,00')])
    observacao = models.CharField('Observação', max_length=500, null=True, blank=True)
    situacao = models.IntegerField('Situação', null=True, blank=True, choices=SituacaoFinanceiro.choices,
                                   default=SituacaoFinanceiro.ABERTO)

    def __str__(self):
        return self.documento
    
    @property
    def saldo_pagar(self):
        return self.valor_titulo - self.total_pago

    @property
    def total_pago(self) -> float:
        total_pago = self.baixas.aggregate(saldo=Sum('valor_pago'))['saldo']
        if total_pago is None:
            total_pago = Decimal('0.00')
        return Decimal(total_pago)

    class Meta:
        verbose_name = 'Conta Receber'
        verbose_name_plural = 'Contas Receber'


class BaixaReceber(GenericoModel):
    contareceber = models.ForeignKey(ContaReceber, on_delete=models.CASCADE, related_name='baixas')
    condicaopagamento = models.ForeignKey(CondicaoPagamento, on_delete=models.RESTRICT,
                                          verbose_name='Condição Pagamento')
    valor_juros = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(
        limit_value=Decimal('0.00'))])
    valor_multa = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(
        limit_value=Decimal('0.00'))])
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(
        limit_value=Decimal('0.00'))])
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(
        limit_value=Decimal('0.01'))])
    data_baixa = models.DateField()

    def clean(self) -> None:
        valor_limite_pago(self, self.contareceber.saldo_pagar)
        return super().clean()

    def __str__(self):
        return f'Documento: {self.contareceber.documento}'

    class Meta:
        verbose_name = 'Baixa Receber'
        verbose_name_plural = 'Baixas Receber'


class ContaPagar(GenericoModel):
    documento = models.CharField('Documento', max_length=20, validators=[alfa_numerico])
    parcela = models.IntegerField('Parcela', default=1)
    contato = models.ForeignKey(Contato, on_delete=models.RESTRICT, verbose_name='Fornecedor')
    data_emissao = models.DateField('Data Emissão', default=timezone.now)
    data_vencimento = models.DateField('Data Vencto', default=timezone.now)
    valor_titulo = models.DecimalField('Vlr. Titulo', max_digits=15, decimal_places=2, default=0,
                                       validators=[MinValueValidator(limit_value=Decimal('0.01'),
                                                                     message='Informe um valor maior que 0,00')])
    observacao = models.CharField('Observação', max_length=500, null=True, blank=True)
    situacao = models.IntegerField('Situação', null=True, blank=True, choices=SituacaoFinanceiro.choices,
                                   default=SituacaoFinanceiro.ABERTO)

    class Meta:
        verbose_name = 'Conta pagar'
        verbose_name_plural = 'Contas pagar'
        # unique_together = ['documento', 'parcela', 'contato']

    def __str__(self):
        return self.documento

    @property
    def saldo_pagar(self):
        return self.valor_titulo - self.total_pago

    @property
    def total_pago(self) -> float:
        total_pago = self.baixas.aggregate(saldo=Sum('valor_pago'))['saldo']
        if total_pago is None:
            total_pago = Decimal('0.00')
        return total_pago


class BaixaPagar(GenericoModel):
    contapagar = models.ForeignKey(ContaPagar, on_delete=models.CASCADE, related_name='baixas')
    condicaopagamento = models.ForeignKey(CondicaoPagamento, on_delete=models.RESTRICT,
                                          verbose_name='Condição Pagamento')
    valor_juros = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_multa = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(limit_value=Decimal('0.01'), message='Informe um valor maior que 0,00')])
    data_baixa = models.DateField()

    def clean(self) -> None:
        valor_limite_pago(self, self.contapagar.saldo_pagar)
        return super().clean()
    
    def __str__(self):
        return f'Documento: {self.contapagar.documento}'
