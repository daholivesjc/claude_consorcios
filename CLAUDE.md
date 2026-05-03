# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository nature

This is a **content/research repository in Portuguese (pt-BR)** about the Brazilian consortium market (*consórcios*) and the trade of contemplated letters (*trade de cartas contempladas*). There is **no code, no build system, no tests, and no package manager** — work here is reading, writing, and editing `.md` analysis documents.

There is no git repository initialized.

## Layout

```
.
├── CLAUDE.md
├── docs/                # source materials (read-only research)
└── .claude/             # Claude Code ecosystem (agents, kb, commands, sdd)
    └── kb/consorcios/   # KB derived from docs/
```

## Source materials (`docs/`)

Each file plays a distinct role — do not treat them as interchangeable:

- `docs/Como investir no Método da Jornada.html` — **primary source** (6.4 MB). Original commercial HTML from Megacombo (CNPJ 07.403.727/0001-69) being analyzed. Treat as read-only source material; cite from it but do not rewrite it.
- `docs/analise_metodo_jornada.md` — critical analysis of the HTML above (structure, formulas, weak points, sales-funnel framing). This is the document that engages most directly with the source.
- `docs/Relatório de Pesquisa_ Investimento em Consórcios e Trade de Cartas Contempladas no Brasil.md` — broad market report (panorama, administradoras, ágio mechanics, taxation, references). Authored "Manus AI". Numbered references `[1]`–`[15]` at the bottom.
- `docs/Guia de Mitigação de Riscos no Trade de Cartas Contempladas.md` — risk-mitigation guide (fraud, credit, liquidity, legal, tax). Authored "Manus AI".
- `docs/Análise Comparativa_ Consórcio vs. Outros Investimentos.md` — comparison vs. renda fixa, FIIs, financiamento. Authored "Manus AI".

The three "Manus AI" documents form a coherent trilogy: market overview → comparative framing → operational risks. The "Método da Jornada" pair (`.html` + `analise_metodo_jornada.md`) is a separate critique track focused on one specific commercial product.

## Knowledge base (`.claude/kb/consorcios/`)

A structured, MCP-validated KB distilled from `docs/` (built 2026-05-02). Use it as the **first lookup** for any consórcios question — `docs/` remains the source of truth, but the KB is the indexed, atomic version.

```
.claude/kb/consorcios/
├── index.md                   # navigation
├── quick-reference.md         # fast lookup tables
├── concepts/                  # 7 atomic definitions (≤ 150 lines each)
├── patterns/                  # 6 reusable procedures (≤ 200 lines each)
└── specs/                     # 2 machine-readable YAMLs
    ├── administradoras-referencia.yaml
    └── sinais-alerta-grupo.yaml
```

The KB is registered in `.claude/kb/_index.yaml` under `domains.consorcios`. Every file there carries a `> **MCP Validated:** YYYY-MM-DD` header — bump it when content is revised. KB files cite back into `docs/` via a trailing `## Fonte` section; preserve that link when editing.

## Conventions to preserve when editing

- **Language: Portuguese (pt-BR)** for all content. Do not translate to English unless explicitly asked.
- **Dates: full Portuguese form** in headers (e.g., `02 de Maio de 2026`) but ISO `YYYY-MM-DD` inside the analysis files (e.g., `2026-05-02`). Match the surrounding file's convention.
- **Authorship line** appears just under the H1 (`**Autor:** ...` / `**Data:** ...`). Preserve and update when editing substantively.
- **Tables** use Markdown pipe syntax with `:---` alignment markers; keep that style for new tables.
- **Numerical claims** in the "Manus AI" reports are footnoted `[N]` and resolved at the end. If you add or change a factual claim, add a corresponding reference rather than leaving it unsourced — that is the established voice of this repo.
- **Tone in the "Manus AI" reports** is neutral/explanatory. **Tone in `analise_metodo_jornada.md`** is critical/auditorial (calls out conflicts of interest, weak claims) — do not flatten one into the other.

## Domain vocabulary (don't gloss over)

Working here requires using these terms precisely; do not paraphrase:

- **Carta de crédito** — the credit letter awarded on contemplation.
- **Contemplação** — being awarded the letter, by *sorteio* (draw) or *lance* (bid).
- **Lance fixo / livre / embutido / fidelidade** — distinct bid types. Note: `analise_metodo_jornada.md` flags **lance embutido** as a *payment modality*, not a bid type — preserve that distinction when editing.
- **Ágio** — the premium paid for a contemplated letter on the secondary market (lucro = ágio − custos).
- **Trade de cartas contempladas** — the secondary-market activity itself.
- **Cota deficitária / "furada"** — a group whose actual contemplations trail the arithmetic expectation (`cotas ÷ prazo`).
- **GCAP** — Receita Federal's *Ganho de Capital* program; relevant for tax sections.
- **ABAC**, **Banco Central**, **Lei 11.795/2008** — regulatory anchors; cite them, don't generalize.

## Working on tasks here

- **Look in `.claude/kb/consorcios/` first** for an existing answer; fall back to `docs/` only when the KB is silent.
- For **factual edits** in `docs/` (numbers, dates, references): cross-check against the existing footnotes in the same file before changing — the documents quote each other implicitly. If you change a fact in `docs/`, also propagate it to the corresponding KB file and bump that file's `MCP Validated` date.
- For **new analysis**: follow the structure of the closest existing file (numbered H2 sections, summary table at the end, conclusion).
- For **work derived from the HTML**: the source is large (6.4 MB) and likely contains images that did not survive text extraction (`docs/analise_metodo_jornada.md` §7 notes this) — be explicit when a claim cannot be verified from the extracted text. Prefer routing through `analise_metodo_jornada.md`'s distillation rather than re-extracting from the HTML.
- The repo has no automation, so there is **nothing to "build" or "lint"**. Verification is editorial: re-read for internal consistency, check that footnote numbers resolve, confirm tables render, and check KB cross-links resolve (`grep -r "\[.*\](" .claude/kb/consorcios/`).
