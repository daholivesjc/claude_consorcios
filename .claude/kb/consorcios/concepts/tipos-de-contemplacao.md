> **MCP Validated:** 2026-05-02

# Tipos de Contemplação

## Definição

A contemplação é o ato pelo qual um cotista do consórcio adquire o direito à carta de crédito antes do encerramento do grupo. Há essencialmente dois caminhos: **sorteio** e **lance**. O lance, por sua vez, tem variantes de regra contratual (livre, fixo, fidelidade) e há também uma **modalidade de pagamento** chamada lance embutido, que é frequentemente confundida com um tipo de lance — não é.

---

## Sorteio

A administradora realiza, em assembleia mensal, um sorteio entre as cotas adimplentes. O número de sorteios por assembleia é definido em contrato e é peça central da aritmética do grupo.

- Não exige desembolso adicional do cotista.
- Quanto maior o número de sorteios mensais relativamente ao total de cotas, maior o `% sorteado` do grupo (ver [aritmetica-do-grupo](aritmetica-do-grupo.md)).

---

## Lance

O lance é uma oferta antecipada de pagamento (em parcelas futuras ou em recursos próprios) feita pelo cotista para conquistar a contemplação. Quem oferece a maior fração do crédito vence — respeitadas as regras do contrato.

### Lance Livre

Modalidade clássica: cada cotista oferece o percentual que quiser do saldo devedor (em geral, dentro de limites mínimos e máximos definidos pela administradora). Vence o maior percentual.

### Lance Fixo

A administradora define um percentual fixo (p. ex. 30%, 40% ou 50% do crédito) e sorteia entre os participantes que ofertaram aquele valor exato. Tira o componente de leilão, mas exige liquidez para cobrir o percentual exigido.

### Lance Fidelidade

Variante do lance fixo condicionada a regularidade ou tempo de permanência. Em geral oferece um percentual mais favorável a quem nunca atrasou. As condições variam por administradora.

> Promessas de contemplação garantida em 3–6 meses via lance fixo ou fidelidade são tratadas pela `analise_metodo_jornada` §4 como sinal de venda enganosa.

---

## Lance Embutido — Modalidade de Pagamento

> **Distinção dura:** lance embutido **não** é um tipo de lance. É a forma como o lance é **pago**.

O cotista pode usar **uma fração da própria carta de crédito futura** para compor o valor do lance, em vez de desembolsar o dinheiro do bolso. Ou seja: o lance é financiado pelo próprio crédito que será recebido na contemplação. O cotista efetivamente recebe um crédito menor que o nominal.

Pode coexistir com qualquer modalidade contratual:

- Lance livre **com embutido** — parte do percentual ofertado vem do crédito.
- Lance fixo **com embutido** — idem, dentro do percentual exigido.

A `analise_metodo_jornada` §3.3 e §4 alertam: usar embutido em **lance livre** quase sempre é desvantajoso, porque o efeito agregado eleva os percentuais vencedores e o cotista paga taxa de administração sobre um crédito que, na prática, ele não vai usar. Ver [armadilha-lance-embutido](../patterns/armadilha-lance-embutido.md).

---

## Tabela Comparativa

| Tipo | Custo imediato | Previsibilidade | Risco principal |
|------|----------------|-----------------|-----------------|
| Sorteio | Nenhum (só parcela) | Baixa | Não ser contemplado no prazo |
| Lance livre | Variável (alto p/ vencer) | Média | Inflar o percentual e perder margem |
| Lance fixo / fidelidade | Percentual exigido | Alta (se sorteado entre os ofertantes) | Liquidez para cobrir o percentual |
| Lance embutido (modalidade) | Reduz crédito recebido | Depende do tipo onde é aplicado | Pagar taxa sobre crédito não utilizado |

---

## Conexões

- [aritmetica-do-grupo](aritmetica-do-grupo.md) — quanto maior o `% sorteado`, menor a dependência de lance
- [armadilha-lance-embutido](../patterns/armadilha-lance-embutido.md) — cenário "dobre seu crédito"
- [carta-de-credito](carta-de-credito.md) — o que está sendo financiado pelo embutido

---

## Fonte

`docs/analise_metodo_jornada.md` §§3.3 e 4. O Relatório de Pesquisa (`docs/Relatório de Pesquisa...md` §4.3) também trata o lance embutido como "estratégia de alavancagem"; aqui seguimos a leitura mais precisa do texto-fonte (Megacombo via análise crítica): trata-se de modalidade de pagamento, não tipo de lance.
