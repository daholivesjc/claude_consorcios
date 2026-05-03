> **MCP Validated:** 2026-05-02

# Trade de Cartas Contempladas — Passo a Passo

Sequência operacional do trade, desde a aquisição da cota até a liquidação fiscal.

---

## Visão Geral

```
AQUISIÇÃO ──▶ CONTEMPLAÇÃO ──▶ ANÚNCIO ──▶ ANÁLISE DE CRÉDITO ──▶ CESSÃO ──▶ LIQUIDAÇÃO ──▶ FISCO
   │              │              │             │                    │           │             │
 cota nova    sorteio/lance   marketplace   administradora        anuência    ágio + IR    GCAP/DARF
 ou andamento                  ou direto                                                    último dia útil
                                                                                            do mês +1
```

---

## Etapa 1: Aquisição da Cota

Duas portas de entrada:

- **Cota nova** — em grupo recém-formado; mais barato, mas sem histórico de contemplação.
- **Cota em andamento** — comprada de outro cotista; pode já ter histórico no grupo.

Em ambos os casos, aplicar o [screener-grupo-saudavel](screener-grupo-saudavel.md) **antes** de assinar.

---

## Etapa 2: Contemplação

Caminhos:

| Caminho | Vantagem | Desvantagem |
|---------|----------|-------------|
| Sorteio | Sem desembolso adicional | Imprevisível |
| Lance livre | Acelera contemplação | Custo do lance |
| Lance fixo / fidelidade | Mais previsível | Liquidez exigida |

Ver [tipos-de-contemplacao](../concepts/tipos-de-contemplacao.md). Evitar lance embutido em lance livre — ver [armadilha-lance-embutido](armadilha-lance-embutido.md).

---

## Etapa 3: Anúncio

Após contemplação, anunciar a cota:

- **Diretamente** — anúncios próprios, redes sociais, indicações.
- **Via marketplace** — Grupo LuME, Tramontana, Toco Consórcios (Relatório §3.2).

O anúncio deve conter:

- Administradora, número do grupo e da cota
- Saldo devedor restante e prazo
- Valor já pago + ágio pretendido
- Comprovação da contemplação (extrato oficial)

---

## Etapa 4: Análise de Crédito do Comprador

A administradora exige análise cadastral do comprador. Itens típicos:

- CPF/CNPJ sem restrições graves
- Renda compatível com as parcelas remanescentes
- Documentação completa (RG, CPF, comprovante de renda e residência)

> Vendedor: **antes** de assinar contrato particular, pedir que o comprador passe por **pré-análise** na administradora — protege contra reprovação tardia (`Guia...` §2).

---

## Etapa 5: Cessão de Direitos

Procedimento jurídico-formal:

1. Contrato particular de compra e venda do ágio entre vendedor e comprador, com cláusula de reversão por reprovação de crédito (ver [mitigacao-risco-credito](mitigacao-risco-credito.md)).
2. Termo oficial de cessão na administradora (firma reconhecida ou assinatura presencial).
3. **Anuência expressa** da administradora registrada no sistema.
4. Atualização do titular no grupo.

Sem essa anuência, a operação **não vincula a administradora** — ver [regime-juridico](../concepts/regime-juridico.md).

---

## Etapa 6: Liquidação Financeira

| Elemento | Regra prudencial |
|----------|------------------|
| Pagamento do ágio | **Após** a confirmação da transferência de titularidade (Guia §1) |
| Forma de pagamento | TED/PIX rastreável; nunca dinheiro vivo |
| Custódia intermediária | Em algumas operações, marketplace ou cartório retém os valores até a anuência |

> O `Guia de Mitigação de Riscos...md` §1 é categórico: nunca pague o ágio antes da formalização da cessão.

---

## Etapa 7: Liquidação Fiscal

Ver [tributacao-ganho-de-capital](../concepts/tributacao-ganho-de-capital.md).

```
1. Apurar custo de aquisição (parcelas pagas + taxas + lances do bolso)
2. Apurar lucro = preço de venda − custo de aquisição
3. Verificar se a venda do mês excede R$ 35.000 (limite de isenção)
4. Se tributável: emitir DARF GCAP, pagar até o último dia útil do mês subsequente
5. Lançar baixa da cota na ficha "Bens e Direitos" do IRPF do ano-base
6. Importar dados do GCAP para a declaração anual
```

---

## Métricas do Trade

| Métrica | Cálculo |
|---------|---------|
| Ágio bruto | Preço de venda − parcelas pagas |
| Ágio líquido | Ágio bruto − taxa de cessão − IR (15%) |
| Rentabilidade nominal | Ágio líquido ÷ capital investido |
| Rentabilidade anualizada | (1 + rent. nominal)^(12/meses até contemplação) − 1 |
| Custo de oportunidade | Comparar com CDI do período (ver [comparativo-de-investimentos](comparativo-de-investimentos.md)) |

Rentabilidade típica reportada: **20% a 50% sobre o capital investido** em cenários de contemplação rápida (Relatório §6).

---

## Alertas Operacionais

- **Não anunciar antes da contemplação confirmada** (anúncio falso pode caracterizar estelionato).
- **Não aceitar pagamento adiantado** mesmo de comprador conhecido — siga o procedimento institucional.
- **Não esquecer da etapa fiscal** — Receita Federal recebe dados das administradoras.

---

## Conexões

- [screener-grupo-saudavel](screener-grupo-saudavel.md) — auditoria pré-entrada
- [mitigacao-risco-fraude](mitigacao-risco-fraude.md) — defesas no anúncio e cessão
- [mitigacao-risco-credito](mitigacao-risco-credito.md) — reprovação do comprador
- [armadilha-lance-embutido](armadilha-lance-embutido.md) — risco específico na contemplação

---

## Fonte

`docs/Relatório de Pesquisa...md` §§4.2, 5.1, 5.2 e 5.3 (passo a passo, riscos, segurança jurídica e tributação); `docs/Guia de Mitigação de Riscos...md` resumo final ("caminho seguro do investidor").
