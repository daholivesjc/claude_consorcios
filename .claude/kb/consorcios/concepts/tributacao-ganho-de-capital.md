> **MCP Validated:** 2026-05-02

# Tributação e Ganho de Capital

## Definição

O lucro obtido na venda de uma carta de crédito contemplada — o **ágio** — é considerado **Ganho de Capital** pela Receita Federal e está sujeito à apuração e recolhimento de IR via **programa GCAP**, com **alíquota de 15%** sobre o lucro, ressalvada a faixa de isenção mensal.

---

## Premissa Central

> O imposto incide sobre o **lucro** (ágio líquido), não sobre o preço total da cota. Custo de aquisição entra na base de cálculo.

Esquematicamente:

```
ganho de capital tributável = preço de venda − custo de aquisição
custo de aquisição          = parcelas pagas + taxas administrativas + lances pagos do bolso
```

Quem mantém registro rigoroso de todos os desembolsos paga menos imposto.

---

## Alíquota e Isenção

| Item | Regra |
|------|-------|
| Alíquota base | 15% sobre o lucro |
| Isenção | Vendas até **R$ 35.000 no mês** ficam isentas |
| Faixas progressivas | A partir de R$ 5 milhões, alíquota cresce (17,5% / 20% / 22,5%) |
| Prazo de pagamento (DARF) | Até o **último dia útil do mês subsequente** à venda |
| Programa | **GCAP** (Ganho de Capital), integrado ao IRPF |

A isenção de R$ 35.000/mês é por valor de **alienação** no mês, não por lucro. Vendas múltiplas no mesmo mês somam-se para fins do limite.

Fonte: `docs/Relatório de Pesquisa...md` §5.3 e referências [13]–[15]; `docs/Guia de Mitigação de Riscos...md` §5.

---

## Declaração no IRPF

| Etapa | Onde |
|-------|------|
| Durante o ano da venda | Apurar o GCAP no mês e pagar o DARF |
| Na declaração anual | Importar dados do GCAP para o IRPF |
| Ficha "Bens e Direitos" | Baixar a cota pelo valor de **custo** (não pelo preço de venda) |
| Ficha "Rendimentos sujeitos a tributação exclusiva/definitiva" | Lançar o ganho |

A cota deve sair da ficha de "Bens e Direitos" pelo valor de aquisição original. O lucro é informado em ficha específica de ganho de capital.

---

## Custo de Aquisição — O Que Compõe

Mantenha registro detalhado de:

- Parcelas pagas (mês a mês)
- Taxas de administração efetivamente desembolsadas
- Fundo de reserva
- Seguros pagos
- **Lances pagos do bolso** (não os embutidos)
- Eventuais taxas de cessão

Esses valores **somam ao custo** e reduzem a base de cálculo do imposto.

> Atenção: o **lance embutido** (parte do crédito futuro usada como lance) **não é desembolso** e portanto **não compõe o custo de aquisição**.

---

## Exemplo de Apuração

Investidor pagou R$ 50.000 (parcelas + taxas) e vende a cota contemplada por R$ 80.000:

```
preço de venda                     = R$ 80.000
custo de aquisição                 = R$ 50.000
ganho de capital                   = R$ 30.000
isenção mensal aplicável?          = NÃO (venda > R$ 35.000)
imposto devido (15%)               = R$ 4.500
ágio líquido após imposto          = R$ 30.000 − R$ 4.500 = R$ 25.500
```

Se houvesse, no mesmo mês, outra venda de cota por R$ 20.000, somaria com a primeira (R$ 80.000 + R$ 20.000 = R$ 100.000) — todas tributáveis sobre o respectivo lucro, pois o agregado supera R$ 35.000.

---

## Riscos de Não Apurar

- **Multa de mora** sobre o imposto não pago no prazo
- **Juros Selic** desde o vencimento
- **Multa de ofício** se a Receita autuar
- **Malha fina** ao cruzar dados das administradoras com o IRPF

A lavagem do trade pelo "esqueço o ágio" é caminho garantido para problema fiscal — `Guia...` §5 trata o risco tributário como uma das cinco categorias críticas.

---

## Conexões

- [agio](agio.md) — definição do ganho que será tributado
- [mercado-secundario-de-cotas](mercado-secundario-de-cotas.md) — operação que gera o fato gerador
- [trade-cartas-contempladas](../patterns/trade-cartas-contempladas.md) — onde cabe a etapa fiscal

---

## Fonte

`docs/Relatório de Pesquisa...md` §5.3 (alíquota, GCAP, R$35k); referências [13] (Rede Sul Consórcios), [14] (Blog BB), [15] (Valor Investe); `docs/Guia de Mitigação de Riscos...md` §5 (calendário fiscal, prazo do DARF).
