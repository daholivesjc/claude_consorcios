> **MCP Validated:** 2026-05-02

# Carta de Crédito

## Definição

A **carta de crédito** é o instrumento financeiro entregue ao cotista contemplado: um valor pré-aprovado, atualizado por índice contratual, destinado à aquisição do bem ou serviço previsto no grupo (imóvel, veículo, eletroeletrônico, serviço, etc.).

Ela é o **ativo subjacente** de qualquer operação de trade no mercado secundário.

---

## Premissa Central

> Não é dinheiro vivo na conta — é poder de compra carimbado para um fim específico.

A carta de crédito tem três traços que a distinguem de uma poupança ou de um empréstimo bancário:

1. **Vinculação contratual** — só pode ser usada na finalidade do grupo.
2. **Atualização por índice** — protege o poder de compra durante a espera.
3. **Saldo devedor remanescente** — quem usa a carta continua pagando parcelas até o fim do grupo.

---

## Atualização por Índice

A carta é reajustada periodicamente pelo índice contratual. Os mais comuns no mercado brasileiro são:

| Segmento | Índice típico | Por quê |
|----------|---------------|---------|
| Imóveis | INCC | Acompanha custo de construção |
| Imóveis usados / mistos | IPCA | Inflação geral |
| Veículos | IPCA ou tabela específica do segmento | Equilíbrio com preço de tabela |
| Eletroeletrônicos / serviços | IPCA | Inflação geral |

Esse reajuste é o que protege o **poder de compra** do cotista, conforme destacado na `Análise Comparativa` (§1) — algo que a renda fixa nem sempre acompanha perfeitamente.

---

## Uso do FGTS no Consórcio Imobiliário

No consórcio imobiliário, o FGTS pode ser utilizado em duas situações principais:

- **Para dar lance** — antecipa a contemplação.
- **Para amortizar parcelas** — reduz o saldo devedor após a contemplação.

É um diferencial relevante frente a FIIs, onde **não há uso possível de FGTS** (`Análise Comparativa` §2).

> Regras específicas e teto seguem a normativa da Caixa Econômica Federal e variam conforme localização e situação do imóvel; sempre confirmar com a administradora.

---

## Componentes Custaveis da Carta

Quem analisa a carta precisa olhar além do valor nominal:

| Componente | Onde aparece |
|------------|--------------|
| Valor nominal do crédito | Contrato de adesão |
| Taxa de administração | Diluída ao longo das parcelas |
| Fundo de reserva | Garantia coletiva contra inadimplência |
| Seguro | Em alguns grupos, opcional ou obrigatório |
| Reajuste anual pelo índice | Aplicado tanto sobre crédito quanto sobre saldo devedor |

A `analise_metodo_jornada` §7 nota que esses componentes não foram tratados pelo material original do "Método da Jornada" — qualquer leitura financeira séria precisa modeláveis explicitamente.

---

## Ciclo de Vida da Carta

```
ADESÃO          CONTEMPLAÇÃO          UTILIZAÇÃO          QUITAÇÃO
   │                  │                    │                  │
   ▼                  ▼                    ▼                  ▼
Cota nova ──▶ sorteio/lance ──▶ uso do crédito ──▶ saldo devedor zerado
                  │                    │
                  ▼                    ▼
             Pode ser cedida      Bem entra como
             (mercado secundário) garantia até quitar
```

Após a contemplação, a carta pode ser:

- **Utilizada** — para comprar o bem objeto do grupo.
- **Cedida** — vendida no mercado secundário com ágio (ver [mercado-secundario-de-cotas](mercado-secundario-de-cotas.md)).
- **Mantida em uso parcial** — em alguns segmentos, é possível usar parte do crédito e devolver o saldo remanescente.

---

## Conexões

- [agio](agio.md) — preço de venda da carta no secundário
- [mercado-secundario-de-cotas](mercado-secundario-de-cotas.md) — onde a carta é negociada
- [aritmetica-do-grupo](aritmetica-do-grupo.md) — quantas cartas o grupo entrega/mês

---

## Fonte

`docs/Relatório de Pesquisa...md` §§3 e 4 (atualização por índice e uso pós-contemplação); `docs/Análise Comparativa...md` §§1 e 2 (poder de compra, uso de FGTS); `docs/analise_metodo_jornada.md` §7 (componentes não tratados pelo material original).
