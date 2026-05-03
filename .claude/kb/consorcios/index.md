> **MCP Validated:** 2026-05-02

# Consórcios e Trade de Cartas Contempladas

Domínio de conhecimento sobre o sistema brasileiro de consórcios, mercado secundário de cotas contempladas, regime jurídico (Lei 11.795/2008), tributação (GCAP) e auditoria de grupos.

---

## Visão Geral

Este domínio cobre dois eixos complementares:

1. **Consórcio como ferramenta de aquisição** — alavancagem patrimonial sem juros, com base em sorteio e lance dentro de grupos administrados.
2. **Trade de cartas contempladas** — compra e venda de cotas já sorteadas com ágio, tratado como ganho de capital pela Receita Federal.

**Princípio central:** consórcio não é sorte — é aritmética e regra contratual. A chance real de contemplação de um grupo decorre da relação `cotas ÷ prazo` e da política de sorteios e lances. Quem entende a aritmética do grupo consegue evitar grupos deficitários e operar o trade com previsibilidade.

---

## Conceitos

| Conceito | Arquivo | Descrição |
|----------|---------|-----------|
| Aritmética do grupo | [concepts/aritmetica-do-grupo.md](concepts/aritmetica-do-grupo.md) | Fórmulas `cotas ÷ prazo` e `% sorteado`, exemplos numéricos |
| Tipos de contemplação | [concepts/tipos-de-contemplacao.md](concepts/tipos-de-contemplacao.md) | Sorteio, lance fixo, lance livre, lance fidelidade e a distinção do lance embutido |
| Ágio | [concepts/agio.md](concepts/agio.md) | Definição, formação e exemplo numérico do ágio em cota contemplada |
| Carta de crédito | [concepts/carta-de-credito.md](concepts/carta-de-credito.md) | O que é, atualização por INCC/IPCA, uso de FGTS no consórcio imobiliário |
| Mercado secundário de cotas | [concepts/mercado-secundario-de-cotas.md](concepts/mercado-secundario-de-cotas.md) | Cessão de direitos, anuência da administradora, papel das corretoras |
| Regime jurídico | [concepts/regime-juridico.md](concepts/regime-juridico.md) | Lei 11.795/2008 art. 13, ABAC, Banco Central, autorização de transferência |
| Tributação e ganho de capital | [concepts/tributacao-ganho-de-capital.md](concepts/tributacao-ganho-de-capital.md) | GCAP, alíquota de 15%, isenção de R$35k/mês, prazo do DARF |

## Padrões

| Padrão | Arquivo | Descrição |
|--------|---------|-----------|
| Screener de grupo saudável | [patterns/screener-grupo-saudavel.md](patterns/screener-grupo-saudavel.md) | Auditoria de grupo antes da entrada (cotas/prazo, % sorteio, sinais de alerta) |
| Trade de cartas contempladas | [patterns/trade-cartas-contempladas.md](patterns/trade-cartas-contempladas.md) | Passo a passo: aquisição, contemplação, anúncio, cessão, liquidação |
| Mitigação de risco de fraude | [patterns/mitigacao-risco-fraude.md](patterns/mitigacao-risco-fraude.md) | Checklist (anuência, validação direta, pagamento condicionado, certidões) |
| Mitigação de risco de crédito | [patterns/mitigacao-risco-credito.md](patterns/mitigacao-risco-credito.md) | Pré-análise do comprador e cláusula de reversão |
| Comparativo de investimentos | [patterns/comparativo-de-investimentos.md](patterns/comparativo-de-investimentos.md) | Consórcio vs renda fixa, FIIs e financiamento |
| Armadilha do lance embutido | [patterns/armadilha-lance-embutido.md](patterns/armadilha-lance-embutido.md) | Como a oferta de "dobre seu crédito" inverte a vantagem do cliente |

## Specs

| Spec | Arquivo | Descrição |
|------|---------|-----------|
| Administradoras de referência | [specs/administradoras-referencia.yaml](specs/administradoras-referencia.yaml) | Catálogo das administradoras citadas com flags (banco/independente, transferência, segmento forte) |
| Sinais de alerta de grupo | [specs/sinais-alerta-grupo.yaml](specs/sinais-alerta-grupo.yaml) | Lista machine-readable de red flags em ofertas e estruturas de grupo |

---

## Fontes Primárias

- **Relatório de Pesquisa (Manus AI)** — panorama de mercado, ágio, tributação, referências [1]–[15]
- **Guia de Mitigação de Riscos (Manus AI)** — protocolo de segurança em 5 categorias de risco
- **Análise Comparativa (Manus AI)** — consórcio vs renda fixa, FIIs e financiamento
- **Análise crítica do "Método da Jornada" (Megacombo)** — fórmulas universais e armadilhas comerciais

---

## Contexto de Uso

Este KB foi criado para apoiar decisões de entrada em consórcio (investimento ou aquisição) e operações de trade de cartas contempladas, com foco em três rotinas:

1. **Antes de assinar:** aplicar o `screener-grupo-saudavel` para descartar grupos deficitários.
2. **Durante o trade:** seguir os padrões de mitigação de risco para fraude, crédito e tributação.
3. **Comparando alternativas:** usar `comparativo-de-investimentos` para posicionar consórcio frente a renda fixa, FIIs e financiamento.
