> **MCP Validated:** 2026-05-02

# Mitigação de Risco de Fraude

Checklist procedimental para reduzir exposição a anúncios falsos, falsa contemplação e cotas com gravame.

---

## Quando Usar

- Antes de pagar qualquer valor em cota contemplada anunciada por terceiros
- Quando o vendedor pressiona por pagamento rápido ou adiantado
- Quando o ágio anunciado é "imperdível" (muito abaixo do mercado)
- Quando a operação ocorre fora de marketplace conhecido

---

## Categorias de Fraude Cobertas

| Categoria | O que é |
|-----------|---------|
| Cota inexistente | Anúncio de cota que não pertence ao "vendedor" ou que não existe |
| Falsa contemplação | Documentos falsificados simulando contemplação |
| Pagamento antecipado | Vendedor desaparece após receber o ágio |
| Cota com gravame | Bloqueio judicial ou pendência financeira oculta |

Fonte: `docs/Guia de Mitigação de Riscos...md` §§1 e 4.

---

## Checklist de Validação

### 1. Documentação Mínima Antes de Negociar

- [ ] Extrato oficial e atualizado da cota
- [ ] Número do grupo e da cota
- [ ] Comprovante oficial da contemplação (extrato da assembleia)
- [ ] Documento de identificação do vendedor (CPF + RG)
- [ ] Comprovante de residência do vendedor

### 2. Confirmação Direta com a Administradora

- [ ] Ligar para o **SAC oficial** da administradora (pegando o número do site, não do anúncio)
- [ ] Confirmar:
  - existência da cota
  - titularidade
  - status de contemplação
  - permissão para transferência
  - ausência de impedimento judicial ou bloqueio
- [ ] Pedir orientação sobre o protocolo de cessão dessa administradora específica

### 3. Certidões Negativas

- [ ] Certidão negativa de débitos trabalhistas (CNDT)
- [ ] Certidões dos distribuidores cíveis e federais (varas onde o vendedor tenha domicílio)
- [ ] Verificação de protestos no estado de domicílio do vendedor

Foco: garantir que a cota não seja alvo de penhora por dívidas externas (`Guia...` §4).

### 4. Pagamento Condicionado

- [ ] **Nunca pagar antes** da formalização do termo de cessão
- [ ] Preferir pagamento via **TED/PIX rastreável**, nunca dinheiro vivo
- [ ] Em transações de alto valor, considerar custódia em cartório ou marketplace
- [ ] Cláusula contratual de devolução em caso de reprovação cadastral (ver [mitigacao-risco-credito](mitigacao-risco-credito.md))

### 5. Validação por Marketplace ou Assessoria Jurídica

- [ ] Quando possível, operar via marketplace conhecido (Grupo LuME, Tramontana, Toco) com triagem documental
- [ ] Em operação direta, contratar assessoria jurídica especializada para validar contrato e cessão

---

## Sinais de Alerta Vermelhos

| Sinal | Reação |
|-------|--------|
| Pedido de pagamento antes do termo de cessão | **Recusar e encerrar** a negociação |
| Ágio muito abaixo do mercado sem explicação | Suspeitar; não acelerar |
| Vendedor evita contato presencial ou videoconferência | Suspeitar |
| Vendedor recusa fornecer extrato oficial atualizado | Encerrar |
| Anúncio fora de canais conhecidos com pressão por urgência | Tratar como possível golpe |
| Documentos com inconsistências (nome, datas, número de grupo) | Encerrar |

---

## Protocolo de Resposta a Suspeita

Se detectar fraude ou suspeita durante a negociação:

1. **Interromper imediatamente** qualquer pagamento ou transferência.
2. **Documentar** todas as comunicações (e-mails, mensagens, comprovantes).
3. **Notificar a administradora** se a cota referenciada for de um grupo real.
4. **Registrar boletim de ocorrência** se houver tentativa de extorsão ou falsificação.
5. **Reportar** ao marketplace usado, se aplicável.

---

## "Caminho Seguro" Sintetizado

O `Guia de Mitigação de Riscos...md` resume em quatro etapas:

| Etapa | Ação |
|-------|------|
| Seleção | Administradora autorizada pelo BCB e associada à ABAC |
| Validação | Confirmar dados da cota no portal do consorciado ou via SAC |
| Formalização | Cessão de direitos com **anuência expressa** da administradora |
| Financeiro | Liquidar o ágio **somente após** a confirmação da transferência |

> Cada uma dessas etapas existe para neutralizar um vetor específico de fraude. Nenhuma é dispensável.

---

## Conexões

- [mercado-secundario-de-cotas](../concepts/mercado-secundario-de-cotas.md) — operação onde o risco se materializa
- [regime-juridico](../concepts/regime-juridico.md) — base legal da anuência
- [mitigacao-risco-credito](mitigacao-risco-credito.md) — risco complementar
- [trade-cartas-contempladas](trade-cartas-contempladas.md) — passo a passo onde este checklist se encaixa

---

## Fonte

`docs/Guia de Mitigação de Riscos...md` §§1, 2 e 4 (riscos de fraude, validação cadastral e jurídica); `docs/Relatório de Pesquisa...md` §5.1 (riscos e fraudes, anuência da administradora).
