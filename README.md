# ClaudeConsórcios — Especialista em Consórcios e Trade de Cartas Contempladas

> Assistente especializado em análise de grupos de consórcio, cálculo de ágio, apuração fiscal e verificação de riscos no mercado brasileiro de consórcios

**Status:** Em produção | **Linguagem:** Python 3.11+ | **Framework:** Streamlit | **Modelos:** Groq + OpenRouter

---

## O que é

**ClaudeConsórcios** é uma aplicação Streamlit que combina um assistente de IA com cinco ferramentas de cálculo especializadas no mercado de consórcios brasileiro. Utilize-a para:

- **Auditar grupos de consórcio** — validar aritmética, calcular % sorteado e identificar grupos deficitários
- **Calcular ágio** — bruto, líquido (após IR) e rentabilidade anualizada do trade de cartas contempladas
- **Apurar GCAP** — ganho de capital, isenção de R$ 35.000/mês, alíquota progressiva e prazo do DARF
- **Verificar red flags** — identificar 5 bandeiras vermelhas comuns em ofertas enganosas
- **Comparar investimentos** — consórcio vs renda fixa (CDI) vs financiamento bancário

O assistente aciona automaticamente as ferramentas quando você fornece dados suficientes — não é necessário saber o nome da ferramenta. Basta descrever seu caso em linguagem natural.

---

## Funcionalidades Principais

### 🔍 Auditar Grupo

Calcula a aritmética do grupo e classifica como **Verde / Amarelo / Vermelho**.

**Fórmulas:**
```
entregas/mês = cotas ÷ prazo (meses)
% sorteado = (sorteios/mês × prazo) ÷ cotas × 100
```

**Classificação:**
| % Sorteado | Avaliação |
|---|---|
| ≥ 50% | Verde — sorteio é caminho viável |
| 30–49% | Amarelo — complementar com lance |
| 10–29% | Amarelo — sorteio improvável |
| < 10% | Vermelho — grupo deficitário |

### 💰 Calcular Ágio

Computa ágio bruto, desconta taxa de cessão e IR (15%), entrega rentabilidade nominal e TIR anualizada.

**Fórmulas:**
```
ágio bruto   = preço de venda − parcelas pagas
ágio líquido = ágio bruto − taxa de cessão − IR (15%)
TIR anual    = (1 + rent. nominal) ^ (12 / meses) − 1
```

**Referência de mercado:** rentabilidade típica **20% a 50%** sobre capital investido em contemplações rápidas.

### 🧾 Calcular GCAP (IR)

Apura o Ganho de Capital segundo programa GCAP da Receita Federal. Verifica isenção de R$ 35.000/mês, aplica alíquota progressiva e calcula prazo do DARF.

**Regras:**
| Situação | Alíquota |
|---|---|
| Vendas ≤ R$ 35.000/mês | Isento — sem DARF |
| Lucro até R$ 5 mi | 15% |
| Lucro R$ 5–10 mi | 17,5% |
| Lucro R$ 10–30 mi | 20% |
| Lucro > R$ 30 mi | 22,5% |

### ⚠️ Verificar Red Flags

Valida cinco bandeiras vermelhas comuns em ofertas enganosas:

1. **Todos pagam meia parcela** — arrecadação reduzida à metade
2. **Milhares de cotas + 1 sorteio/mês** — % sorteado próximo de zero
3. **Taxa sobre crédito cheio com meia parcela** — custo relativo dobrado
4. **Promessa de contemplação em 3–6 meses via sorteio** — matematicamente impossível
5. **"Dobre seu crédito" com lance embutido de 50%** — paga taxa sobre R$ 1M para alavancar R$ 500k

**Veredicto:** 0 flags = Verde · 1 flag = Amarelo · 2+ flags = Vermelho

### 📊 Comparar Investimentos

Coloca lado a lado consórcio, renda fixa (CDI) e financiamento (Price) para o mesmo objetivo, mostrando custo total, parcela estimada e montante acumulado em renda fixa.

---

## Pré-requisitos

- **Python 3.11+**
- **Chaves de API:**
  - `GROQ_API_KEY` — [Groq API](https://console.groq.com)
  - `OPEN_ROUTER` — [OpenRouter](https://openrouter.ai)

### Modelos Disponíveis

| Modelo | Provedor | Tipo |
|---|---|---|
| Llama 3.3 70B | Groq | Rápido, preciso |
| Llama 3.1 8B | Groq | Leve, rápido |
| Gemma 3 27B | OpenRouter | Gratuito |
| Gemini 2.0 Flash | Google | Multimodal (recomendado) |
| Claude Sonnet 4.6 | Anthropic | Especializado |
| GPT-4o | OpenAI | SOTA |

---

## Instalação

### 1. Clone ou baixe o repositório

```bash
git clone <repo-url>
cd 00-ClaudeConsorcios
```

### 2. Crie um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale dependências

```bash
pip install -r requirements.txt
```

As dependências principais são:

```
streamlit>=1.32.0
python-dotenv>=1.0.0
openai>=1.50.0
```

### 4. Configure variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
GROQ_API_KEY="gsk_your_groq_key_here"
OPEN_ROUTER="sk-or-v1-your_openrouter_key_here"
```

**Nota:** Em produção (Streamlit Cloud), configure as chaves no painel **Settings → Secrets**.

---

## Como Rodar

### Localmente

```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`.

### Streamlit Cloud

1. Faça push do repositório para GitHub
2. Acesse [Streamlit Cloud](https://streamlit.io/cloud)
3. Clique em "New app" e selecione seu repositório
4. Configure as **Secrets** com suas chaves de API:
   ```
   GROQ_API_KEY = "gsk_..."
   OPEN_ROUTER = "sk-or-v1-..."
   ```
5. Deploy automático

---

## Estrutura do Projeto

```
00-ClaudeConsorcios/
├── app.py                          # Aplicação Streamlit principal
├── config.py                       # Configurações (API keys, modelos)
├── requirements.txt                # Dependências Python
├── .env                            # Variáveis de ambiente (local)
├── .env.example                    # Template de .env
│
├── docs/                           # Documentação de referência
│   ├── Como investir no Método da Jornada.html
│   ├── analise_metodo_jornada.md
│   ├── Relatório de Pesquisa_ Investimento em Consórcios...md
│   ├── Guia de Mitigação de Riscos no Trade...md
│   └── Análise Comparativa_ Consórcio vs. Outros Investimentos.md
│
├── .claude/                        # Ecossistema Claude Code
│   ├── CLAUDE.md
│   ├── kb/consorcios/              # Knowledge Base validado
│   │   ├── index.md
│   │   ├── quick-reference.md
│   │   ├── concepts/               # 7 conceitos atômicos
│   │   │   ├── aritmetica-do-grupo.md
│   │   │   ├── agio.md
│   │   │   ├── carta-de-credito.md
│   │   │   ├── tipos-de-contemplacao.md
│   │   │   ├── mercado-secundario-de-cotas.md
│   │   │   ├── tributacao-ganho-de-capital.md
│   │   │   └── regime-juridico.md
│   │   ├── patterns/               # 6 procedimentos reutilizáveis
│   │   │   ├── screener-grupo-saudavel.md
│   │   │   ├── trade-cartas-contempladas.md
│   │   │   ├── armadilha-lance-embutido.md
│   │   │   ├── comparativo-de-investimentos.md
│   │   │   ├── mitigacao-risco-fraude.md
│   │   │   └── mitigacao-risco-credito.md
│   │   └── specs/                  # YAMLs de referência
│   │       ├── administradoras-referencia.yaml
│   │       └── sinais-alerta-grupo.yaml
│   └── sdd/                        # Spec-Driven Development (arquivos históricos)
│
└── README.md                       # Este arquivo
```

---

## Ferramentas de Cálculo

Cada ferramenta é acionada automaticamente pelo assistente quando você fornece os dados necessários:

| Ferramenta | Trigger | Entrada |
|---|---|---|
| `auditar_grupo` | "auditar", "grupo", "cotas" | `cotas`, `prazo_meses`, `sorteios_por_mes`, `red_flags?`, `desvio_historico%?` |
| `calcular_agio` | "agio", "lucro", "vendo" | `parcelas_pagas`, `preco_venda`, `taxa_cessao?`, `meses_ate_contemplacao?` |
| `calcular_gcap` | "imposto", "IR", "DARF" | `preco_venda`, `custo_aquisicao`, `outras_vendas?`, `mes_venda`, `ano_venda` |
| `verificar_red_flags` | "red flag", "problema", "oferta" | `cotas?`, `prazo?`, `sorteios?`, `meia_parcela`, `promessa_meses`, `lance_embutido%`, `taxa_credito_cheio?` |
| `comparar_investimentos` | "comparar", "renda fixa", "financiamento" | `valor_credito`, `prazo_meses`, `taxa_adm%?`, `cdi%?`, `taxa_fin%?` |

---

## Knowledge Base (KB)

O projeto mantém uma **Knowledge Base validada via MCP** em `.claude/kb/consorcios/`, construída em **02 de Maio de 2026**. 

### Estrutura

- **7 Conceitos Atômicos** (≤ 150 linhas cada) — definições fundamentais
- **6 Padrões Reutilizáveis** (≤ 200 linhas cada) — procedimentos operacionais
- **2 Especificações YAML** — dados de referência estruturados

### Conceitos Disponíveis

| Conceito | Arquivo | Descrição |
|---|---|---|
| Aritmética do Grupo | `aritmetica-do-grupo.md` | Fórmulas de entregas/mês e % sorteado |
| Ágio | `agio.md` | Cálculo bruto, líquido e rentabilidade |
| Carta de Crédito | `carta-de-credito.md` | O que é contemplação |
| Tipos de Contemplação | `tipos-de-contemplacao.md` | Sorteio, lance, variações |
| Mercado Secundário | `mercado-secundario-de-cotas.md` | Trade de cartas contempladas |
| Tributação (GCAP) | `tributacao-ganho-de-capital.md` | Ganho de capital, DARF |
| Regime Jurídico | `regime-juridico.md` | Lei 11.795, BCB, ABAC |

### Padrões Disponíveis

| Padrão | Arquivo | Descrição |
|---|---|---|
| Screener Grupo Saudável | `screener-grupo-saudavel.md` | Passo a passo auditoria |
| Trade de Cartas | `trade-cartas-contempladas.md` | Fluxo completo do trade |
| Armadilha Lance Embutido | `armadilha-lance-embutido.md` | Por que é problema |
| Comparativo Investimentos | `comparativo-de-investimentos.md` | Consórcio vs alternativas |
| Mitigação Risco Fraude | `mitigacao-risco-fraude.md` | Proteção contra golpes |
| Mitigação Risco Crédito | `mitigacao-risco-credito.md` | Cota deficitária, cobertura |

---

## Configuração de API Keys

### Opção 1: Arquivo `.env` (Local)

Crie `.env` na raiz:

```bash
GROQ_API_KEY="gsk_..."
OPEN_ROUTER="sk-or-v1-..."
```

Execute:
```bash
streamlit run app.py
```

### Opção 2: Streamlit Cloud

1. No painel de controle do Streamlit Cloud, acesse **Settings → Secrets**
2. Cole suas chaves:
   ```
   GROQ_API_KEY = "gsk_..."
   OPEN_ROUTER = "sk-or-v1-..."
   ```
3. Deploy automático reconhecerá as chaves

A aplicação tenta `st.secrets` primeiro, depois `os.environ`. Se nenhuma for encontrada, exibe erro instruindo a configuração.

---

## Deployment

### Streamlit Cloud (Recomendado)

```bash
# 1. Push para GitHub
git add .
git commit -m "Deploy ClaudeConsórcios"
git push origin main

# 2. Acesse https://streamlit.io/cloud
# 3. Clique "New app" → selecione seu repositório
# 4. Configure Secrets (GROQ_API_KEY, OPEN_ROUTER)
# 5. Deploy automático
```

### Docker

```bash
# Crie Dockerfile (se necessário)
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]

# Build e execute
docker build -t claude-consorcios .
docker run -p 8501:8501 \
  -e GROQ_API_KEY="gsk_..." \
  -e OPEN_ROUTER="sk-or-v1-..." \
  claude-consorcios
```

### Google Cloud Run

```bash
gcloud run deploy claude-consorcios \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GROQ_API_KEY="gsk_...",OPEN_ROUTER="sk-or-v1-..."
```

---

## Temperatura do Modelo

A aplicação permite ajustar a **temperatura** via slider na sidebar:

| Temperatura | Perfil | Uso |
|---|---|---|
| 0.0 | 🎯 Preciso | Cálculos, recomendações |
| 0.5 | ⚖️ Equilibrado | Explicações e análises |
| 1.0 | 🎨 Criativo | Brainstorming, exploração |

**Padrão:** `0.0` (determinístico — ideal para cálculos).

---

## Exemplos de Uso

### Exemplo 1: Auditar Grupo

**Pergunta:**
> Um grupo tem 2.000 cotas, prazo de 180 meses e 1 sorteio por mês. Vale a pena entrar?

**Assistente calcula:**
- Entregas/mês: 11,11
- % sorteado: 0,1% (Vermelho)
- **Veredicto:** Descartar — grupo deficitário

### Exemplo 2: Calcular Ágio

**Pergunta:**
> Paguei R$ 50.000 em parcelas e vendo por R$ 80.000 com taxa de cessão de R$ 500. Qual o lucro?

**Assistente calcula:**
- Ágio bruto: R$ 30.000
- IR (15%): R$ 4.425
- **Ágio líquido: R$ 25.075**
- Rentabilidade: 50,1%

### Exemplo 3: Apurar GCAP

**Pergunta:**
> Vendi uma cota em maio/2026 por R$ 90.000. Paguei R$ 60.000 em parcelas e taxas. Qual o IR?

**Assistente calcula:**
- Ganho de capital: R$ 30.000
- IR devido (15%): R$ 4.500
- **Prazo DARF:** último dia útil de junho/2026

### Exemplo 4: Red Flags

**Pergunta:**
> O corretor prometeu contemplação em 6 meses e mencionou lance embutido de 50%. Tem problema?

**Assistente identifica:**
- Flag 4: Promessa em 6 meses (impossível)
- Flag 5: Lance embutido 50%
- **Veredicto:** Descartar — duas ou mais bandeiras

---

## Regras de Ouro

### Nunca

- 🚫 Pague ágio antes da anuência expressa da administradora registrada no sistema
- 🚫 Confie em promessas de contemplação em 3–6 meses via sorteio
- 🚫 Pague ágio em dinheiro vivo ou via marketplace sem custódia

### Sempre

- ✅ Exija histórico de contemplações por escrito antes de assinar
- ✅ Confirme autorização da administradora no portal do **Banco Central**
- ✅ Pague ágio via TED/PIX rastreável
- ✅ Guarde comprovantes de desembolso para reduzir base do GCAP
- ✅ Valide dados da cota no portal do consorciado ou SAC

---

## Legislação Aplicável

| Instrumento | Escopo |
|---|---|
| **Lei 11.795/2008** | Regula sistema de consórcios no Brasil |
| **Banco Central do Brasil** | Autoriza administradoras, supervisiona |
| **ABAC** | Associação Brasileira de Administradoras de Consórcios |
| **GCAP** | Programa Ganho de Capital (Receita Federal) |

---

## Contatos Úteis

| Órgão | Link |
|---|---|
| Banco Central | [www.bcb.gov.br](https://www.bcb.gov.br) |
| ABAC | [www.abac.org.br](https://www.abac.org.br) |
| Receita Federal (GCAP) | [www.gov.br/receitafederal](https://www.gov.br/receitafederal) |

---

## Contribuindo

Contribuições são bem-vindas! Para melhorias ou correções:

1. Identifique o problema ou proposta
2. Submeta um issue ou pull request
3. Siga as convenções do projeto (Python 3.11+, type hints, docstrings em português)

### Para Pesquisadores

Se está pesquisando o mercado de consórcios, veja os documentos em `docs/`:

- `Relatório de Pesquisa_ Investimento em Consórcios e Trade de Cartas Contempladas no Brasil.md` — panorama de mercado
- `Guia de Mitigação de Riscos no Trade de Cartas Contempladas.md` — riscos operacionais
- `Análise Comparativa_ Consórcio vs. Outros Investimentos.md` — comparações

---

## Licença

Este projeto é fornecido como ferramenta de educação e análise. Não constitui aconselhamento financeiro ou jurídico.

**Disclaimer:** Sempre consulte um especialista em consórcios e imposto de renda antes de tomar decisões financeiras importantes.

---

## Suporte

- **Documentação KB:** `.claude/kb/consorcios/index.md`
- **Documentação técnica:** `.claude/CLAUDE.md`
- **Issues:** Abra um issue no repositório
- **Email:** daniel.holiveira@gmail.com

---

## Histórico de Versões

| Data | Versão | Mudanças |
|---|---|---|
| 2026-05-03 | 1.0.0 | README inicial com todas as ferramentas e KB |
| 2026-01-31 | 0.9.0 | MVP em produção com 5 ferramentas e 3 abas |

---

**Última atualização:** 03 de Maio de 2026

Desenvolvido com IA generativa para especialistas em consórcios brasileiros.
