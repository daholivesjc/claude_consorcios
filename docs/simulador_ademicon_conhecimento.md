# Simulador "Venda da Carta com Lucro" — Ademicon

**Arquivo fonte:** `docs/Simulador Venda da Carta com Lucro - Ademicon  - cópia.xlsx`
**Aba única:** "Venda da Carta com Lucro" — 220 linhas de simulação (meses 1–220), 17 colunas (A–Q).

---

## 1. Parâmetros de Entrada (Linha 7–8) — Células Editáveis

| Célula | Campo | Valor Padrão |
|--------|-------|-------------|
| `A8` | Valor do Crédito | R$ 100.000 |
| `D8` | Parcela Liberada (paga pelo comprador) | R$ 338 |
| `E8` | Prazo (meses) | 220 |
| `F8` | Correção INCC (a.a.) | 6% |
| `G8` | % de Recompra / Ágio | 25% |
| `H8` | CDI (a.a.) | 14,2% |
| `C8` | Parcela Original (calculada) | `= A8 × (1 + Q12) / E8` = R$ 564,55 |
| `I8` | CDI (a.m.) | `= H8 / 12` ≈ 1,18% |

---

## 2. Configurações Auxiliares (Coluna P–Q)

| Célula | Nome | Valor | Fórmula |
|--------|------|-------|---------|
| `Q12` | Taxa Administrativa | 24,2% | Constante |
| `Q13` | Parcela Reduzida (%) | 50% | Redução aplicada ao comprador |
| `Q14` | Lance Embutido (nº parcelas antecipadas) | 44 | Constante |
| `Q15` | Crédito Reduzido + TX Adm | R$ 74.200 | `= (A8 × (1 − Q13)) + (A8 × Q12)` |

---

## 3. Estrutura das Colunas — 3 Blocos de Simulação

### BLOCO 1 — Modalidade SORTEIO (colunas A–G)

| Col | Nome | Fórmula |
|-----|------|---------|
| A | Mês da Contemplação | Texto: "1º mês", "2º mês"... |
| B | Crédito | Mantém valor; a cada 12 meses: `B × (1 + F8)` |
| C | Valor da Parcela | Idem B (corrigida anualmente pelo INCC) |
| D | Total Investido | `= D_anterior + C_atual` (acumulado) |
| E | Lucro Bruto | `= B × G8` (ágio = 25% do crédito) |
| F | Lucro Líquido | `= E − D` |
| G | ROI | `= F / D` |

### BLOCO 2 — Modalidade LANCE FIXO com Lance Embutido (colunas H–K)

| Col | Nome | Fórmula |
|-----|------|---------|
| H | Crédito c/ Lance Embutido | `= B − (((B × (1 + Q12)) / E8) × Q14)` |
| I | Lucro Bruto | `= H × G8` |
| J | Lucro Líquido | `= I − D` |
| K | ROI | `= J / D` |

> O Lance Embutido usa 44 parcelas futuras antecipadas como lance, reduzindo o crédito efetivo de R$ 100.000 para ~R$ 75.160.

### BLOCO 3 — Benchmark CDI (colunas L–N)

| Col | Nome | Fórmula |
|-----|------|---------|
| L | Total Acumulado CDI | `= L_anterior × (1 + H8/12) + C_atual` |
| M | Lucro Líquido CDI | `= L − Σ Parcelas pagas` |
| N | ROI CDI | `= M / L` |

---

## 4. Regra Crítica: Correção INCC Anual

A cada **12 meses**, crédito (col B) e parcela (col C) são multiplicados por `(1 + 6%)`.

```
Mês   1–12 : Crédito = R$ 100.000  | Parcela = R$ 338
Mês  13–24 : Crédito = R$ 106.000  | Parcela = R$ 358
Mês  25–36 : Crédito = R$ 112.360  | Parcela = R$ 379
...
Mês 217–220: Crédito = R$ 285.433  | Parcela = R$ 965
```

Ocorre nos meses: 13, 25, 37, 49, 61, 73, 85, 97, 109, 121, 133, 145, 157, 169, 181, 193, 205, 217.

---

## 5. Pontos de Break-even (Lucro Líquido = R$ 0)

| Modalidade | Último mês lucrativo | Primeiro mês de prejuízo | Total pago no ponto de virada |
|-----------|---------------------|--------------------------|-------------------------------|
| **Lance Embutido** | 65° mês (R$ +20 de lucro) | **66° mês** (−R$ 433) | R$ 25.578 |
| **Sorteio** | 90° mês (R$ +496 de lucro) | **91° mês** (−R$ 12) | R$ 37.603 |

---

## 6. Zonas de Decisão para Venda da Carta

```
MESES  ──────────────────────────────────────────────────────────────►

  1°       12°       24°       36°       48°      60°  66° 72°      91°
  │         │         │         │         │         │    │   │        │
  ▼         ▼         ▼         ▼         ▼         ▼    ▼   ▼        ▼

SORTEIO  [████████████████████████ VERDE ████████████| AMARELO |██]✗ PREJUÍZO
LANCE    [████████████████████████ VERDE █████████| AMARELO |██]✗ PREJUÍZO
CDI      [═══════════════════════════════════════════ cresce sempre ═════════►]
```

| Zona | Período | Sorteio ROI | Lance ROI | Recomendação |
|------|---------|------------|----------|-------------|
| **VERDE** | Até 48° mês | > 67% | > 26% | Vender sem hesitar |
| **AMARELA** | 49° ao 65°/90° | 38% → 1,3% | 3,8% → 0% | Sorteio ainda compensa; Lance com cuidado |
| **VERMELHA** | 66°+ (Lance) / 91°+ (Sorteio) | Prejuízo | Prejuízo | Não vender — usar o crédito |

> A partir do ~62°–63° mês, o CDI (renda fixa) já supera ambas as modalidades.

---

## 7. Marcos Quantitativos Chave

| Mês | Total Pago | Lucro Líq. Sorteio | ROI Sorteio | Lucro Líq. Lance | ROI Lance | CDI ROI |
|-----|-----------|-------------------|------------|-----------------|-----------|---------|
| 1°  | R$ 338    | R$ 24.662         | 7.296%     | R$ 18.452       | 5.459%    | 0%      |
| 12° | R$ 4.056  | R$ 20.944         | 516%       | R$ 14.734       | 363%      | 6,3%    |
| 24° | R$ 8.355  | R$ 18.145         | 217%       | R$ 11.562       | 138%      | 12,8%   |
| 36° | R$ 12.913 | R$ 15.177         | 117%       | R$ 8.200        | 63%       | 18,8%   |
| 48° | R$ 17.743 | R$ 12.032         | 68%        | R$ 4.636        | 26%       | 24,4%   |
| 60° | R$ 22.864 | R$ 8.698          | 38%        | R$ 858          | 3,8%      | 29,6%   |
| 66° | R$ 25.578 | R$ 7.878          | 30,8%      | **−R$ 433**     | **−1,7%** | 32,1%   |
| 84° | R$ 34.045 | R$ 1.418          | 4,2%       | −R$ 7.391       | −21,7%    | 39,1%   |
| 91° | R$ 37.603 | **−R$ 12**        | **−0,03%** | −R$ 9.350       | −24,9%    | 41,6%   |
| 120° | R$ 53.461 | −R$ 11.224       | −21%       | −R$ 21.716      | −40,6%    | 51,1%   |
| 180° | R$ 94.407 | −R$ 37.885       | −40%       | −R$ 51.925      | −55%      | 66,2%   |

---

## 8. Como Usar a Planilha

1. **Defina o grupo:** Preencha `A8` (crédito), `D8` (parcela), `E8` (prazo), `F8` (INCC), `G8` (ágio), `H8` (CDI)
2. **Identifique o mês esperado de contemplação** e localize a linha correspondente
3. **Compare os 3 cenários:** Sorteio (col F/G), Lance Embutido (col J/K), CDI (col M/N)
4. **Decida** com base nas zonas acima — o mês de contemplação é o fator determinante do lucro
