Figura 1 – Por que o clustering (KMeans, GMM, etc.) falha como decomposição física na Teoria do Multifluxo

   Campo turbulento real (Re ≈ 10⁶)                   Tentativa de decomposição em N = 4 subfluxos

   ╔═══════════════════════════════════╗        ╔══════════════════════════════════════════╗
   ║   ●    ●   ●     ●   ●   ●   ●    ║        ║   Subfluxo 1 (dominante, razoável)       ║
   ║     ●    ●    ●     ●     ●       ║        ║                                          ║
   ║   ●   ●     ●   ●    ●   ●   ●    ║  ──►   ║   Subfluxo 2 (distorcido e sobreposto)   ║
   ║       ●   ●      ●    ●     ●     ║        ║                                          ║
   ║   ●  ●   ●   ●  ●  ●   ●   ●   ●  ║        ║   Subfluxo 3 (artificial – não existe)   ║
   ║                                   ║        ║                                          ║
   ╚═══════════════════════════════════╝        ║   Subfluxo 4 (ruído classificado errado) ║
                                                ╚══════════════════════════════════════════╝

   Conclusão visual: em presença de cascata contínua de escalas (Kolmogorov),
   qualquer algoritmo de clustering produz N artificial, centróides distorcidos e
   decomposição não-única → não serve como base física determinística da teoria.



Instabilidade da decomposição em subfluxos via clustering (ex: KMeans)

          Campo de velocidade real (DNS/LES turbulento)                 Resultado típico do KMeans (N = 3 fixo)

   ┌───────────────────────────────────────┐                 ┌───────────────────────────────────────┐
   │                                       │                 │     ●  Centróide 1 (distorcido)       │
   │   ●  ●   ●   ●  ● ●  ●   ●  ●   ●,    │                 │                                       │
   │     ●   ●        ●        ●    ●      │                 │         ●  Centróide 2 (errado)       │
   │   ●   ●   ●   ●   ●  ● ●   ●   ●      │   ──────►       │                                       │
   │        ●    ●        ●   ●     ●      │                 │   ●  Centróide 3 (fantasma)           │
   │   ● ●   ●     ●  ●   ●    ●  ●   ●    │                 │                                       │
   │                                       │                 │   Inércia total ≈ 24 000 – 48 000     │
   └───────────────────────────────────────┘                 └───────────────────────────────────────┘

      Cascata de Kolmogorov contínua                     Os centróides NÃO correspondem a
      → espectro inercial com dezenas de milhares         subfluxos físicos reais
      de escalas de comprimento simultâneas               → N não é finito nem único
                                                         → dependente de inicialização
                                                         → viola o requisito de determinismo da teoria




