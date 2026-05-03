> **MCP Validated:** 2026-05-02

# Mercado Secundário de Cotas

## Definição

O **mercado secundário de cotas de consórcio** é o conjunto de transações em que cotistas vendem suas cotas (em andamento ou já contempladas) a terceiros. Quando a cota já foi contemplada, a operação envolve **ágio** e configura o **trade de cartas contempladas**.

A operação se estrutura em três pilares: **cessão de direitos**, **anuência da administradora** e **intermediação por corretoras**.

---

## Premissa Central

> A cota só muda de dono quando a administradora carimba. Sem anuência, não há transferência juridicamente válida.

A cessão entre particulares (vendedor e comprador) não basta. A **anuência expressa da administradora** é requisito de validade — base jurídica detalhada em [regime-juridico](regime-juridico.md).

---

## Cessão de Direitos

Mecanismo formal que transfere os direitos e obrigações da cota do vendedor para o comprador, mediante:

1. Contrato particular de compra e venda do ágio (entre vendedor e comprador).
2. **Análise de crédito** do comprador pela administradora.
3. Termo oficial de cessão assinado nas instalações da administradora ou em cartório com validação posterior.
4. Quitação financeira (pagamento do ágio) preferencialmente após o termo oficial.

A não aprovação da análise de crédito **invalida** a operação e exige cláusula contratual de reversão para devolver o ágio (ver [mitigacao-risco-credito](../patterns/mitigacao-risco-credito.md)).

---

## Papel das Corretoras Especializadas

Algumas empresas atuam como **marketplaces**, conectando vendedores de cotas contempladas a compradores. Citadas no Relatório de Pesquisa §3.2:

| Corretora | Função |
|-----------|--------|
| Grupo LuME | Marketplace de cartas contempladas |
| Tramontana Consórcios | Marketplace de cartas contempladas |
| Toco Consórcios | Marketplace de cartas contempladas |

Vantagens típicas:

- Curadoria das cotas anunciadas
- Apoio jurídico para validação contratual
- Intermediação do contato com a administradora

Não substituem a anuência da administradora nem dispensam validação direta pelo comprador.

---

## Quem Aceita Transferência

| Tipo | Comportamento típico |
|------|----------------------|
| Independentes (Ademicon, Rodobens, Porto Seguro) | Aceitam transferência de cotas contempladas, com análise de crédito |
| Bancos (Itaú, Bradesco, Santander, BB, Caixa) | Geralmente **não participam ativamente** do mercado secundário; o trade do ágio é intermediado por corretores externos |

Fonte: Relatório de Pesquisa §3.1 e §3.2. A Ademicon, em particular, é destacada como ecossistema que facilita compra e venda de cotas (§3.1).

---

## Fluxo Resumido da Operação

```
VENDEDOR              ADMINISTRADORA            COMPRADOR
   │                       │                       │
   │  anuncia (corretora)  │                       │
   ├──────────────────────────────────────────────▶│
   │                       │   análise de crédito  │
   │                       │◀──────────────────────┤
   │                       │   aprovação           │
   │                       ├──────────────────────▶│
   │  termo de cessão      │                       │
   ├──────────────────────▶├──────────────────────▶│
   │                       │   anuência expressa   │
   │  recebe (parcelas+ágio)                       │
   │◀──────────────────────────────────────────────┤
```

---

## Riscos Específicos do Secundário

- **Cota inexistente** — anúncio fraudulento.
- **Falsa contemplação** — documentos forjados.
- **Pagamento antecipado** — golpista some após o depósito.
- **Cota com gravame** — bloqueio judicial ou pendência financeira oculta.

Os procedimentos de mitigação estão em [mitigacao-risco-fraude](../patterns/mitigacao-risco-fraude.md).

---

## Conexões

- [agio](agio.md) — preço da operação
- [regime-juridico](regime-juridico.md) — base legal da cessão
- [tributacao-ganho-de-capital](tributacao-ganho-de-capital.md) — fiscalização do lucro
- [trade-cartas-contempladas](../patterns/trade-cartas-contempladas.md) — passo a passo

---

## Fonte

`docs/Relatório de Pesquisa...md` §§3.1, 3.2, 4.2 e 5.2; `docs/Guia de Mitigação de Riscos...md` §§1, 2 e 4.
