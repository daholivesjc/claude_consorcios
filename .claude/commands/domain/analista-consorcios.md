---
description: Aciona o consorcios-specialist para análise de grupos, cotas contempladas, trade, comparativos e tributação (GCAP), 100% baseada na KB .claude/kb/consorcios.
argument-hint: [pergunta ou contexto livre — ex.: "auditar grupo 2000 cotas / 180 meses / 1 sorteio"]
---

# Analista de Consórcios

> Especialista em consórcios brasileiros e mercado secundário de cartas contempladas. Toda recomendação é ancorada em `.claude/kb/consorcios/` (7 conceitos + 6 padrões + 2 specs).

## Uso

```
/analista-consorcios <pergunta ou contexto>
```

**Exemplos:**

```
/analista-consorcios audita esse grupo: Ademicon imóvel, 1.500 cotas, 200 meses, 2 sorteios/mês, parcela integral
/analista-consorcios cota Porto Seguro contemplada — pago R$50k, ágio R$30k, vale a pena?
/analista-consorcios tenho R$80k para trade de cartas em 12 meses, monta um plano
/analista-consorcios consórcio ou financiamento para imóvel de R$500k em 5 anos?
/analista-consorcios o vendedor ofereceu dobrar meu crédito com 50% de embutido — analisa
/analista-consorcios vendi cota por R$80k, paguei R$50k em parcelas — quanto pago de IR e quando?
```

## O que acontece

1. **Captura contexto** — intenção (entrar em grupo / comprar cota / vender / comparar / declarar), capital, horizonte, segmento.
2. **Carrega a KB `.claude/kb/consorcios/`** — fonte única e autossuficiente. Lê `quick-reference.md` e os arquivos relevantes ao caso.
3. **Aplica o fluxo do agente** (`consorcios-specialist`):
   - Aritmética: `cotas ÷ prazo`, `% sorteado`
   - Validação jurídica: Lei 11.795/2008 art. 13, ABAC, BCB
   - Sinais de alerta: `specs/sinais-alerta-grupo.yaml`
   - Administradora: `specs/administradoras-referencia.yaml`
   - Tributação: GCAP 15%, isenção R$35k/mês, DARF
4. **Calcula confiança** com modificadores específicos do domínio.
5. **Recomenda com semáforo:** ENTRAR / AGUARDAR / DESCARTAR / FUGIR — sempre citando os arquivos da KB usados.

## Capabilities cobertas

| Capability | Quando aciona |
|-----------|---------------|
| Auditoria de grupo (screener pré-entrada) | Você tem proposta concreta de cotas × prazo × sorteios |
| Avaliação de cota contemplada | Cota anunciada com valor e ágio |
| Plano de trade de cartas | Capital alocado + horizonte definido |
| Comparativo patrimonial | Decisão entre consórcio, renda fixa, FIIs e financiamento |
| Armadilha do lance embutido | Oferta de "dobrar crédito" ou embutido > 25% |
| Cálculo de GCAP | Houve ou haverá venda de cota |

## Regra inegociável

Se a resposta não pode citar pelo menos um arquivo de `.claude/kb/consorcios/`, o agente declara baixa confiança e pede mais dados — não inventa. **A KB é fonte única e autossuficiente.**

## Veja também

- **Agente:** `.claude/agents/domain/consorcios-specialist.md`
- **Base de conhecimento:** `.claude/kb/consorcios/`
- **Índice de KB:** `.claude/kb/_index.yaml` (entrada `consorcios:`)
- **Material-fonte:** `docs/` (Manus AI + análise crítica do Método da Jornada)

---

## Instruções para a execução

Quando o usuário invocar este comando, delegue imediatamente ao agente **`consorcios-specialist`** (em `.claude/agents/domain/consorcios-specialist.md`), passando o argumento `$ARGUMENTS` como o contexto da consulta. O agente já contém:

- Decision flow em 8 passos
- Agreement Matrix com a KB como fonte única
- 17 modificadores de confiança domain-specific
- 6 capabilities (auditoria, avaliação de cota, trade, comparativo, armadilha do embutido, GCAP)
- Quality checklist e anti-patterns

Não execute análise diretamente — invoque o agente. Se o argumento estiver vazio, peça ao usuário a intenção, segmento, capital e horizonte antes de delegar.
