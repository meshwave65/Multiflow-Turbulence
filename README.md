# Turbulência como Multifluxo (Turbulence as Multiflow )

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg )](https://creativecommons.org/licenses/by-nc-sa/4.0/ )

Este repositório é o centro de desenvolvimento e colaboração para a tese **"Turbulência como Multifluxo: Uma Nova Perspectiva Conceitual Aprofundada"** de Diogenes Duarte Sobral.

O projeto explora uma redefinição fundamental da turbulência: em vez de um estado de "caos aleatório", ela é proposta como um **Multifluxo** — uma superposição de múltiplos subfluxos laminares locais que interagem de forma não-linear.

<!-- [Link para a Tese Completa](./thesis/pt-BR/Turbulencia_como_Multifluxo_v4.0.pdf) -->

---

## Resumo da Teoria

A mecânica dos fluidos clássica separa o fluxo laminar (ordenado) do turbulento (caótico). A perspectiva do Multifluxo unifica esses conceitos sob um princípio comum: a **ordem local**.

A aparente desordem macroscópica da turbulência emerge da interação não-linear entre múltiplos subfluxos, cada um obedecendo localmente às leis do escoamento viscoso ordenado. Formalizamos esta visão através de uma decomposição do campo de velocidade:

$$ \vec{v}(\vec{x}, t) = \sum_{i=1}^{N} \vec{v}_i(\vec{x}, t) $$

Onde cada $\vec{v}_i$ é um subfluxo laminar local. A turbulência, portanto, não é uma propriedade intrínseca, mas o resultado da interação entre esses subfluxos, descrita pelo termo de convecção na Equação de Navier-Stokes.

### Implicações Práticas

Esta abordagem oferece novas perspectivas para:
*   **Modelagem e Simulação (LES):** Modelar grandes vórtices como subfluxos laminares, permitindo uma formulação mais física e menos empírica.
*   **Controle Ativo de Arrasto:** O objetivo se torna alinhar os subfluxos ($\vec{n}_i \approx \vec{n}_j$) para reduzir a interação não-linear e, consequentemente, o arrasto.
*   **Ensino de Mecânica dos Fluidos:** Apresentar a turbulência como uma soma de "ordens locais", tornando o conceito mais intuitivo.

## Objetivos do Repositório

1.  **Validar a Teoria:** Desenvolver simulações e análises que corroborem (ou refutem) a hipótese do Multifluxo.
2.  **Desenvolver Ferramentas:** Criar códigos e modelos baseados nesta perspectiva.
3.  **Fomentar a Colaboração:** Construir uma comunidade de pesquisadores, estudantes e engenheiros interessados em explorar e aplicar esta teoria.

## Como Contribuir

Estamos abertos a contribuições. Por favor, leia nosso [guia de contribuição](./docs/contributing.md) para mais detalhes.

## Estrutura do Projeto

*   `/thesis`: Contém as versões publicadas da tese.
*   `/src`: Código fonte para simulações, modelos e scripts de análise.
*   `/data`: Dados de simulações (idealmente com Git LFS).
*   `/media`: Imagens, gráficos e vídeos.
*   `/docs`: Documentação do projeto.

## Licença

Este trabalho está licenciado sob a **Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional (CC BY-NC-SA 4.0)**.
