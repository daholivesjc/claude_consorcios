> **MCP Validated:** 2026-05-02

# Screener de Grupo Saudável — Auditoria Antes da Entrada

Processo de filtragem para descartar grupos deficitários **antes** de assinar o contrato. Aplica a aritmética do grupo e os sinais de alerta extraídos do material crítico do "Método da Jornada".

---

## Visão Geral

```
Oferta do corretor
    ↓  Passo 1: Coletar dados-base (cotas, prazo, sorteios/mês, lances)
    ↓  Passo 2: Calcular entregas/mês esperadas
    ↓  Passo 3: Calcular % sorteado
    ↓  Passo 4: Comparar com histórico real do grupo
    ↓  Passo 5: Auditar sinais de alerta contratuais
    ↓  Passo 6: Validar administradora (BCB/ABAC)
Decisão: entrar | renegociar grupo | descartar
```

---

## Passo 1: Coletar Dados-Base

Exija do corretor, por escrito (e-mail ou ficha do grupo):

- Número total de **cotas** do grupo
- **Prazo** em meses
- Quantos **sorteios por assembleia** mensal
- Política de **lance** (fixo, livre, fidelidade) e seus percentuais mínimos/máximos
- Política de **lance embutido** (permitido em quais modalidades)
- **Histórico** de contemplações dos últimos 12 meses (ou de grupos similares já encerrados, se for grupo novo)

> Se o corretor recusar fornecer histórico, isso já é sinal de alerta — `analise_metodo_jornada` §5.

---

## Passo 2: Entregas Mensais Esperadas

```
entregas_esperadas = nº de cotas ÷ prazo em meses
```

Calcule e registre. Exemplos de referência:

| Cotas | Prazo | Entregas/mês esperadas |
|---:|---:|---:|
| 650 | 216 | 3,01 |
| 1.000 | 200 | 5,00 |
| 2.000 | 180 | 11,11 |
| 3.000 | 200 | 15,00 |

---

## Passo 3: Percentual Sorteado

```
% sorteado = (sorteios/mês × prazo) ÷ total de cotas
```

Regras de bolso para a estratégia de entrada por sorteio:

| % sorteado | Avaliação |
|------------|-----------|
| ≥ 50% | Excelente — sorteio é caminho viável |
| 30–49% | Aceitável se complementado por lance |
| 10–29% | Sorteio improvável — depender de lance |
| < 10% | Ruim — só faz sentido com estratégia de lance agressiva |

---

## Passo 4: Histórico Real vs Esperado

Compare:

```
desvio = (entregas_reais_mes_medio − entregas_esperadas) ÷ entregas_esperadas
```

| Desvio | Leitura |
|--------|---------|
| ≥ 0 | Grupo entrega o que promete (ou mais) |
| −10% a 0 | Saudável (variação normal) |
| −30% a −10% | Atenção — verificar inadimplência |
| < −30% | Grupo deficitário — descartar |

Histórico ausente ou apresentado como "imagem decorativa" sem dados auditáveis = tratar como `< −30%` por precaução (`analise_metodo_jornada` §7).

---

## Passo 5: Sinais de Alerta Contratuais

Auditar os red flags listados em `specs/sinais-alerta-grupo.yaml`:

| # | Bandeira | Como identificar |
|---|----------|------------------|
| 1 | Todos pagam meia parcela | Ficha do grupo declara meia parcela como modelo |
| 2 | Milhares de cotas com 1 sorteio/mês | Passo 3 retorna < 10% |
| 3 | Meia parcela com taxa sobre crédito cheio | Comparar taxa contratual vs crédito reduzido |
| 4 | Promessa de contemplação em 3–6 meses via lance fixo/fidelidade | Discurso comercial otimista demais |
| 5 | Oferta de "dobre seu crédito" com 50% embutido | Ver [armadilha-lance-embutido](armadilha-lance-embutido.md) |

Cada bandeira presente reduz a nota do grupo. Duas ou mais → recomenda-se descarte.

---

## Passo 6: Validação Institucional

Antes de assinar:

1. Confirmar autorização da administradora no portal do **Banco Central** (Ranking de Administradoras de Consórcio).
2. Verificar associação à **ABAC**.
3. Conferir prazo de existência da administradora — preferir empresas com histórico longo (Ademicon: 35 anos, segundo §3.1 do Relatório).
4. Buscar reclamações no Reclame Aqui e processos no Jusbrasil em volume incompatível com o porte da empresa.

---

## Saída do Screener

| Avaliação | Ação |
|-----------|------|
| Verde (todos os passos OK) | Pode entrar; calibrar estratégia de sorteio vs lance |
| Amarelo (1 bandeira ou desvio entre −10% e −30%) | Renegociar grupo (outra oferta da mesma administradora) ou outra administradora |
| Vermelho (≥ 2 bandeiras ou desvio < −30%) | **Descartar** |

---

## Limitações Deste Screener

A aritmética e os red flags resolvem a parte mais bruta da decisão, mas não substituem:

- Modelagem de **TIR** considerando taxa de administração e reajuste
- Comparação com **financiamento** ao custo efetivo total (CET) vigente
- Análise contratual completa (cláusulas de devolução, cancelamento, cessão)

Use [comparativo-de-investimentos](comparativo-de-investimentos.md) para a próxima camada.

---

## Fonte

`docs/analise_metodo_jornada.md` §§3.1, 3.2, 4 e 5 (fórmulas, sinais de alerta e recomendações práticas); `docs/Relatório de Pesquisa...md` §§3.1 e 5.1 (validação institucional). Os red flags refletem a análise crítica do material da Megacombo, que é fonte comercial — preserva-se a visão auditorial do documento original.
