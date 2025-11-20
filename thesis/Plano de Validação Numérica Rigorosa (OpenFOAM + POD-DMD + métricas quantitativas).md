Plano de Validação Numérica Rigorosa (OpenFOAM + POD/DMD + métricas quantitativas)

1. Plano de Validação Numérica Rigorosa (OpenFOAM + POD/DMD + métricas quantitativas)
Título do Plano: Numerical Validation Roadmap for the Multifluxe Hypothesis in Wall-Bounded Turbulence
Período estimado: 6–10 meses (2026)

EtapaObjetivoCasoReτGradeFerramentasMétricas de validação1Reprodução canônica + baselineCanal plano periódico (Reτ = 180, 550, 1000)180–1000128³–1024³OpenFOAM pisoFoam + channelFoamCf, ⟨u′v′⟩, espectros 1D/3D, perfis log-law2Decomposição modal clássicaMesmo caso550, 1000–Snapshot POD, SPOD, DMD (Modred/pyDMD)Energia capturada vs. rank, λ-criterion em modos, coerência espacial3Tentativa de clustering em espaço de fasesVelocity snapshots → reduced-order (POD 99%) → KMeans/GMM/DBSCAN––scikit-learn + pyKmedoidsInércia vs. K, silhouette score, estabilidade com inicialização, dependência de Re4Proposta de critério físico alternativoDefinir subfluxo como estruturas quase-coerentes com vida > 10–20 T+ e advecção coletiva550, 1000–Lagrangian tracking (OpenFOAM + PyVista) + Q-criterion + persistenceNúmero médio de subfluxos, taxa de nascimento/morte, transferência de energia entre subfluxos5Teste da hipótese de supressãoImpor condição artificial: forçar v⊥ < 5% da velocidade local média em todos subfluxos → observar Cf e produção de TKE550–Custom boundary condition em OpenFOAMRedução percentual de Cf e ∫τ_wall, colapso da camada log6Escala industrialAla NACA0012, Re = 5×10⁶ (LES WMLES)–~80M célulasOpenFOAM simpleFoam + IDDESDrag reduction (>30%) com supressão ativa de subfluxos transversais
Cronograma sugerido
Mês 1–2 → Etapas 1–2 (baseline + POD/DMD)
Mês 3–4 → Etapa 3 (demonstração rigorosa da falha do clustering)
Mês 5–7 → Etapas 4–5 (proposta e teste do novo critério físico)
Mês 8–10 → Etapa 6 + redação do Paper #2 (resultados definitivos)
