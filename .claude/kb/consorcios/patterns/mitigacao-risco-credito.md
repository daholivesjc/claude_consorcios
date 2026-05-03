> **MCP Validated:** 2026-05-02

# Mitigação de Risco de Crédito

A transferência de uma cota contemplada **não é automática**. Depende da aprovação cadastral do comprador pela administradora. Este padrão protege vendedor e comprador contra reprovação tardia.

---

## Quando Usar

- Sempre que uma cota contemplada estiver para ser cedida a terceiro
- Antes da assinatura do contrato particular de compra e venda do ágio
- Em qualquer operação fora de marketplace que faça pré-análise

---

## Risco Coberto

> O comprador paga o ágio, mas a administradora **não aprova** o cadastro dele por restrições no CPF/CNPJ ou por renda incompatível com as parcelas remanescentes.

Resultado prático sem mitigação: o ágio já foi pago; a cessão não acontece; o vendedor continua titular; o comprador busca devolução — frequentemente via judicial.

Fonte: `docs/Guia de Mitigação de Riscos...md` §2.

---

## Procedimento Recomendado

### 1. Pré-análise Obrigatória

Antes de qualquer pagamento ou contrato definitivo:

- [ ] Comprador encaminha documentação completa para a administradora
- [ ] Administradora emite **parecer de pré-análise** (aprovado, aprovado com condições, reprovado)
- [ ] Apenas com pré-análise positiva, vendedor e comprador firmam o contrato particular

> Algumas administradoras realizam apenas a análise definitiva. Quando não houver pré-análise formal, exigir do comprador documentos equivalentes (comprovação de renda, certidões) e usar cláusula de reversão como rede de segurança.

### 2. Documentação que Compõe a Análise

| Documento | Função |
|-----------|--------|
| RG e CPF | Identificação |
| Comprovante de residência atualizado | Cadastro |
| Comprovantes de renda (3 últimos contracheques ou DECORE/IR) | Capacidade de pagamento |
| Declaração de Imposto de Renda completa | Patrimônio e renda total |
| Certidões negativas | Restrições ativas |
| CNPJ + balanço (PJ) | Capacidade da pessoa jurídica |

### 3. Cláusula de Reversão no Contrato Particular

**Cláusula essencial:** prever expressamente que, em caso de reprovação cadastral pela administradora, o vendedor devolve **integralmente** o valor pago a título de ágio, em prazo determinado (ex: 5 dias úteis), sem retenção de qualquer percentual.

Modelo conceitual:

```
Cláusula X — Reversão por reprovação cadastral

Em caso de reprovação da análise de crédito do COMPRADOR
pela ADMINISTRADORA, o presente contrato será automaticamente
resolvido, obrigando-se o VENDEDOR a restituir, em até 5 (cinco)
dias úteis, a integralidade dos valores recebidos a título de ágio,
sem retenção, multa ou compensação a qualquer título.
```

> Texto ilustrativo. A redação final deve ser revisada por advogado.

### 4. Sequenciamento de Pagamentos

Princípio: **anuência primeiro, dinheiro depois.**

```
pré-análise OK
   ↓
contrato particular assinado (com cláusula de reversão)
   ↓
análise definitiva da administradora
   ↓
termo oficial de cessão e anuência expressa
   ↓
PAGAMENTO DO ÁGIO
```

### 5. Custódia Intermediária (Opcional)

Em operações de alto valor:

- Marketplace ou cartório retém o ágio em conta vinculada
- Liberação para o vendedor **só após** anuência da administradora registrada

Reduz risco para ambos os lados.

---

## Sinalizações Internas

| Situação | Ação |
|----------|------|
| Comprador resiste à pré-análise | Tratar como sinal de risco |
| Comprador insiste em pagar antes da anuência | Recusar |
| Vendedor recusa cláusula de reversão | Encerrar negociação |
| Pré-análise aprovada com condições (ex.: garantidor) | Garantir que a condição esteja cumprida antes da cessão |

---

## Risco Combinado: Crédito + Fraude

A reprovação cadastral pode ser usada como pretexto por golpistas para reter o ágio. Por isso, este padrão se aplica **junto** com o de [mitigacao-risco-fraude](mitigacao-risco-fraude.md):

- A pré-análise valida o comprador.
- O checklist anti-fraude valida o vendedor e a cota.
- A cláusula de reversão protege contra a hipótese de fraude camuflada.

---

## Conexões

- [mitigacao-risco-fraude](mitigacao-risco-fraude.md) — risco complementar
- [trade-cartas-contempladas](trade-cartas-contempladas.md) — etapa 4 ("Análise de Crédito")
- [regime-juridico](../concepts/regime-juridico.md) — fundamentação da exigência de anuência
- [mercado-secundario-de-cotas](../concepts/mercado-secundario-de-cotas.md) — contexto da cessão

---

## Fonte

`docs/Guia de Mitigação de Riscos...md` §2 (risco de reprovação de crédito, pré-análise e cláusula de reversão); `docs/Relatório de Pesquisa...md` §§4.2 (passo a passo) e 5.1 (verificação de crédito como exigência da administradora).
