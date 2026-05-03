> **MCP Validated:** 2026-05-02

# Armadilha do Lance Embutido — "Dobre Seu Crédito"

Padrão de venda enganosa em que o consultor oferece "dobrar o crédito" usando lance embutido, transferindo o custo para o cliente sem que este perceba o efeito agregado.

---

## Quando Usar Este Padrão

- Toda vez que um corretor sugerir "alavancar" o crédito via embutido em lance livre
- Toda vez que a oferta for "compre R$X e leve R$2X" — nas variantes "dobre seu crédito" / "potencialize seu poder de compra"
- Sempre que o consultor empurrar o lance embutido como um **tipo de lance**, e não como modalidade de pagamento

---

## Premissa Central

> **Lance embutido é modalidade de pagamento, não tipo de lance.** Quando todos os concorrentes de um lance livre passam a usar embutido, os percentuais vencedores sobem e o custo da contemplação aumenta — exatamente o efeito oposto da promessa comercial.

Fonte: `docs/analise_metodo_jornada.md` §§3.3 e 4.

---

## A Oferta Típica

Reproduzindo o exemplo numérico do material original (`analise_metodo_jornada` §4 item 5):

> **Cliente:** quero crédito de R$ 500 mil.
> **Consultor:** posso te dar R$ 1 milhão usando 50% de embutido. Você "dobra seu crédito".

A primeira leitura sugere alavancagem. A leitura aritmética desmonta a promessa.

---

## Desmontando o Truque

### Etapa 1: Quem mais usa embutido?

Em um grupo onde **todos** estão sendo orientados a usar embutido em lance livre, o percentual vencedor sobe. O equilíbrio do grupo se desloca: para vencer, é preciso oferecer mais que os concorrentes.

### Etapa 2: O ajuste necessário

Para garantir contemplação dentro de lance livre saturado de embutido, o cliente precisa, em média, complementar com **~30% do bolso sobre o crédito de R$ 1 milhão**.

```
crédito nominal:                     R$ 1.000.000
embutido (50%):                      R$ 500.000   ← parte do próprio crédito
desembolso do bolso (~30%):          R$ 300.000   ← dinheiro real do cliente
crédito que o cliente efetivamente usa:
   = 1.000.000 − 500.000 (embutido) − 300.000 (lance do bolso)
   = R$ 200.000
```

### Etapa 3: Onde está o engano

| Item | Valor |
|------|-------|
| Crédito que o cliente "queria alavancar" | R$ 200.000 |
| Dinheiro real desembolsado de bolso | R$ 300.000 |
| Crédito **nominal** sobre o qual a taxa de administração incide | R$ 1.000.000 |

> O cliente paga taxa de administração sobre R$ 1 milhão **para alavancar apenas R$ 200 mil**, em uma operação onde ele desembolsou R$ 300 mil do bolso.

A "alavancagem" anunciada é negativa: o cliente alavanca menos do que efetivamente paga, e a taxa cobrada é cobrada sobre um crédito que ele não vai usar.

---

## Quem Ganha

| Beneficiário | O que ganha |
|--------------|-------------|
| Administradora | Taxa de administração sobre crédito cheio |
| Consultor / corretor | Comissão calculada sobre crédito cheio |
| Cliente | **Perde** — paga sobre crédito que não usa |

Esse desalinhamento de incentivos é o que torna a oferta tão comum apesar de tão prejudicial ao cliente.

---

## Como Reagir

### 1. Reformular a pergunta

```
NÃO PERGUNTE: "quanto eu posso alavancar?"
PERGUNTE:     "quanto crédito eu vou efetivamente usar?
               quanto vou desembolsar de bolso?
               sobre qual valor a taxa de administração incide?"
```

### 2. Calcular pessoalmente

```
crédito_efetivo = crédito_nominal − embutido − lance_do_bolso
custo_taxa_adm  = taxa_adm × crédito_nominal × prazo
```

Compare `crédito_efetivo` com o custo total. Se o custo da taxa for desproporcional ao crédito efetivo, a oferta é ruim.

### 3. Recusar embutido em lance livre

A `analise_metodo_jornada` §5 recomenda como regra geral: **evitar lance embutido em lance livre**. Em lance fixo, a análise é diferente — o percentual é determinístico e o efeito de saturação não opera da mesma forma.

### 4. Pedir ofertas comparáveis sem embutido

Pedir ao corretor uma simulação de cota com o **crédito efetivamente desejado** (R$ 200 mil ou R$ 500 mil), sem embutido, e comparar custos totais e tempos médios de contemplação.

---

## Por Que o Material da Megacombo Trata Disso Como "Cilada"

> O `analise_metodo_jornada.md` é uma análise crítica de material comercial da Megacombo (CNPJ 07.403.727/0001-69). O material original é interessado: vende o "Método da Jornada".

Apesar do conflito de interesse, a denúncia da armadilha do lance embutido é estruturalmente correta — a aritmética não depende do vendedor. Por isso o padrão é preservado aqui com a etiqueta auditorial: usar a aritmética, **sem** assumir que o exemplo do "grupo modelo" 650/216/2 do mesmo autor é necessariamente o melhor para qualquer cliente.

---

## Conexões

- [tipos-de-contemplacao](../concepts/tipos-de-contemplacao.md) — distinção lance vs modalidade de pagamento
- [aritmetica-do-grupo](../concepts/aritmetica-do-grupo.md) — fórmulas que tornam o efeito quantificável
- [screener-grupo-saudavel](screener-grupo-saudavel.md) — sinal de alerta #5 da auditoria de grupo
- [carta-de-credito](../concepts/carta-de-credito.md) — sobre o que a taxa de administração incide

---

## Fonte

`docs/analise_metodo_jornada.md` §3.3 (lance embutido como modalidade de pagamento) e §4 item 5 (exemplo "dobre seu crédito" com 50% embutido sobre R$ 1 milhão para alavancar R$ 200 mil).
