> **MCP Validated:** 2026-05-02

# Ágio

## Definição

O **ágio** é o valor adicional pago pelo comprador de uma carta de crédito **já contemplada**, acima do que o vendedor pagou em parcelas. Representa o preço da **conveniência** de obter acesso imediato ao crédito sem precisar aguardar sorteio ou desembolsar lance.

---

## Premissa Central

> O ágio é o preço da fila furada. Quem compra paga para entrar na frente.

Em uma cota nova, o cotista entra na fila e aguarda contemplação. Em uma cota contemplada, ele paga ágio para já receber a carta de crédito. O lucro do trade é exatamente esse ágio, líquido de taxas e tributos.

---

## Estrutura do Preço de Venda

```
preço de venda da cota contemplada = parcelas pagas pelo vendedor + ágio
```

| Componente | O que é |
|------------|---------|
| Parcelas pagas | Soma das parcelas e taxas que o vendedor desembolsou até a contemplação |
| Ágio | Margem de lucro do vendedor; o "preço da conveniência" para o comprador |
| Saldo devedor | Continua sob responsabilidade do **comprador** após a cessão |

---

## Exemplo Numérico

> Investidor pagou R$ 50.000 em parcelas. Sua cota é contemplada. Ele anuncia por R$ 80.000.

```
preço de venda = R$ 50.000 (já pago) + R$ 30.000 (ágio)
ágio           = R$ 30.000
```

O comprador desembolsa R$ 80.000 e assume o saldo devedor restante para utilizar a carta. O vendedor recebe R$ 80.000, dos quais **R$ 30.000 são ganho de capital** e tributáveis (ver [tributacao-ganho-de-capital](tributacao-ganho-de-capital.md)).

Fonte do exemplo: `docs/Relatório de Pesquisa...md` §4.1.

---

## Fatores Que Influenciam o Ágio

| Fator | Pressão sobre o ágio |
|-------|----------------------|
| Saldo devedor baixo | + (carta mais "pronta") |
| Crédito reajustado por INCC/IPCA acima da inflação corrente | + (ganho real para o comprador) |
| Taxas de juros de mercado altas (CDI/Selic) | − (alternativa de financiamento mais cara torna consórcio mais valioso, mas custo de oportunidade do dinheiro do comprador também sobe) |
| Tempo restante do grupo | − se muito longo (mais parcelas a pagar) |
| Liquidez do segmento (imóveis, veículos pesados) | + se ativo escasso |

---

## Rentabilidade Estimada do Trade

O Relatório de Pesquisa (§6) estima rentabilidade de **20% a 50% sobre o capital investido** em cenários de contemplação rápida. O "capital investido" aqui é o total já pago em parcelas até a contemplação; o ágio bruto é o lucro antes de taxas e tributos.

Atenção ao **tempo até a contemplação**: rentabilidade absoluta alta com janela longa pode ter TIR menor que renda fixa. Sempre anualizar.

---

## Ágio Bruto vs. Ágio Líquido

```
ágio bruto    = preço de venda − parcelas pagas
ágio líquido  = ágio bruto − taxas administrativas de cessão − IR sobre ganho de capital
```

A taxa de cessão é cobrada por algumas administradoras quando aprovam a transferência de titularidade. O IR sobre ganho de capital é de 15% sobre o lucro, com isenção mensal de R$ 35.000 (ver [tributacao-ganho-de-capital](tributacao-ganho-de-capital.md)).

---

## Sinais de Ágio Suspeito

- **Ágio muito abaixo do mercado** → possível fraude (cota inexistente, falsa contemplação).
- **Ágio negativo** (vendedor "abre mão" de parte do que pagou) → pode indicar urgência financeira, gravame oculto ou cota com problema cadastral.
- **Pedido de pagamento adiantado** → red flag clássico, ver [mitigacao-risco-fraude](../patterns/mitigacao-risco-fraude.md).

---

## Conexões

- [carta-de-credito](carta-de-credito.md) — o ativo subjacente do ágio
- [mercado-secundario-de-cotas](mercado-secundario-de-cotas.md) — onde o ágio é negociado
- [tributacao-ganho-de-capital](tributacao-ganho-de-capital.md) — regra fiscal sobre o lucro
- [trade-cartas-contempladas](../patterns/trade-cartas-contempladas.md) — operação completa

---

## Fonte

`docs/Relatório de Pesquisa...md` §§4.1, 4.2 e 6 (rentabilidade estimada). Exemplo numérico transposto literalmente.
