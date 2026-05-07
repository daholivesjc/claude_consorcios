"""ClaudeConsórcios — Especialista em Consórcios e Trade de Cartas Contempladas"""

from __future__ import annotations

import json
import logging
import math
import os
import uuid
from datetime import datetime, date
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import config

load_dotenv()

logging.basicConfig(level=logging.WARNING)

st.set_page_config(
    page_title="ClaudeConsórcios — Especialista",
    page_icon="🏠",
    layout="wide",
)

# ── Modelos disponíveis ───────────────────────────────────────────────────────
# Prefixo "groq/" → Groq API (GROQ_API_KEY)
# Demais           → OpenRouter (OPEN_ROUTER)
MODELOS = {
    "⚡ Llama 3.3 70B (Groq)":   "groq/llama-3.3-70b-versatile",
    "⚡ Llama 3.1 8B (Groq)":    "groq/llama-3.1-8b-instant",
    "🆓 Gemma 3 27B (OR)":       "google/gemma-3-27b-it:free",
    "💎 Gemini 2.0 Flash":       "google/gemini-2.0-flash-001",
    "💎 Claude Sonnet 4.6":      "anthropic/claude-sonnet-4-6",
    "💎 GPT-4o":                 "openai/gpt-4o",
}

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""Você é um especialista em consórcios brasileiros e trade de cartas contempladas.
Data atual: {datetime.now().strftime('%d/%m/%Y')}. Responda sempre em português do Brasil.

# Base de Conhecimento — Consórcios

## Aritmética do Grupo
```
entregas_esperadas = cotas ÷ prazo_em_meses
pct_sorteado       = (sorteios_por_mes × prazo) ÷ total_de_cotas × 100
```

| % sorteado | Avaliação |
|---|---|
| ≥ 50% | Excelente — sorteio é caminho viável |
| 30–49% | Aceitável se complementado por lance |
| 10–29% | Sorteio improvável — depender de lance |
| < 10% | Ruim — só estratégia de lance agressiva |

## Tipos de Contemplação
- **Sorteio**: Mensal, sem desembolso adicional, mas imprevisível
- **Lance livre**: Maior oferta percentual ganha; custo do lance
- **Lance fixo / fidelidade**: Percentual pré-definido; mais previsível
- **Lance embutido**: Modalidade de PAGAMENTO (parte do crédito futuro vira lance), NÃO é tipo de lance — é armadilha quando vendido como alavancagem

## Ágio e Trade de Cartas Contempladas
```
preço_de_venda = parcelas_pagas + ágio
ágio_bruto     = preço_de_venda − parcelas_pagas
ágio_líquido   = ágio_bruto − taxa_de_cessão − IR (15%)
```
- Rentabilidade típica: 20%–50% sobre capital investido em contemplação rápida
- Sempre anualizar a TIR para comparar com CDI

## Tributação (GCAP)
```
ganho_de_capital = preço_venda − custo_aquisição
custo_aquisição  = parcelas + taxas + lances pagos do bolso (exceto lance embutido)
```
| Regra | Detalhe |
|---|---|
| Isenção | Alienações até R$ 35.000 no mês |
| Alíquota base | 15% sobre o lucro |
| Alíquotas progressivas | 17,5% (>R$5M), 20% (>R$10M), 22,5% (>R$30M) |
| Prazo DARF | Último dia útil do mês seguinte à venda |

## Sinais de Alerta — Red Flags
1. Todos pagam meia parcela → arrecadação cai pela metade
2. Milhares de cotas com 1 sorteio/mês → % sorteado próximo de zero
3. Meia parcela com taxa sobre crédito cheio → dobro de taxa relativa
4. Promessa de contemplação em 3–6 meses via sorteio → enganoso
5. "Dobre seu crédito" com 50% embutido → paga taxa sobre crédito cheio para alavancar crédito reduzido

Duas ou mais bandeiras → descartar o grupo.

## Trade — Caminho Seguro
1. Seleção: administradora autorizada pelo Banco Central + associada à ABAC
2. Validação: confirmar dados da cota no portal do consorciado ou SAC
3. Formalização: cessão com anuência EXPRESSA da administradora registrada no sistema
4. Financeiro: pagar ágio SOMENTE APÓS transferência de titularidade confirmada
   → NUNCA pagar adiantado, nem a marketplaces sem custódia

## Administradoras de Referência
- Independentes: Ademicon (35 anos), Rodobens, Porto Seguro, Evoy, Reserva, Simpala, Magalu, HS
- Bancos: Itaú, Bradesco, Santander, BB, Caixa
- Marketplaces de cartas: Grupo LuME, Tramontana, Toco Consórcios

## Comparativo de Investimentos
| Critério | Consórcio | Renda Fixa | FIIs | Financiamento |
|---|---|---|---|---|
| Objetivo | Alavancagem/Bem | Preservação | Renda mensal | Uso imediato |
| Custo | Taxa adm (sem juros) | Recebe juros | Recebe dividendos | Juros bancários |
| Liquidez | Baixa | Alta a média | Alta (bolsa) | Nula |
| Risco principal | Tempo de espera | Baixo | Mercado | Inadimplência |

## Simulador Venda da Carta — Modelo Ademicon

**Referência:** planilha "Venda da Carta com Lucro" da Ademicon (220 meses, 17 colunas, 3 blocos de simulação).

**Parâmetros padrão:** Crédito R$ 100.000 | Parcela R$ 338/mês | Prazo 220 meses | INCC 6%a.a. | Ágio 25% | CDI 14,2%a.a. | Taxa Adm 24,2% | Lance Embutido 44 parcelas antecipadas.

**Regra INCC:** crédito e parcela sobem 6% a cada 12 meses (meses 13, 25, 37, 49 …)
```
Mês  1–12 : Crédito = R$ 100.000  | Parcela ≈ R$ 338
Mês 13–24 : Crédito = R$ 106.000  | Parcela ≈ R$ 358
Mês 25–36 : Crédito = R$ 112.360  | Parcela ≈ R$ 379
Mês 217–220: Crédito = R$ 285.433 | Parcela ≈ R$ 965
```

**Lance Embutido — fórmula do crédito efetivo:**
```
parcela_original  = crédito × (1 + taxa_adm) ÷ prazo
crédito_embutido  = crédito − parcela_original × 44 parcelas
→ R$ 100.000 vira ~R$ 75.160 de crédito efetivo (desconto de ~25%)
```

**Pontos de break-even (parâmetros padrão):**
- Lance Embutido: lucrativo até o 65°, **prejuízo a partir do 66° mês** (R$ –433)
- Sorteio: lucrativo até o 90°, **prejuízo a partir do 91° mês** (R$ –12)
- CDI supera ambas as modalidades a partir do **~63° mês**

**Zonas de Decisão:**
| Zona | Período | Sorteio ROI | Lance ROI | Recomendação |
|---|---|---|---|---|
| VERDE | Até 48° mês | > 67% | > 26% | Vender sem hesitar |
| AMARELA | 49°–90° (Sorteio) / 49°–65° (Lance) | 38% → ~1% | 3,8% → 0% | Sorteio compensa; Lance com cuidado |
| VERMELHA | 91°+ (Sorteio) / 66°+ (Lance) | Prejuízo | Prejuízo | Não vender — usar o crédito |

**Marcos quantitativos (parâmetros padrão):**
| Mês | Total Pago | ROI Sorteio | ROI Lance | ROI CDI |
|---|---|---|---|---|
| 1° | R$ 338 | 7.296% | 5.459% | ~1% |
| 12° | R$ 4.056 | 516% | 363% | 6,3% |
| 48° | R$ 17.743 | 68% | 26% | 24,4% |
| 60° | R$ 22.864 | 38% | 3,8% | 29,6% |
| 66° | R$ 25.578 | 30,8% | **−1,7%** | 32,1% |
| 91° | R$ 37.603 | **−0,03%** | −24,9% | 41,6% |
| 120° | R$ 53.461 | −21% | −40,6% | 51,1% |

Use a tool `simular_venda_carta` quando o usuário informar o mês de contemplação e quiser saber se vale a pena vender a carta ou usar o crédito.

## Estratégia do Método — Múltiplas Cartas e Bola de Neve

### Diversificação: N cartas menores > 1 carta grande
- N cartas de R$ 100.000 têm N× mais probabilidade de contemplação do que 1 carta de R$ 500.000 pelo mesmo aporte mensal total
- Cada carta contemplada gera lucro independente — não precisa esperar todas para lucrar
- Período de retorno sensacional: contemplação até o 6° ano (≈ 72 meses)
- Contemplação entre 7–13 anos: (a) usar crédito para imóvel com aluguel pagando o saldo devedor; ou (b) deixar o crédito investido em fundo de renda fixa, rendendo sobre o capital acumulado (~dobro do investido até ali)
- Contemplação acima de 13 anos: crédito corrigido pelo INCC ainda supera total pago, mas retorno menos expressivo

### Efeito Bola de Neve
- Ao vender a carta contemplada, reinvestir o lucro em novas cartas sem aumentar o aporte próprio
- As novas cartas são pagas com o lucro obtido → mais cartas → mais chances de contemplação → ciclo se acelera
- Regra: nunca parar de fazer aportes mensais enquanto a estratégia de crescimento de patrimônio estiver ativa

### 3 Critérios de Escolha da Administradora (específicos para trade)
1. **Junção de cartas de grupos DIFERENTES**: permitir unir créditos de qualquer grupo da administradora para formar valores maiores (R$ 300k, R$ 500k, R$ 1M). Junção apenas dentro do mesmo grupo não é suficiente.
2. **Volume de cartas no mercado**: dezenas ou centenas de cartas contempladas por mês para tornar a junção viável na prática. Administradoras pequenas ou "digitais" sem histórico são irrelevantes.
3. **Máximo de modalidades de uso**: imóvel novo, usado, construção, reforma E compra de terreno. Quanto mais usos permitidos, maior o público potencial comprador.

### Regras Operacionais do Método
- **NÃO dar lance em cota destinada à venda**: lance antecipa pagamentos ao grupo e reduz a margem de lucro → somente dá lance quem vai usar o crédito para comprar imóvel
- **FGTS**: usar FGTS no consórcio obriga a compra de imóvel — NUNCA permite vender a carta contemplada
- **Seguro prestamista**: geralmente incluído na prestação; quita o saldo devedor em caso de falecimento ou invalidez permanente — recomendável manter
- **Cancelamento da cota**: perdas de ~50%+ dos valores amortizados (desconta taxa adm paga + multa + taxa de reposição). Continua concorrendo nos sorteios como "cancelado" para receber de volta. NUNCA cancelar — só investir o que se pode pagar mensalmente por longo prazo
- **Taxa de administração NÃO é o critério determinante**: o que importa é contemplar cedo e ter liquidez para vender

### Precificação da Carta Contemplada para o Comprador
- Carta contemplada é precificada como crédito com CET equivalente a **7%–8% a.a.** (~0,6%/mês)
- Mais barato que qualquer financiamento bancário → vantagem estrutural para o comprador → alta demanda permanente
- Comprador também inclui: quem tem dificuldade de comprovar renda para financiamento (parcela do consórcio é menor) e quem tem dinheiro à vista mas prefere não se descapitalizar

### Processo de Transferência da Carta Contemplada
1. Intermediária recebe sinal do comprador confirmando intenção de compra
2. Administradora avalia documentos e capacidade de pagamento do comprador
3. Administradora envia e-mail + SMS para validação biométrica e assinatura digital do vendedor
4. Prazo típico: **2 a 4 semanas** da contemplação até carta transferida e dinheiro na conta do vendedor
5. Após transferência, vendedor não tem mais nenhuma obrigação com o consórcio

### Sinal de Alerta Adicional — Grupos de Banco
- Gerentes empurram consórcio em venda casada → cliente obtém o produto que queria e logo cancela o consórcio
- Alta rotatividade gera arrecadação deficitária → contemplações concentradas no final do prazo → período de menor lucro
- Exemplo real: grupo com 1.000 participantes com 2.840 desistentes ou excluídos

### INCC — Dados Históricos
- Média dos últimos 20 anos: **6,3% a.a.**
- Pico recente: **17% em 2021** (pandemia) — crédito subiu muito mais do que as parcelas pagas no ano, ampliando a margem de lucro

### Por que Consórcio de Imóveis (não veículos)
- Prazo longo (≥ 10 anos): parcelas menores para o mesmo crédito → margem de lucro maior
- Prazo curto (veículos): parcelas altas para o mesmo crédito + baixa probabilidade por sorteio = lucro insignificante

## Regime Jurídico
- Lei 11.795/2008 regula o sistema de consórcios no Brasil
- Administradoras precisam de autorização do Banco Central do Brasil
- Cessão de cota exige anuência da administradora — sem ela, não vincula a administradora
- ABAC: Associação Brasileira de Administradoras de Consórcios

## Mercado (dez/2025, ABAC)
- 12,76 milhões de participantes ativos
- 5,16 milhões de cotas vendidas em 2025 (+15% vs 2024)
- R$ 500,27 bi em créditos comercializados (+32,1%)

# Comportamento Esperado
- Use as tools quando o usuário fornecer dados suficientes para cálculo
- Após calcular, dê recomendação clara: VERDE/AMARELO/VERMELHO (grupos) ou VIÁVEL/ANALISAR/EVITAR (trades)
- Cite leis e regulações relevantes quando pertinente (Lei 11.795, BCB, ABAC, GCAP)
- NUNCA recomende pagar ágio antes da anuência da administradora
- Use termos técnicos precisos: carta de crédito, contemplação, ágio, GCAP, cota deficitária
"""


# ── Definição dos tools ───────────────────────────────────────────────────────

def _tool(name: str, description: str, parameters: dict) -> dict:
    return {"type": "function", "function": {"name": name, "description": description, "parameters": parameters}}


TOOLS = [
    _tool(
        "auditar_grupo",
        "Audita um grupo de consórcio: calcula entregas/mês, % sorteado e classifica Verde/Amarelo/Vermelho com veredicto.",
        {
            "type": "object",
            "required": ["cotas", "prazo_meses", "sorteios_por_mes"],
            "properties": {
                "cotas": {"type": "integer", "description": "Número total de cotas do grupo"},
                "prazo_meses": {"type": "integer", "description": "Prazo do grupo em meses"},
                "sorteios_por_mes": {"type": "integer", "description": "Sorteios por assembleia mensal"},
                "red_flags": {
                    "type": "array", "items": {"type": "integer"},
                    "description": "Índices (1–5) das bandeiras vermelhas presentes"
                },
                "desvio_historico_pct": {
                    "type": "number",
                    "description": "Desvio do histórico real vs esperado em % (negativo = abaixo do esperado; null se não disponível)"
                },
            },
        },
    ),
    _tool(
        "calcular_agio",
        "Calcula ágio bruto, ágio líquido (após taxa de cessão e IR de 15%) e rentabilidade do trade. Use quando o usuário informar parcelas pagas e preço de venda.",
        {
            "type": "object",
            "required": ["parcelas_pagas", "preco_venda"],
            "properties": {
                "parcelas_pagas": {"type": "number", "description": "Total já pago pelo vendedor em parcelas e taxas (custo de aquisição)"},
                "preco_venda": {"type": "number", "description": "Preço de venda da cota contemplada"},
                "taxa_cessao": {"type": "number", "default": 0, "description": "Taxa de cessão cobrada pela administradora (R$)"},
                "meses_ate_contemplacao": {
                    "type": "integer",
                    "description": "Meses transcorridos até a contemplação (para calcular TIR anualizada)"
                },
            },
        },
    ),
    _tool(
        "calcular_gcap",
        "Calcula o imposto de renda (GCAP) sobre a venda de cota contemplada. Verifica isenção de R$35k/mês e gera instrução do DARF.",
        {
            "type": "object",
            "required": ["preco_venda", "custo_aquisicao"],
            "properties": {
                "preco_venda": {"type": "number", "description": "Preço de venda da cota"},
                "custo_aquisicao": {"type": "number", "description": "Custo total (parcelas + taxas + lances pagos do bolso — NÃO inclui lance embutido)"},
                "outras_vendas_no_mes": {
                    "type": "number", "default": 0,
                    "description": "Valor de outras alienações no mesmo mês (para verificar se ultrapassa o limite de isenção)"
                },
                "mes_venda": {"type": "integer", "description": "Mês da venda (1–12) para calcular prazo do DARF"},
                "ano_venda": {"type": "integer", "description": "Ano da venda (ex: 2026)"},
            },
        },
    ),
    _tool(
        "verificar_red_flags",
        "Verifica bandeiras vermelhas em uma oferta de consórcio. Retorna lista de problemas e veredicto.",
        {
            "type": "object",
            "properties": {
                "cotas": {"type": "integer", "description": "Número total de cotas"},
                "prazo_meses": {"type": "integer", "description": "Prazo em meses"},
                "sorteios_por_mes": {"type": "integer", "description": "Sorteios por mês"},
                "meia_parcela": {"type": "boolean", "description": "Todos pagam meia parcela?"},
                "promessa_meses": {
                    "type": "integer",
                    "description": "Promessa de contemplação em X meses via sorteio (0 = sem promessa)"
                },
                "lance_embutido_pct": {
                    "type": "number",
                    "description": "Percentual de lance embutido ofertado como 'alavancagem' (ex: 50 para 50%)"
                },
                "taxa_sobre_credito_cheio": {
                    "type": "boolean",
                    "description": "Taxa administrativa calculada sobre crédito cheio mesmo com meia parcela?"
                },
            },
        },
    ),
    _tool(
        "comparar_investimentos",
        "Compara consórcio com renda fixa (CDI) e financiamento bancário para o mesmo objetivo financeiro.",
        {
            "type": "object",
            "required": ["valor_credito", "prazo_meses"],
            "properties": {
                "valor_credito": {"type": "number", "description": "Valor do crédito / bem desejado (R$)"},
                "prazo_meses": {"type": "integer", "description": "Prazo em meses"},
                "taxa_adm_pct_ano": {
                    "type": "number", "default": 1.5,
                    "description": "Taxa de administração anual do consórcio (%)"
                },
                "cdi_anual_pct": {
                    "type": "number", "default": 10.5,
                    "description": "CDI / Selic anual vigente (%)"
                },
                "taxa_financiamento_anual_pct": {
                    "type": "number", "default": 12.0,
                    "description": "Taxa de juros do financiamento bancário (% a.a.)"
                },
            },
        },
    ),
    _tool(
        "calcular_multiplas_cartas",
        (
            "Analisa a estratégia de múltiplas cartas de consórcio: calcula parcela total mensal, "
            "fator de probabilidade (N× maior vs 1 carta), estimativa de lucro se 1 carta contemplar "
            "em cada zona (VERDE/AMARELA/VERMELHA) e efeito bola de neve ao reinvestir o primeiro lucro. "
            "Use quando o usuário perguntar quantas cartas fazer, qual o aporte necessário, "
            "ou quiser entender o efeito de diversificar em várias cartas menores."
        ),
        {
            "type": "object",
            "required": ["numero_cartas", "parcela_por_carta"],
            "properties": {
                "numero_cartas": {
                    "type": "integer",
                    "description": "Número de cartas de consórcio que o investidor deseja manter simultaneamente"
                },
                "parcela_por_carta": {
                    "type": "number",
                    "description": "Parcela mensal por carta em R$ (ex: 644 para o plano padrão Rodobens/MegaCombo)"
                },
                "valor_credito_por_carta": {
                    "type": "number",
                    "description": "Valor do crédito de cada carta em R$ (padrão: 100.000)"
                },
                "pct_sorteado_grupo": {
                    "type": "number",
                    "description": "% de cotas sorteadas no grupo (padrão: 66 para o plano MegaCombo; 9 para grupos ruins)"
                },
                "prazo_meses": {
                    "type": "integer",
                    "description": "Prazo do grupo em meses (padrão: 216)"
                },
                "agio_pct": {
                    "type": "number",
                    "description": "Percentual de ágio esperado na venda (padrão: 25%)"
                },
                "incc_anual_pct": {
                    "type": "number",
                    "description": "INCC anual projetado (padrão: 6%)"
                },
            },
        },
    ),
    _tool(
        "simular_venda_carta",
        (
            "Simula a rentabilidade da venda de carta contemplada no mês informado, usando o modelo Ademicon "
            "(3 cenários: Sorteio, Lance Embutido e CDI benchmark). Calcula total investido, lucro líquido, "
            "ROI e classifica a zona de decisão VERDE/AMARELA/VERMELHA. "
            "Identifica os pontos de break-even (padrão: Lance=66°mês, Sorteio=91°mês) e o mês em que o CDI supera ambos. "
            "Use quando o usuário informar o mês de contemplação e quiser saber se vale a pena vender ou usar o crédito."
        ),
        {
            "type": "object",
            "required": ["mes_contemplacao"],
            "properties": {
                "mes_contemplacao": {
                    "type": "integer",
                    "description": "Mês em que ocorreu (ou ocorrerá) a contemplação (1–220)"
                },
                "valor_credito": {
                    "type": "number",
                    "description": "Valor do crédito em R$ (padrão: 100.000)"
                },
                "parcela": {
                    "type": "number",
                    "description": "Parcela mensal inicial em R$ (padrão: 338)"
                },
                "prazo_meses": {
                    "type": "integer",
                    "description": "Prazo total do grupo em meses (padrão: 220)"
                },
                "agio_pct": {
                    "type": "number",
                    "description": "Percentual de ágio sobre o crédito no momento da venda, ex: 25 para 25% (padrão: 25)"
                },
                "incc_anual_pct": {
                    "type": "number",
                    "description": "Correção INCC anual aplicada ao crédito e à parcela (padrão: 6)"
                },
                "cdi_anual_pct": {
                    "type": "number",
                    "description": "CDI anual para benchmark de renda fixa (padrão: 14,2)"
                },
                "taxa_adm_pct": {
                    "type": "number",
                    "description": "Taxa de administração total do grupo em % (padrão: 24,2)"
                },
                "lance_embutido_parcelas": {
                    "type": "integer",
                    "description": "Número de parcelas antecipadas usadas como lance embutido (padrão: 44)"
                },
            },
        },
    ),
]


# ── Implementação dos tools ───────────────────────────────────────────────────

_RED_FLAG_LABELS = {
    1: "Todos pagam meia parcela → arrecadação reduzida à metade",
    2: "Grupo com muitas cotas e poucos sorteios → % sorteado próximo de zero",
    3: "Taxa administrativa sobre crédito cheio com meia parcela → custo relativo dobrado",
    4: "Promessa de contemplação em 3–6 meses via sorteio → matematicamente improvável",
    5: "'Dobre seu crédito' com lance embutido de 50% → paga taxa sobre crédito cheio, recebe metade",
}


def _exec_auditar_grupo(
    cotas: int,
    prazo_meses: int,
    sorteios_por_mes: int,
    red_flags: list[int] | None = None,
    desvio_historico_pct: float | None = None,
) -> str:
    entregas_mes = cotas / prazo_meses
    pct_sorteado = (sorteios_por_mes * prazo_meses) / cotas * 100

    if pct_sorteado >= 50:
        avaliacao_sorteio, cor_sorteio = "Excelente — sorteio é caminho viável", "VERDE"
    elif pct_sorteado >= 30:
        avaliacao_sorteio, cor_sorteio = "Aceitável se complementado por lance", "AMARELO"
    elif pct_sorteado >= 10:
        avaliacao_sorteio, cor_sorteio = "Sorteio improvável — depender de lance", "AMARELO"
    else:
        avaliacao_sorteio, cor_sorteio = "Ruim — só com estratégia de lance agressiva", "VERMELHO"

    cor_historico = "INDEFINIDO"
    if desvio_historico_pct is not None:
        if desvio_historico_pct >= -10:
            cor_historico = "VERDE"
        elif desvio_historico_pct >= -30:
            cor_historico = "AMARELO"
        else:
            cor_historico = "VERMELHO"

    n_flags = len(red_flags) if red_flags else 0

    cores = {cor_sorteio, cor_historico}
    if "VERMELHO" in cores or n_flags >= 2:
        veredicto = "DESCARTAR"
    elif "AMARELO" in cores or n_flags == 1:
        veredicto = "MONITORAR — renegociar grupo ou buscar outra administradora"
    elif cor_historico == "INDEFINIDO":
        veredicto = "INCONCLUSIVO — solicitar histórico de contemplações antes de decidir"
    else:
        veredicto = "VERDE — pode entrar; calibrar estratégia de sorteio vs lance"

    linhas = [
        "## Auditoria do Grupo\n",
        f"**Cotas:** {cotas:,} | **Prazo:** {prazo_meses} meses | **Sorteios/mês:** {sorteios_por_mes}\n",
        "### Aritmética",
        f"- Entregas/mês esperadas: **{entregas_mes:.2f}**",
        f"- % sorteado: **{pct_sorteado:.1f}%** → {avaliacao_sorteio} `[{cor_sorteio}]`",
    ]

    if desvio_historico_pct is not None:
        linhas.append(
            f"- Desvio histórico real vs esperado: **{desvio_historico_pct:+.1f}%** `[{cor_historico}]`"
        )

    if red_flags:
        linhas.append("\n### Bandeiras Vermelhas Identificadas")
        for f in red_flags:
            linhas.append(f"- ⚠️ **Flag {f}:** {_RED_FLAG_LABELS.get(f, 'Bandeira desconhecida')}")
    elif n_flags == 0:
        linhas.append("\n### Bandeiras Vermelhas: nenhuma informada")

    linhas.append(f"\n### Veredicto: **{veredicto}**")
    return "\n".join(linhas)


def _exec_calcular_agio(
    parcelas_pagas: float,
    preco_venda: float,
    taxa_cessao: float = 0.0,
    meses_ate_contemplacao: int | None = None,
) -> str:
    agio_bruto = preco_venda - parcelas_pagas
    lucro_tributavel = agio_bruto - taxa_cessao
    ir = max(lucro_tributavel * 0.15, 0) if lucro_tributavel > 0 else 0.0
    agio_liquido = lucro_tributavel - ir

    rent_nominal = (agio_liquido / parcelas_pagas) * 100 if parcelas_pagas > 0 else 0.0

    linhas = [
        "## Cálculo de Ágio\n",
        f"| Item | Valor |",
        f"|---|---|",
        f"| Custo de aquisição (parcelas pagas) | R$ {parcelas_pagas:,.2f} |",
        f"| Preço de venda | R$ {preco_venda:,.2f} |",
        f"| Ágio bruto | R$ {agio_bruto:,.2f} |",
        f"| Taxa de cessão | R$ {taxa_cessao:,.2f} |",
        f"| IR (15% sobre lucro) | R$ {ir:,.2f} |",
        f"| **Ágio líquido** | **R$ {agio_liquido:,.2f}** |",
        f"| Rentabilidade nominal | {rent_nominal:.1f}% |",
    ]

    if meses_ate_contemplacao and meses_ate_contemplacao > 0:
        tir_anual = ((1 + rent_nominal / 100) ** (12 / meses_ate_contemplacao) - 1) * 100
        linhas.append(f"| TIR anualizada ({meses_ate_contemplacao} meses) | {tir_anual:.1f}% a.a. |")

    if agio_liquido <= 0:
        linhas.append("\n⚠️ **Ágio líquido negativo ou zero — operação sem retorno financeiro.**")
    elif rent_nominal >= 20:
        linhas.append(f"\n✅ Rentabilidade dentro da faixa típica de mercado (20%–50%).")
    else:
        linhas.append(f"\n⚠️ Rentabilidade abaixo da faixa típica (20%–50%) — avaliar custo de oportunidade vs CDI.")

    return "\n".join(linhas)


def _exec_calcular_gcap(
    preco_venda: float,
    custo_aquisicao: float,
    outras_vendas_no_mes: float = 0.0,
    mes_venda: int | None = None,
    ano_venda: int | None = None,
) -> str:
    total_alienado_mes = preco_venda + outras_vendas_no_mes
    ganho = preco_venda - custo_aquisicao

    isento = total_alienado_mes <= 35_000.0
    if ganho <= 0:
        ir_devido = 0.0
        situacao = "Sem ganho — não há imposto a recolher."
    elif isento:
        ir_devido = 0.0
        situacao = f"Isento (total alienado no mês: R$ {total_alienado_mes:,.2f} ≤ R$ 35.000)."
    else:
        # Alíquota progressiva
        if ganho <= 5_000_000:
            aliq = 0.15
        elif ganho <= 10_000_000:
            aliq = 0.175
        elif ganho <= 30_000_000:
            aliq = 0.20
        else:
            aliq = 0.225
        ir_devido = ganho * aliq
        situacao = f"Tributável — alíquota {aliq*100:.1f}%."

    linhas = [
        "## Apuração GCAP — Ganho de Capital\n",
        f"| Item | Valor |",
        f"|---|---|",
        f"| Preço de venda | R$ {preco_venda:,.2f} |",
        f"| Custo de aquisição | R$ {custo_aquisicao:,.2f} |",
        f"| Ganho de capital | R$ {ganho:,.2f} |",
        f"| Total alienado no mês | R$ {total_alienado_mes:,.2f} |",
        f"| **IR devido** | **R$ {ir_devido:,.2f}** |",
        f"\n**Situação:** {situacao}",
    ]

    if ir_devido > 0 and mes_venda and ano_venda:
        if mes_venda == 12:
            mes_darf, ano_darf = 1, ano_venda + 1
        else:
            mes_darf, ano_darf = mes_venda + 1, ano_venda
        linhas.append(
            f"\n**Prazo do DARF:** último dia útil de {mes_darf:02d}/{ano_darf} "
            f"(mês subsequente à venda — Lei 11.795/2008 + regulamentação GCAP)"
        )

    if not isento and ganho > 0:
        linhas.append(
            "\n💡 Dica: custo de aquisição inclui parcelas + taxas administrativas + lances pagos "
            "do bolso (excluindo lance embutido). Registre cada desembolso para reduzir a base."
        )

    return "\n".join(linhas)


def _exec_verificar_red_flags(
    cotas: int | None = None,
    prazo_meses: int | None = None,
    sorteios_por_mes: int | None = None,
    meia_parcela: bool = False,
    promessa_meses: int = 0,
    lance_embutido_pct: float = 0.0,
    taxa_sobre_credito_cheio: bool = False,
) -> str:
    flags_encontradas: list[str] = []

    if meia_parcela:
        flags_encontradas.append(f"🚩 **Flag 1** — {_RED_FLAG_LABELS[1]}")

    if cotas and prazo_meses and sorteios_por_mes:
        pct = (sorteios_por_mes * prazo_meses) / cotas * 100
        if pct < 10:
            flags_encontradas.append(
                f"🚩 **Flag 2** — {_RED_FLAG_LABELS[2]} (% sorteado calculado: {pct:.1f}%)"
            )

    if meia_parcela and taxa_sobre_credito_cheio:
        flags_encontradas.append(f"🚩 **Flag 3** — {_RED_FLAG_LABELS[3]}")

    if 0 < promessa_meses <= 6:
        flags_encontradas.append(
            f"🚩 **Flag 4** — {_RED_FLAG_LABELS[4]} (promessa: {promessa_meses} meses)"
        )

    if lance_embutido_pct >= 40:
        flags_encontradas.append(
            f"🚩 **Flag 5** — {_RED_FLAG_LABELS[5]} (embutido ofertado: {lance_embutido_pct:.0f}%)"
        )

    n = len(flags_encontradas)

    if n == 0:
        veredicto = "✅ Nenhuma bandeira detectada com os dados fornecidos. Prosseguir para auditoria completa do grupo."
    elif n == 1:
        veredicto = "⚠️ **MONITORAR** — uma bandeira presente. Renegociar grupo ou buscar outra oferta."
    else:
        veredicto = "🔴 **DESCARTAR** — duas ou mais bandeiras. Risco elevado de grupo deficitário ou oferta enganosa."

    linhas = ["## Verificação de Red Flags\n"]
    if flags_encontradas:
        linhas += flags_encontradas
    else:
        linhas.append("Nenhuma bandeira identificada.")

    linhas.append(f"\n**Veredicto: {veredicto}**")
    linhas.append(
        "\n> Referência: `specs/sinais-alerta-grupo.yaml` e `analise_metodo_jornada.md` §§3–5"
    )
    return "\n".join(linhas)


def _exec_comparar_investimentos(
    valor_credito: float,
    prazo_meses: int,
    taxa_adm_pct_ano: float = 1.5,
    cdi_anual_pct: float = 10.5,
    taxa_financiamento_anual_pct: float = 12.0,
) -> str:
    # Consórcio: taxa total de administração sobre o crédito
    taxa_adm_total_pct = taxa_adm_pct_ano * (prazo_meses / 12)
    custo_consorcio = valor_credito * (taxa_adm_total_pct / 100)

    # Renda fixa: quanto renderia o mesmo capital investido em parcelas no CDI
    parcela_consorcio = (valor_credito + custo_consorcio) / prazo_meses
    cdi_mensal = (1 + cdi_anual_pct / 100) ** (1 / 12) - 1
    valor_acumulado_renda_fixa = 0.0
    for _ in range(prazo_meses):
        valor_acumulado_renda_fixa = (valor_acumulado_renda_fixa + parcela_consorcio) * (1 + cdi_mensal)
    ganho_renda_fixa = valor_acumulado_renda_fixa - (parcela_consorcio * prazo_meses)

    # Financiamento: juros totais pela Tabela Price
    taxa_fin_mensal = (1 + taxa_financiamento_anual_pct / 100) ** (1 / 12) - 1
    if taxa_fin_mensal > 0:
        parcela_fin = valor_credito * (taxa_fin_mensal * (1 + taxa_fin_mensal) ** prazo_meses) / (
            (1 + taxa_fin_mensal) ** prazo_meses - 1
        )
    else:
        parcela_fin = valor_credito / prazo_meses
    total_financiamento = parcela_fin * prazo_meses
    juros_financiamento = total_financiamento - valor_credito

    linhas = [
        f"## Comparativo de Investimentos — R$ {valor_credito:,.0f} / {prazo_meses} meses\n",
        f"| Critério | Consórcio | Renda Fixa (CDI {cdi_anual_pct}%) | Financiamento ({taxa_financiamento_anual_pct}% a.a.) |",
        f"|---|---|---|---|",
        f"| Custo total | R$ {custo_consorcio:,.0f} | — | R$ {juros_financiamento:,.0f} (juros) |",
        f"| Parcela estimada | R$ {parcela_consorcio:,.0f}/mês | R$ {parcela_consorcio:,.0f}/mês | R$ {parcela_fin:,.0f}/mês |",
        f"| Acesso ao bem | Por sorteio/lance | Ao acumular o valor | Imediato |",
        f"| Liquidez | Baixa | Alta | Nula |",
        f"| Risco | Tempo de espera | Baixo | Inadimplência |",
        f"",
        f"**Se aplicar as parcelas do consórcio em renda fixa ({cdi_anual_pct}% a.a.) por {prazo_meses} meses:**",
        f"- Rendimento acumulado: R$ {ganho_renda_fixa:,.0f}",
        f"- Total acumulado: R$ {valor_acumulado_renda_fixa:,.0f}",
        f"",
        f"### Recomendação",
    ]

    if custo_consorcio < juros_financiamento * 0.5:
        linhas.append(
            "✅ **Consórcio vantajoso vs financiamento** — custo total significativamente menor. "
            "Ideal se o prazo de espera for aceitável para o objetivo."
        )
    elif custo_consorcio < juros_financiamento:
        linhas.append(
            "⚠️ **Consórcio mais barato, mas com prazo incerto.** "
            "Avaliar urgência de uso do bem — se urgente, financiamento pode ser necessário."
        )
    else:
        linhas.append(
            "⚠️ **Taxa de administração elevada** — avaliar outras administradoras ou "
            "considerar renda fixa se o objetivo for acumular capital sem urgência no bem."
        )

    return "\n".join(linhas)


def _exec_calcular_multiplas_cartas(
    numero_cartas: int,
    parcela_por_carta: float,
    valor_credito_por_carta: float = 100_000.0,
    pct_sorteado_grupo: float = 66.0,
    prazo_meses: int = 216,
    agio_pct: float = 25.0,
    incc_anual_pct: float = 6.0,
) -> str:
    parcela_total = numero_cartas * parcela_por_carta
    credito_total = numero_cartas * valor_credito_por_carta
    # Probabilidade mensal de cada carta ser sorteada
    prob_mensal_por_carta = (pct_sorteado_grupo / 100) / prazo_meses
    # Probabilidade de ao menos 1 ser sorteada em determinado mês
    prob_1_no_mes = 1 - (1 - prob_mensal_por_carta) ** numero_cartas
    # Mês esperado até a primeira contemplação (valor esperado)
    mes_esperado_1a = round(1 / prob_1_no_mes) if prob_1_no_mes > 0 else prazo_meses

    # Calcular lucro estimado para 3 cenários de contemplação usando a lógica do simulador
    incc = incc_anual_pct / 100
    def _lucro_no_mes(mes: int) -> tuple[float, float]:
        c, p, ti = valor_credito_por_carta, parcela_por_carta, 0.0
        for m in range(1, mes + 1):
            if m > 1 and (m - 1) % 12 == 0:
                c *= (1 + incc)
                p *= (1 + incc)
            ti += p
        lucro = c * (agio_pct / 100) - ti
        roi = lucro / ti * 100 if ti > 0 else 0.0
        return lucro, roi

    cenarios = [
        ("🟢 Cedo (3° ano)", 36),
        ("🟡 Médio (5° ano)", 60),
        ("🔴 Tarde (8° ano)", 96),
    ]

    # Efeito bola de neve: com o lucro da 1ª carta, quantas cartas extras por quanto tempo?
    lucro_cedo, _ = _lucro_no_mes(36)
    cartas_extras_4anos = max(0, int(lucro_cedo // (parcela_por_carta * 48)))
    meses_1_carta_extra = int(lucro_cedo // parcela_por_carta) if parcela_por_carta > 0 else 0

    linhas = [
        f"## Estratégia de Múltiplas Cartas — {numero_cartas} carta(s) de R$ {valor_credito_por_carta:,.0f}\n",
        "### Visão Geral",
        f"| Métrica | Valor |",
        f"|---|---|",
        f"| Aporte mensal total | R$ {parcela_total:,.0f}/mês |",
        f"| Crédito total em jogo | R$ {credito_total:,.0f} |",
        f"| Probabilidade mensal (ao menos 1 sorteio) | {prob_1_no_mes*100:.2f}% |",
        f"| **Fator de diversificação vs 1 carta** | **{numero_cartas}× mais chances** |",
        f"| Mês esperado da 1ª contemplação | ~{mes_esperado_1a}° mês |",
        f"| % sorteado do grupo | {pct_sorteado_grupo:.0f}% |",
        "",
        "### Lucro Estimado da 1ª Carta Contemplada por Cenário",
        "| Cenário | Mês | Total Investido | Lucro Líquido | ROI |",
        "|---|---|---|---|---|",
    ]
    for label, mes in cenarios:
        lucro, roi = _lucro_no_mes(mes)
        _, ti_ref = 0, 0
        c2, p2, ti2 = valor_credito_por_carta, parcela_por_carta, 0.0
        for m in range(1, mes + 1):
            if m > 1 and (m - 1) % 12 == 0:
                c2 *= (1 + incc); p2 *= (1 + incc)
            ti2 += p2
        sinal = "✅" if lucro > 0 else "🔴"
        linhas.append(f"| {label} | {mes}° | R$ {ti2:,.0f} | {sinal} R$ {lucro:,.0f} | {roi:.1f}% |")

    linhas += [
        "",
        f"### Efeito Bola de Neve (com lucro de contemplação no 3° ano)",
        f"- Lucro líquido estimado na 1ª venda (36° mês): **R$ {lucro_cedo:,.0f}**",
        f"- Com esse lucro, é possível financiar **1 carta extra** por até **{meses_1_carta_extra} meses** (parcela R$ {parcela_por_carta:.0f})",
    ]
    if cartas_extras_4anos >= 1:
        linhas.append(
            f"- Ou financiar **{cartas_extras_4anos} carta(s) extra(s)** por ~48 meses sem colocar dinheiro novo"
        )
    linhas.append(
        f"- Reinvestindo cada lucro em novas cartas: o número de cartas em andamento cresce sem aumentar o aporte próprio"
    )

    # Risk/recommendation
    linhas += [
        "",
        "### Recomendação",
    ]
    if pct_sorteado_grupo >= 50:
        linhas.append(
            f"✅ **Grupo adequado** ({pct_sorteado_grupo:.0f}% sorteado) + diversificação de {numero_cartas} cartas. "
            f"A probabilidade de contemplação cedo é favorável. Mantenha apenas o que pode pagar mensalmente (R$ {parcela_total:,.0f})."
        )
    elif pct_sorteado_grupo >= 20:
        linhas.append(
            f"⚠️ **Grupo razoável** ({pct_sorteado_grupo:.0f}% sorteado). Com {numero_cartas} cartas o risco de contemplação tardia diminui, "
            f"mas o período de lucro pode ser mais estreito. Valide o histórico de entregas do grupo."
        )
    else:
        linhas.append(
            f"🔴 **Grupo ruim** ({pct_sorteado_grupo:.0f}% sorteado) — mesmo com {numero_cartas} cartas, "
            f"a maioria das contemplações tende a cair no período final, onde o lucro é mínimo ou negativo. Busque outro grupo."
        )
    linhas.append(
        f"\n> **Regra de ouro:** nunca fazer mais cartas do que consegue pagar mensalmente por longo prazo. "
        f"Cancelamento antes da contemplação implica perda de ~50% dos valores pagos."
    )
    return "\n".join(linhas)


def _exec_simular_venda_carta(
    mes_contemplacao: int,
    valor_credito: float = 100_000.0,
    parcela: float = 338.0,
    prazo_meses: int = 220,
    agio_pct: float = 25.0,
    incc_anual_pct: float = 6.0,
    cdi_anual_pct: float = 14.2,
    taxa_adm_pct: float = 24.2,
    lance_embutido_parcelas: int = 44,
) -> str:
    if mes_contemplacao < 1 or mes_contemplacao > prazo_meses:
        return f"Erro: mês {mes_contemplacao} inválido para grupo com prazo de {prazo_meses} meses (1–{prazo_meses})."

    incc = incc_anual_pct / 100
    cdi_mensal = (1 + cdi_anual_pct / 100) ** (1 / 12) - 1
    # Lance embutido usa 44 parcelas do crédito CORRIGIDO pelo INCC: H = B × (1 − (1+taxa_adm)×parcelas/prazo)
    lance_factor = 1 - (1 + taxa_adm_pct / 100) * lance_embutido_parcelas / prazo_meses

    c = valor_credito
    p = parcela
    ti = 0.0
    cdi_acc = 0.0
    be_s: int | None = None
    be_l: int | None = None
    cdi_vence: int | None = None
    snap: dict = {}

    for m in range(1, prazo_meses + 1):
        if m > 1 and (m - 1) % 12 == 0:
            c *= (1 + incc)
            p *= (1 + incc)
        ti += p
        cdi_acc = (cdi_acc + p) * (1 + cdi_mensal)

        ll_s = c * (agio_pct / 100) - ti
        ll_l = c * lance_factor * (agio_pct / 100) - ti
        roi_s_m = ll_s / ti * 100
        roi_l_m = ll_l / ti * 100
        roi_cdi_m = (cdi_acc - ti) / ti * 100

        if m == mes_contemplacao:
            snap = {
                "ti": ti, "c": c,
                "ll_s": ll_s, "roi_s": roi_s_m,
                "credito_lance": c * lance_factor,
                "ll_l": ll_l, "roi_l": roi_l_m,
                "lucro_cdi": cdi_acc - ti, "roi_cdi": roi_cdi_m,
            }

        if be_l is None and ll_l < 0:
            be_l = m
        if be_s is None and ll_s < 0:
            be_s = m
        if cdi_vence is None and roi_cdi_m >= roi_s_m and roi_s_m >= 0:
            cdi_vence = m

        if m > mes_contemplacao and be_s is not None and be_l is not None and cdi_vence is not None:
            break

    ti = snap["ti"]
    c_mes = snap["c"]
    ll_s = snap["ll_s"]
    roi_s = snap["roi_s"]
    c_lance = snap["credito_lance"]
    ll_l = snap["ll_l"]
    roi_l = snap["roi_l"]
    lucro_cdi = snap["lucro_cdi"]
    roi_cdi = snap["roi_cdi"]

    def _zona(lucro: float, roi: float) -> str:
        if lucro <= 0:
            return "🔴 VERMELHA"
        if roi > 25:
            return "🟢 VERDE"
        return "🟡 AMARELA"

    zona_s = _zona(ll_s, roi_s)
    zona_l = _zona(ll_l, roi_l)

    if "VERMELHA" in zona_s and "VERMELHA" in zona_l:
        rec = "🔴 **NÃO VENDER** — ambos os cenários em prejuízo. Use o crédito para adquirir o bem diretamente."
    elif "VERDE" in zona_s and "VERDE" in zona_l:
        rec = "✅ **VENDER** — excelente momento. Ambos os cenários em zona verde com ROI sólido."
    elif "VERDE" in zona_s and "VERMELHA" in zona_l:
        rec = "✅ **SORTEIO: vender** — ROI sólido. 🔴 **LANCE EMBUTIDO: usar o crédito** — ultrapassou o break-even, a venda dará prejuízo."
    elif "AMARELA" in zona_s and "VERMELHA" in zona_l:
        rec = "⚠️ **SORTEIO: vender se urgente** — ainda lucrativo, mas margem estreita. 🔴 **LANCE: não vender** — em prejuízo."
    else:
        rec = "⚠️ **Avaliar urgência** — rentabilidade positiva, mas reduzida. Fechar rápido se decidir vender."

    linhas = [
        f"## Simulador Venda da Carta — {mes_contemplacao}° Mês\n",
        f"**Crédito:** R$ {valor_credito:,.0f} | **Parcela:** R$ {parcela:.0f} | "
        f"**Ágio:** {agio_pct:.0f}% | **INCC:** {incc_anual_pct:.0f}%a.a. | **CDI:** {cdi_anual_pct:.1f}%a.a.",
        f"**Crédito no {mes_contemplacao}° mês** (após correção INCC): R$ {c_mes:,.0f}\n",
        "### Resultado no Mês de Contemplação",
        "| Cenário | Total Investido | Lucro Bruto | Lucro Líquido | ROI | Zona |",
        "|---|---|---|---|---|---|",
        f"| 🎯 **Sorteio** | R$ {ti:,.0f} | R$ {c_mes * (agio_pct / 100):,.0f} | R$ {ll_s:,.0f} | {roi_s:.1f}% | {zona_s} |",
        f"| 🔵 **Lance Embutido** | R$ {ti:,.0f} | R$ {c_lance * (agio_pct / 100):,.0f} | R$ {ll_l:,.0f} | {roi_l:.1f}% | {zona_l} |",
        f"| 📈 **CDI** ({cdi_anual_pct}%a.a.) | R$ {ti:,.0f} | R$ {lucro_cdi:,.0f} | — | {roi_cdi:.1f}% | — |",
        "",
        "### Break-even e Cruzamentos",
    ]

    if be_l is not None:
        dist = mes_contemplacao - be_l
        nota = f" ← **{abs(dist)} mês(es) {'após' if dist >= 0 else 'antes do'} break-even**" if abs(dist) <= 6 else ""
        linhas.append(f"- **Lance Embutido:** lucrativo até o {be_l - 1}°, prejuízo a partir do **{be_l}° mês**{nota}")
    if be_s is not None:
        dist = mes_contemplacao - be_s
        nota = f" ← **{abs(dist)} mês(es) {'após' if dist >= 0 else 'antes do'} break-even**" if abs(dist) <= 6 else ""
        linhas.append(f"- **Sorteio:** lucrativo até o {be_s - 1}°, prejuízo a partir do **{be_s}° mês**{nota}")
    if cdi_vence is not None:
        linhas.append(f"- **CDI supera o Sorteio** a partir do **{cdi_vence}° mês** ({cdi_anual_pct}%a.a.)")

    linhas.append(f"\n### Recomendação\n{rec}")
    return "\n".join(linhas)


# ── Dispatcher de tools ───────────────────────────────────────────────────────

def execute_tool(name: str, inputs: dict) -> str:
    try:
        if name == "auditar_grupo":
            return _exec_auditar_grupo(**inputs)
        if name == "calcular_agio":
            return _exec_calcular_agio(**inputs)
        if name == "calcular_gcap":
            return _exec_calcular_gcap(**inputs)
        if name == "verificar_red_flags":
            return _exec_verificar_red_flags(**inputs)
        if name == "comparar_investimentos":
            return _exec_comparar_investimentos(**inputs)
        if name == "calcular_multiplas_cartas":
            return _exec_calcular_multiplas_cartas(**inputs)
        if name == "simular_venda_carta":
            return _exec_simular_venda_carta(**inputs)
        return f"Tool desconhecida: {name}"
    except Exception as e:
        return f"Erro ao executar '{name}': {type(e).__name__}: {e}"


# ── Helpers de API ────────────────────────────────────────────────────────────

def get_api_key(key_name: str) -> str:
    """Busca chave de API em st.secrets (Streamlit Cloud) ou variáveis de ambiente (local)."""
    try:
        return st.secrets[key_name]
    except KeyError:
        api_key = os.environ.get(key_name)
        if not api_key:
            st.error(f"❌ {key_name} não encontrada. Configure em Secrets do Streamlit Cloud ou no arquivo .env")
            st.stop()
        return api_key


def get_client(model: str) -> OpenAI:
    if model.startswith("groq/"):
        api_key = get_api_key("GROQ_API_KEY")
        return OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)

    api_key = get_api_key("OPEN_ROUTER")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)


def chat(client: OpenAI, messages: list[dict], model: str, temperature: float = 0.3) -> tuple[str, list[dict]]:
    tool_log: list[dict] = []
    api_model = model.removeprefix("groq/")
    full_messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    while True:
        response = client.chat.completions.create(
            model=api_model,
            messages=full_messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=config.MAX_TOKENS,
            temperature=temperature,
        )

        choice = response.choices[0]
        msg = choice.message

        if choice.finish_reason == "stop" or not msg.tool_calls:
            text = msg.content or ""
            messages.append({"role": "assistant", "content": text})
            return text, tool_log

        assistant_dict: dict = {
            "role": "assistant",
            "content": msg.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ],
        }
        messages.append(assistant_dict)
        full_messages.append(assistant_dict)

        for tc in msg.tool_calls:
            inputs = json.loads(tc.function.arguments)
            tool_log.append({"name": tc.function.name, "input": inputs})
            result = execute_tool(tc.function.name, inputs)
            tool_result = {"role": "tool", "tool_call_id": tc.id, "content": result}
            messages.append(tool_result)
            full_messages.append(tool_result)


# ── Guia de Funcionalidades ───────────────────────────────────────────────────

def _render_guia() -> None:
    st.markdown("## 📚 Guia de Funcionalidades")
    st.markdown(
        "O **ClaudeConsórcios** combina um assistente de linguagem natural com cinco ferramentas "
        "de cálculo especialistas no mercado brasileiro de consórcios. "
        "Basta descrever seu caso no chat — o assistente identifica automaticamente qual ferramenta usar."
    )

    st.divider()

    with st.expander("🔍 Auditar Grupo — saiba se o grupo é saudável antes de assinar", expanded=True):
        st.markdown(
            """
**O que faz:** Calcula a aritmética do grupo e classifica como Verde / Amarelo / Vermelho.

**Fórmulas aplicadas:**
- `entregas/mês = cotas ÷ prazo (meses)`
- `% sorteado = (sorteios/mês × prazo) ÷ cotas × 100`

| % sorteado | Avaliação |
|---|---|
| ≥ 50% | Verde — sorteio é caminho viável |
| 30–49% | Amarelo — complementar com lance |
| 10–29% | Amarelo — sorteio improvável |
| < 10% | Vermelho — grupo deficitário |

**Quando usar:** Antes de assinar qualquer contrato. Se o corretor recusar fornecer cotas, prazo e histórico, isso já é sinal de alerta.

**Exemplo de pergunta:**
> *"Um grupo tem 2.000 cotas, prazo de 180 meses e 1 sorteio por mês. Vale a pena entrar?"*
"""
        )

    with st.expander("💰 Calcular Ágio — rentabilidade real do trade de carta contemplada"):
        st.markdown(
            """
**O que faz:** Calcula ágio bruto, desconta taxa de cessão e IR (15%), e entrega a rentabilidade nominal e a TIR anualizada.

**Fórmulas aplicadas:**
```
ágio bruto   = preço de venda − parcelas pagas
ágio líquido = ágio bruto − taxa de cessão − IR (15%)
TIR anual    = (1 + rent. nominal) ^ (12 / meses) − 1
```

**Referência de mercado:** rentabilidade típica de **20% a 50%** sobre o capital investido em contemplações rápidas (Relatório de Pesquisa §6).

**Quando usar:** Ao receber uma oferta de cota contemplada ou ao anunciar a sua para calcular o preço justo.

**Exemplo de pergunta:**
> *"Paguei R$ 50.000 em parcelas, vendo por R$ 80.000 com taxa de cessão de R$ 500. Qual o lucro líquido?"*
"""
        )

    with st.expander("📅 Simulador Venda da Carta — decida o momento certo para vender"):
        st.markdown(
            """
**O que faz:** Simula a rentabilidade da venda de uma carta contemplada em qualquer mês do grupo,
usando o modelo da planilha Ademicon ("Venda da Carta com Lucro"). Compara três cenários —
Sorteio, Lance Embutido e CDI benchmark — e classifica o momento como **VERDE / AMARELA / VERMELHA**.

**Os 3 cenários simulados:**

| Cenário | Como funciona | O que calcula |
|---|---|---|
| 🎯 **Sorteio** | Crédito cheio × ágio − total investido | Lucro líquido e ROI se contemplado por sorteio |
| 🔵 **Lance Embutido** | Crédito reduzido (44 parcelas antecipadas) × ágio − total investido | ROI com crédito efetivo ~25% menor |
| 📈 **CDI** | Parcelas aplicadas a juros compostos | Benchmark: quanto renderia investir as mesmas parcelas |

**Regra INCC:** crédito e parcela são corrigidos em +6% a cada 12 meses — o crédito no 91° mês já é
~R$ 143.000, não R$ 100.000. O simulador aplica isso automaticamente.

**Lance Embutido — por que o crédito encolhe:**
```
parcela_original = R$ 100.000 × (1 + 24,2%) ÷ 220 = R$ 564,55
crédito_efetivo  = R$ 100.000 − R$ 564,55 × 44 = ~R$ 75.160
```
Você paga taxa administrativa sobre R$ 100.000, mas o crédito disponível para venda é só R$ 75.160.

**Pontos de break-even (parâmetros padrão Ademicon):**

| Modalidade | Último mês lucrativo | Primeiro mês de prejuízo |
|---|---|---|
| Lance Embutido | 65° mês (ROI +0,1%) | **66° mês** (ROI −1,7%) |
| Sorteio | 90° mês (ROI +1,3%) | **91° mês** (ROI −0,03%) |
| CDI supera ambos | — | **~63° mês** |

**Zonas de decisão:**

| Zona | Período | Recomendação |
|---|---|---|
| 🟢 **VERDE** | Até o 48° mês | Vender sem hesitar — ROI acima de 26% |
| 🟡 **AMARELA** | 49°–65° (Lance) / 49°–90° (Sorteio) | Ainda lucrativo; fechar rápido se decidir |
| 🔴 **VERMELHA** | 66°+ (Lance) / 91°+ (Sorteio) | Não vender — usar o crédito diretamente |

**Marcos quantitativos de referência (parâmetros padrão):**

| Mês | Total Pago | ROI Sorteio | ROI Lance | ROI CDI |
|---|---|---|---|---|
| 1° | R$ 338 | 7.296% | 5.459% | ~1% |
| 12° | R$ 4.056 | 516% | 363% | 6,3% |
| 48° | R$ 17.743 | 68% | 26% | 24,4% |
| 60° | R$ 22.864 | 38% | 3,8% | 29,6% |
| 66° | R$ 25.578 | 30,8% | **−1,7%** | 32,1% |
| 91° | R$ 37.603 | **−0,03%** | −24,9% | 41,6% |

**Quando usar:** Ao ser contemplado e precisar decidir entre vender a carta (lucrar o ágio)
ou usar o crédito para adquirir o bem. O mês de contemplação é o fator determinante.

**Parâmetros personalizáveis:** valor do crédito, parcela, prazo, % de ágio, INCC, CDI, taxa adm e parcelas do lance embutido.

**Exemplos de pergunta:**
> *"Fui contemplado no 45° mês em um grupo Ademicon de R$ 100k. Vale vender a carta?"*

> *"Tenho uma carta Ademicon, fui contemplado no 70° mês. Ainda dá lucro vender?"*

> *"Grupo de R$ 200k, parcela R$ 700, contemplei no 30° mês, ágio atual de 20%. Simula pra mim."*
"""
        )

    with st.expander("🧾 Calcular IR (GCAP) — apure o imposto e o prazo do DARF"):
        st.markdown(
            """
**O que faz:** Apura o Ganho de Capital (programa GCAP da Receita Federal), verifica a isenção de R$ 35.000/mês e calcula o valor do DARF com prazo correto.

**Regras aplicadas:**
| Situação | Regra |
|---|---|
| Vendas ≤ R$ 35.000 no mês | Isento — sem DARF |
| Lucro até R$ 5 milhões | Alíquota de 15% |
| Lucro R$ 5M–R$ 10M | Alíquota de 17,5% |
| Lucro R$ 10M–R$ 30M | Alíquota de 20% |
| Lucro acima de R$ 30M | Alíquota de 22,5% |

**Prazo do DARF:** último dia útil do mês seguinte à venda.

**Custo de aquisição inclui:** parcelas + taxas administrativas + lances pagos do bolso.
**Não inclui:** lance embutido (parte do crédito futuro — não é desembolso real).

**Quando usar:** Logo após fechar a venda de uma cota contemplada, antes do vencimento do DARF.

**Exemplo de pergunta:**
> *"Vendi uma cota em maio/2026 por R$ 90.000. Paguei R$ 60.000 em parcelas e taxas. Qual o IR e o prazo?"*
"""
        )

    with st.expander("⚠️ Verificar Red Flags — identifique armadilhas em ofertas"):
        st.markdown(
            """
**O que faz:** Analisa os dados da oferta contra as 5 bandeiras vermelhas mais comuns no mercado, baseadas na análise crítica do "Método da Jornada" (Megacombo) e do Guia de Mitigação de Riscos.

**As 5 red flags:**

| # | Bandeira | Por quê é problema |
|---|---|---|
| 1 | Todos pagam meia parcela | Arrecadação cai pela metade — grupo não financia as contemplações normalmente |
| 2 | Milhares de cotas com 1 sorteio/mês | % sorteado próximo de zero — contemplação por sorteio é praticamente impossível |
| 3 | Taxa sobre crédito cheio com meia parcela | Você paga taxa dobrada em relação ao crédito que efetivamente recebe |
| 4 | Promessa de contemplação em 3–6 meses via sorteio | Matematicamente impossível na maioria dos grupos |
| 5 | "Dobre seu crédito" com 50% de lance embutido | Você paga taxa sobre R$ 1M para alavancar R$ 500k — a vantagem é ilusória |

**Veredicto:** 0 flags = Verde · 1 flag = Amarelo (negociar) · 2+ flags = Vermelho (descartar).

**Quando usar:** Ao receber qualquer proposta de corretor ou vendedor de consórcio.

**Exemplo de pergunta:**
> *"O vendedor prometeu contemplação em 6 meses e mencionou lance embutido de 50%. Tem problema?"*
"""
        )

    with st.expander("🎯 Estratégia do Método — Múltiplas Cartas, Bola de Neve e Critérios de Escolha"):
        st.markdown(
            """
**O que é:** A estratégia de múltiplas cartas pequenas em vez de uma carta grande, popularizada pelo
"Método Jornada da Tranquilidade Financeira" — base para maximizar lucro e reduzir dependência da sorte.

---

#### Por que várias cartas menores?

| Abordagem | Cartas | Aporte/mês | Probabilidade de contemplação |
|---|---|---|---|
| 1 carta de R$ 500k | 1 | R$ 3.220 | 1× |
| 5 cartas de R$ 100k | 5 | R$ 3.220 | **5×** |

O aporte mensal é o mesmo, mas 5 cartas têm 5× mais chances de contemplação.
Cada carta que contempla é vendida com lucro — sem esperar todas.

---

#### Efeito Bola de Neve

```
Início: 5 cartas  →  1ª contempla (mês 10)  →  vende por R$ 30k
                                            ↓
                        Reinveste: paga 2 cartas extras com o lucro
                                            ↓
                        Agora: 6–7 cartas em andamento sem aporte extra
                                            ↓
                        2ª contempla (mês 18)  →  R$ 30k+ reinvestido...
```

O ciclo se acelera: lucros das primeiras cartas financiam novas cartas — sem aumentar o aporte próprio.

---

#### 3 Critérios para Escolha da Administradora

| Critério | O que verificar | Por que importa |
|---|---|---|
| **1. Junção entre grupos diferentes** | A administradora permite unir créditos de grupos distintos? | Sem isso, não dá para montar créditos maiores para compradores |
| **2. Volume de cartas no mercado** | Há dezenas/centenas de cartas contempladas por mês? | Precisam existir outras cartas para juntar com a sua |
| **3. Máximo de usos permitidos** | Novo, usado, construção, reforma e terreno? | Mais usos = mais compradores potenciais = mais liquidez |

> ⚠️ A **taxa de administração** não é o critério determinante. O que importa é contemplar
> cedo em grupo bom e ter liquidez para vender. Taxas aparentemente menores muitas vezes
> escondem cobranças (fundo reserva, taxa de adesão) ou vêm de grupos com métricas ruins.

---

#### Regras Operacionais

**NÃO dar lance em carta destinada à venda**
O lance antecipa pagamentos ao grupo e reduz a margem. Cota para trade = aguardar sorteio ou usar lance livre de outros como combustível para o grupo.

**FGTS não permite venda da carta**
Se você usar FGTS no consórcio, é obrigatório comprar o imóvel — a carta fica ilíquida para trade.

**Cancelamento = ~50% de perda**
Se cancelar antes de contemplar: perda de ~50%+ dos valores amortizados (descontada a taxa adm paga) + multa + taxa de reposição + aguarda sorteio como "cancelado" para receber de volta.
Regra: só faça o número de cartas que consegue pagar mensalmente por longo prazo.

**Seguro prestamista**
Geralmente incluído na prestação. Em caso de falecimento ou invalidez permanente, quita o saldo devedor de todas as cartas. Recomendável manter.

---

#### Estratégia por Período de Contemplação

| Período | Estratégia recomendada |
|---|---|
| Até o 6° ano (72 meses) | Vender carta com lucro → reinvestir (bola de neve) |
| 7°–13° ano | Usar crédito para imóvel com aluguel pagando o saldo; OU deixar investido em renda fixa rendendo sobre capital acumulado |
| Acima do 13° ano | Crédito corrigido pelo INCC ainda supera total pago — use o crédito diretamente |

---

#### Preço de Venda da Carta Contemplada

A carta é precificada como crédito com CET equivalente a **7%–8% a.a.** (~0,6%/mês) — mais barato que
qualquer financiamento bancário. Isso gera demanda estrutural permanente de compradores.

Comprador típico: quem quer imóvel mas tem dificuldade de comprovar renda para financiamento
(parcela do consórcio é menor), quem não quer se descapitalizar pagando à vista,
e quem precisa de crédito para construção, reforma ou terreno.

---

#### Exemplo de Pergunta

> *"Tenho R$ 3.000/mês para investir em consórcio. Quantas cartas devo fazer e qual o efeito da diversificação?"*

> *"Se eu vender minha primeira carta por R$ 30.000, quantas cartas extras consigo pagar com esse lucro?"*

> *"Fui contemplado no 70° mês. Vale a pena vender ou usar o crédito?"*
"""
        )

    with st.expander("📊 Comparar Investimentos — consórcio vs renda fixa vs financiamento"):
        st.markdown(
            """
**O que faz:** Coloca os três caminhos lado a lado para o mesmo objetivo financeiro, calculando custo total, parcela estimada e, para renda fixa, o montante acumulado se as parcelas fossem aplicadas no CDI.

**O que é comparado:**

| Critério | Consórcio | Renda Fixa (CDI) | Financiamento (Price) |
|---|---|---|---|
| Custo | Taxa adm (sem juros) | Zero — você recebe | Juros bancários (maiores custo) |
| Acesso ao bem | Por sorteio ou lance | Após acumular o valor | Imediato |
| Liquidez | Baixa | Alta | Nula |
| Risco | Tempo de espera | Baixo | Inadimplência |

**Quando usar:**
- Planejando comprar imóvel, veículo ou bem de alto valor
- Comparando se vale mais a pena consórcio ou investir o dinheiro no Tesouro/CDB
- Avaliando urgência: se precisa do bem agora, financiamento pode ser necessário mesmo sendo mais caro

**Exemplo de pergunta:**
> *"Quero comprar um imóvel de R$ 500.000 em 10 anos. Compensa consórcio ou financiamento?"*
"""
        )

    st.divider()

    st.markdown("### ⚙️ Ferramentas de Cálculo — Quando São Acionadas Automaticamente")
    st.info(
        "O assistente aciona as ferramentas **automaticamente** quando você fornece os dados necessários na conversa. "
        "Você não precisa saber o nome da ferramenta — basta descrever seu caso com números."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dados que acionam cada ferramenta:**")
        st.markdown(
            """
- **Auditar grupo** → cotas + prazo + sorteios/mês
- **Calcular ágio** → parcelas pagas + preço de venda
- **Calcular GCAP** → preço de venda + custo de aquisição
- **Verificar red flags** → dados da oferta recebida
- **Comparar** → valor do crédito + prazo
"""
        )
    with col2:
        st.markdown("**O que o assistente entrega:**")
        st.markdown(
            """
- Cálculos detalhados com tabelas
- Veredicto claro (Verde / Amarelo / Vermelho)
- Recomendação de ação
- Alertas jurídicos relevantes (Lei 11.795, BCB, ABAC)
- Prazo e valor do DARF quando aplicável
"""
        )

    st.divider()

    st.markdown("### 📌 Regras de Ouro do Mercado de Consórcios")
    st.warning(
        "**NUNCA** pague o ágio antes da anuência expressa da administradora registrada no sistema. "
        "Sem esse passo, a cessão não vincula a administradora — e você perde o dinheiro sem recurso jurídico eficaz."
    )
    st.markdown(
        """
1. Exija histórico de contemplações por escrito antes de assinar
2. Confirme autorização da administradora no portal do **Banco Central**
3. Pague o ágio via TED/PIX rastreável — nunca em dinheiro vivo
4. Lance embutido é **forma de pagamento**, não alavancagem — não confunda
5. Guarde todos os comprovantes de desembolso para reduzir a base do GCAP
"""
    )


# ── Histórico de Interações ───────────────────────────────────────────────────

def _render_historico(messages: list[dict]) -> None:
    st.markdown("## 🕐 Histórico de Interações")

    interacoes = [m for m in messages if m["role"] in ("user", "assistant")]
    if not interacoes:
        st.info("Nenhuma interação registrada nesta sessão. Inicie uma conversa na aba Chat.")
        return

    total_user = sum(1 for m in interacoes if m["role"] == "user")
    total_tools = sum(len(m.get("tool_log", [])) for m in interacoes if m["role"] == "assistant")

    col1, col2, col3 = st.columns(3)
    col1.metric("Mensagens", len(interacoes))
    col2.metric("Perguntas", total_user)
    col3.metric("Cálculos executados", total_tools)

    st.divider()

    pares: list[tuple[dict, dict | None]] = []
    i = 0
    while i < len(interacoes):
        if interacoes[i]["role"] == "user":
            pergunta = interacoes[i]
            resposta = interacoes[i + 1] if i + 1 < len(interacoes) and interacoes[i + 1]["role"] == "assistant" else None
            pares.append((pergunta, resposta))
            i += 2 if resposta else 1
        else:
            i += 1

    for idx, (pergunta, resposta) in enumerate(reversed(pares), 1):
        n = len(pares) - idx + 1
        ferramentas = resposta.get("tool_log", []) if resposta else []
        label = f"**#{n}** — {pergunta['content'][:80]}{'…' if len(pergunta['content']) > 80 else ''}"
        if ferramentas:
            label += f"  🔧 *{len(ferramentas)} cálculo(s)*"

        with st.expander(label):
            st.markdown("**Pergunta:**")
            st.markdown(f"> {pergunta['content']}")

            if resposta:
                st.markdown("**Resposta:**")
                st.markdown(resposta["content"])

                if ferramentas:
                    st.markdown("**Cálculos executados:**")
                    for t in ferramentas:
                        st.code(
                            f"{t['name']}({json.dumps(t['input'], ensure_ascii=False, indent=2)})",
                            language="python",
                        )
            else:
                st.warning("Resposta não disponível.")

    st.divider()
    if st.button("📋 Copiar histórico como texto", key="copy_hist"):
        linhas = []
        for idx, (p, r) in enumerate(pares, 1):
            linhas.append(f"## Interação {idx}")
            linhas.append(f"**Pergunta:** {p['content']}")
            if r:
                linhas.append(f"**Resposta:** {r['content']}")
            linhas.append("")
        st.text_area("Histórico em texto:", value="\n".join(linhas), height=300, key="hist_text")


# ── UI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "quick_action" not in st.session_state:
        st.session_state.quick_action = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "selected_model_name" not in st.session_state:
        st.session_state.selected_model_name = "💎 Gemini 2.0 Flash"
    if "temperatura" not in st.session_state:
        st.session_state.temperatura = 0.0

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.title("🏠 ClaudeConsórcios")
        st.caption("Especialista em Consórcios e Trade de Cartas Contempladas")

        st.divider()

        st.markdown("### Modelo LLM")
        selected_model_name = st.selectbox(
            "Escolha o modelo:",
            options=list(MODELOS.keys()),
            index=list(MODELOS.keys()).index(st.session_state.selected_model_name),
            key="model_selector",
        )
        st.session_state.selected_model_name = selected_model_name
        selected_model = MODELOS[selected_model_name]

        st.markdown("### Temperatura")
        temperatura = st.slider(
            "Criatividade / precisão:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperatura,
            step=0.05,
            key="temp_slider",
            help=(
                "0.0 = respostas determinísticas e precisas (ideal para cálculos)\n"
                "0.5 = equilíbrio entre precisão e fluidez\n"
                "1.0 = respostas mais criativas e variadas"
            ),
        )
        st.session_state.temperatura = temperatura
        _label_temp = "🎯 Preciso" if temperatura <= 0.2 else ("⚖️ Equilibrado" if temperatura <= 0.6 else "🎨 Criativo")
        st.caption(f"{_label_temp} — temperatura {temperatura:.2f}")

        st.divider()

        st.markdown("### Ações Rápidas")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Auditar Grupo", use_container_width=True):
                st.session_state.quick_action = (
                    "Me ajude a auditar um grupo de consórcio. "
                    "Preciso informar: número de cotas, prazo em meses e sorteios por mês."
                )
        with col2:
            if st.button("💰 Calcular Ágio", use_container_width=True):
                st.session_state.quick_action = (
                    "Quero calcular o ágio e a rentabilidade de um trade de carta contemplada. "
                    "O que preciso informar?"
                )

        col3, col4 = st.columns(2)
        with col3:
            if st.button("🧾 Calcular IR", use_container_width=True):
                st.session_state.quick_action = (
                    "Vendi uma cota contemplada e preciso calcular o imposto de renda (GCAP). "
                    "Me ajude a apurar o valor e o prazo do DARF."
                )
        with col4:
            if st.button("⚡ Red Flags", use_container_width=True):
                st.session_state.quick_action = (
                    "Recebi uma oferta de consórcio e quero verificar se há sinais de alerta. "
                    "Pode me ajudar a identificar red flags?"
                )

        col5, col6 = st.columns(2)
        with col5:
            if st.button("📊 Comparar", use_container_width=True):
                st.session_state.quick_action = (
                    "Quero comparar consórcio com renda fixa e financiamento bancário. "
                    "Me ajude a entender as diferenças para meu caso."
                )
        with col6:
            if st.button("📖 Como funciona", use_container_width=True):
                st.session_state.quick_action = (
                    "Explique como funciona o trade de cartas contempladas no Brasil: "
                    "do início até a liquidação fiscal."
                )

        st.divider()

        st.markdown("### Exemplos de Perguntas")
        st.markdown(
            """
- *Um grupo tem 2.000 cotas, prazo 180 meses e 1 sorteio/mês. Vale a pena?*
- *Paguei R$50k em parcelas e vendo por R$80k. Qual o ágio líquido?*
- *Vendi uma cota por R$90k e paguei R$60k. Qual o IR?*
- *O corretor prometeu contemplação em 6 meses. É confiável?*
- *Consórcio ou financiamento para um imóvel de R$500k?*
- *O que é lance embutido e por que é uma armadilha?*
- *Quais administradoras são confiáveis no Brasil?*
"""
        )

        st.divider()

        if st.button("🗑️ Limpar conversa", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

        st.divider()
        st.markdown("**Ferramentas disponíveis**")
        st.markdown("🔍 Auditar grupo (aritmética)")
        st.markdown("💰 Calcular ágio bruto/líquido")
        st.markdown("🧾 Apurar GCAP / DARF")
        st.markdown("⚠️ Verificar red flags")
        st.markdown("📊 Comparar investimentos")
        st.caption(f"Modelo: {selected_model_name}  \nData: {datetime.now().strftime('%d/%m/%Y')}")

    # ── Header ────────────────────────────────────────────────────────────────
    st.title("🏠 ClaudeConsórcios — Especialista em Consórcios")
    st.caption(
        "Análise de grupos, cálculo de ágio, apuração de GCAP, verificação de red flags "
        "e comparativo com renda fixa e financiamento — com base na Lei 11.795/2008, ABAC e Banco Central."
    )

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_chat, tab_guia, tab_hist = st.tabs(["💬 Chat", "📚 Guia de Funcionalidades", "🕐 Histórico"])

    with tab_guia:
        _render_guia()

    with tab_hist:
        _render_historico(st.session_state.messages)

    with tab_chat:
        if not st.session_state.messages:
            with st.chat_message("assistant"):
                st.markdown(
                    "Olá! Sou o **ClaudeConsórcios**, seu especialista em consórcios brasileiros e "
                    "trade de cartas contempladas.\n\n"
                    "Posso te ajudar com:\n"
                    "- 🔍 **Auditar grupos** — calcular % sorteado, entregas/mês e identificar grupos deficitários\n"
                    "- 💰 **Calcular ágio** — bruto, líquido (após IR) e rentabilidade anualizada\n"
                    "- 🧾 **Apurar GCAP/IR** — ganho de capital, isenção de R$35k, prazo do DARF\n"
                    "- ⚠️ **Verificar red flags** — sinais de alerta em ofertas e contratos\n"
                    "- 📊 **Comparar alternativas** — consórcio vs renda fixa vs financiamento\n"
                    "- 📋 **Explicar o processo** — do trade completo às regras jurídicas (Lei 11.795/2008)\n\n"
                    "Como posso ajudar? Pode descrever seu caso ou usar os botões rápidos na barra lateral."
                )

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("tool_log"):
                    with st.expander(f"🔧 {len(msg['tool_log'])} cálculo(s) executado(s)"):
                        for t in msg["tool_log"]:
                            st.code(
                                f"{t['name']}({json.dumps(t['input'], ensure_ascii=False, indent=2)})",
                                language="python",
                            )

        user_input = st.chat_input("Descreva seu caso ou faça uma pergunta sobre consórcios...")

        if st.session_state.quick_action:
            user_input = st.session_state.quick_action
            st.session_state.quick_action = None

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.chat_messages.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                with st.spinner("Analisando..."):
                    try:
                        client = get_client(selected_model)
                        response_text, tool_log = chat(
                            client,
                            st.session_state.chat_messages,
                            selected_model,
                            temperature=st.session_state.temperatura,
                        )
                    except Exception as e:
                        response_text = f"Erro ao comunicar com a API: {type(e).__name__}: {e}"
                        tool_log = []

                st.markdown(response_text)

                if tool_log:
                    with st.expander(f"🔧 {len(tool_log)} cálculo(s) executado(s)"):
                        for t in tool_log:
                            st.code(
                                f"{t['name']}({json.dumps(t['input'], ensure_ascii=False, indent=2)})",
                                language="python",
                            )

            st.session_state.messages.append(
                {"role": "assistant", "content": response_text, "tool_log": tool_log}
            )


if __name__ == "__main__":
    main()
