# Turbulence as Multiflow (Turbulência como Multifluxo)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg )](https://creativecommons.org/licenses/by-nc-sa/4.0/ )

**[English]** | [Português](#português)

This repository is the development and collaboration hub for the thesis **"Turbulence as Multiflux: A Unified Framework"** by Diogenes Duarte Sobral.

The project explores a fundamental redefinition of turbulence: instead of a state of "random chaos," it is proposed as a **Multiflow**—a superposition of multiple local laminar subflows that interact non-linearly.

---

## Abstract

Classical fluid dynamics separates laminar (ordered) flow from turbulent (chaotic) flow. The Multiflow perspective unifies these concepts under a common principle: **local order**.

The apparent macroscopic disorder of turbulence emerges from the non-linear interaction between multiple subflows, each locally obeying the laws of ordered viscous flow. We formalize this view through a velocity field decomposition:

$$ \vec{v}(\vec{x}, t) = \sum_{i=1}^{N} \vec{v}_i(\vec{x}, t) $$

Where each $\vec{v}_i$ is a local laminar subflow. Turbulence, therefore, is not an intrinsic property but the result of the interaction between these subflows, described by the convection term in the Navier-Stokes Equation.

### Practical Implications

This approach offers new perspectives for:
*   **Modeling and Simulation (LES):** Modeling large eddies as laminar subflows, allowing for a more physical and less empirical formulation.
*   **Active Drag Control:** The goal becomes aligning the subflows ($\vec{n}_i \approx \vec{n}_j$) to reduce non-linear interaction and, consequently, drag.
*   **Fluid Mechanics Education:** Presenting turbulence as a sum of "local orders," making the concept more intuitive.

## Repository Goals

1.  **Validate the Theory:** Develop simulations and analyses that corroborate (or refute) the Multiflow hypothesis.
2.  **Develop Tools:** Create codes and models based on this perspective.
3.  **Foster Collaboration:** Build a community of researchers, students, and engineers interested in exploring and applying this theory.

## How to Contribute

We are open to contributions. Please read our [contribution guide](./docs/contributing.md) for more details.

## Project Structure

*   `/thesis`: Contains the published versions of the thesis.
*   `/src`: Source code for simulations, models, and analysis scripts.
*   `/data`: Simulation data (ideally using Git LFS).
*   `/media`: Images, graphics, and videos.
*   `/docs`: Project documentation.

## License

This work is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

---
---

## Português

Este repositório é o centro de desenvolvimento e colaboração para a tese **"Turbulência como Multifluxo: Uma Nova Perspectiva Conceitual"** de Diogenes Duarte Sobral.

O projeto explora uma redefinição fundamental da turbulência: em vez de um estado de "caos aleatório", ela é proposta como um **Multifluxo** — uma superposição de múltiplos subfluxos laminares locais que interagem de forma não-linear.

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

