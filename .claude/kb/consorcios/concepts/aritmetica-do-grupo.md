> **MCP Validated:** 2026-05-02

# Aritmética do Grupo

## Definição

A aritmética do grupo é o conjunto de fórmulas elementares que descreve a capacidade de um grupo de consórcio de entregar contemplações ao longo do tempo. Trata o consórcio como um sistema fechado, onde a arrecadação mensal deve viabilizar um número previsível de cartas de crédito.

---

## Premissa Central

> Consórcio não é sorte — é matemática, estrutura e regra contratual.

Um grupo de N cotas com prazo P (em meses) precisa entregar, em média, `N ÷ P` cartas por mês para honrar os contratos no horizonte combinado. Quem entende essa aritmética avalia rapidamente se o grupo é saudável.

---

## Fórmulas Centrais

### Entregas mensais esperadas

```
entregas_esperadas_mes = nº de cotas ÷ prazo em meses
```

- Grupo de 1.000 cotas / 200 meses → **5 contemplações/mês**.
- Grupo de 3.000 cotas / 200 meses → **15 contemplações/mês**.

Se a entrega real do grupo for substancialmente menor que a esperada, há um **passivo de contemplação** — o grupo é deficitário.

### Percentual de sorteio

```
% sorteado = (sorteios/mês × prazo em meses) ÷ total de cotas
```

Estima a fração de cotas que serão contempladas por sorteio ao longo do prazo. As demais terão de buscar contemplação por lance.

| Exemplo | Cotas | Prazo (m) | Sorteios/mês | % sorteado |
|---|---:|---:|---:|---:|
| Grupo "modelo" Megacombo | 650 | 216 | 2 | **66%** |
| Grupo grande típico | 2.000 | 180 | 1 | **9%** |

A diferença entre 66% e 9% explica por que dois grupos com taxas e parcelas parecidas podem ter perfis de risco completamente distintos para quem espera ser contemplado por sorteio.

---

## Como Aplicar na Avaliação de um Grupo

1. **Pegue do corretor:** número de cotas, prazo, sorteios/mês.
2. **Calcule** `entregas_esperadas_mes` e `% sorteado`.
3. **Peça o histórico** de contemplações dos últimos 12 meses (ou de grupos similares fechados, se for grupo novo).
4. **Compare** entrega real vs entrega esperada — discrepância > 30% acende sinal vermelho.
5. **Se a estratégia for sorteio**, exija `% sorteado` ≥ 30% como regra de bolso. Se for lance, peça também o histórico dos lances vencedores.

---

## Variáveis Que a Fórmula Não Captura

A aritmética do grupo é necessária mas não suficiente. Ela ignora:

- Taxa de administração e fundo de reserva
- Reajuste do crédito (INCC, IPCA)
- Inadimplência efetiva do grupo (impacta o caixa real)
- Política de lances (mínimos, livres, embutidos)
- Cláusulas contratuais sobre devolução, cancelamento e cessão

Essas variáveis entram nas etapas seguintes da auditoria — ver [screener-grupo-saudavel](../patterns/screener-grupo-saudavel.md).

---

## Exemplos Numéricos Comparados

### Cenário A — Grupo enxuto e ativo

```
650 cotas / 216 meses / 2 sorteios mensais
entregas/mês esperadas = 650 / 216 ≈ 3,01
% sorteado            = (2 × 216) / 650 ≈ 66%
```

Dois terços dos cotistas saem por sorteio. O restante depende de lance.

### Cenário B — Grupo grande com 1 sorteio/mês

```
2.000 cotas / 180 meses / 1 sorteio mensal
entregas/mês esperadas = 2.000 / 180 ≈ 11,11
% sorteado            = (1 × 180) / 2.000 = 9%
```

Apenas 9% dos cotistas são contemplados por sorteio. Quem entra esperando "ter sorte" tende a percorrer todo o prazo sem contemplação se não der lance.

---

## Conexões

- [tipos-de-contemplacao](tipos-de-contemplacao.md) — sorteio, lance livre, lance fixo e o caso específico do lance embutido
- [mercado-secundario-de-cotas](mercado-secundario-de-cotas.md) — quando a contemplação não vem, sair via cessão é o plano B
- [screener-grupo-saudavel](../patterns/screener-grupo-saudavel.md) — usa estas fórmulas como primeiro filtro

---

## Fonte

`docs/analise_metodo_jornada.md` §§3.1–3.2. As fórmulas são universalmente válidas; o material original é comercial (Megacombo) e usa o "grupo modelo" 650/216/2 como autopromoção — extrair a aritmética é seguro, mas não generalize a partir do exemplo escolhido pelo próprio vendedor.
