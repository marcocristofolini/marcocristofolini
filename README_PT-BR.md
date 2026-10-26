# Marco Cristofolini

**Principal Site Reliability Engineer | Engenharia de Cloud e Plataformas**

Trabalho com sistemas e práticas de engenharia que tornam a produção mais fácil de operar: **serviços confiáveis, plataformas compartilhadas, entregas seguras e recuperação mais rápida de incidentes**.

[LinkedIn](https://www.linkedin.com/in/marcocristofolini/) · [Portfólio](https://marcocristofolini.dev) · [Projeto em destaque: AI SRE RCA](https://github.com/marcocristofolini/ai-sre-rca) · [English](README.md)

Sou **Principal SRE e ex-SRE Tech Lead**, com **mais de 13 anos** em infraestrutura, sistemas distribuídos e engenharia de plataformas. Trabalho diretamente com AWS, Azure e GCP e também com direção técnica, padrões de engenharia e equipes que operam serviços críticos. Minha experiência vai de hospedagem 24×7 a plataformas globais para desenvolvedores e infraestrutura de fintech regulada.

## Resultados e escala

| Escopo | Resultado documentado |
| --- | --- |
| **Adoção de plataforma — Ambev / AB InBev** | Plataforma interna baseada em Backstage adotada por **250+ squads**, com **800+ serviços** catalogados na América Latina e Europa |
| **Experiência do desenvolvedor — Ambev / AB InBev** | Onboarding de novos serviços reduzido de **~2 semanas para menos de 1 dia** com templates reutilizáveis e autosserviço |
| **Recuperação de incidentes — Caju** | MTTR reduzido de **~120 para ~40 minutos (−67%)**; disponibilidade dos serviços críticos de **99,5% para 99,9%** |
| **Entrega de software — Caju** | Lead time de mudanças reduzido de **~2 semanas para menos de 2 dias** com GitOps e entrega progressiva |
| **Eficiência em cloud — Caju** | Custos AWS reduzidos em **~28% (~R$ 45 mil/mês)** com rightsizing, autoscaling e limpeza de recursos |

*Os resultados acima vêm das experiências profissionais, não dos projetos pessoais publicados no GitHub.*

## Liderança técnica na prática

### Ambev / AB InBev · Principal Site Reliability Engineer / Platform Engineer (2020–2023)

- Liderei o desenvolvimento e a adoção de uma **plataforma interna para desenvolvedores com Backstage**, Golden Paths, catálogo de serviços, documentação e templates de autosserviço, com atuação em equipes da América Latina e Europa.
- Projetei e operei componentes de plataforma Kubernetes multicloud com **Azure AKS, AWS EKS e GCP GKE**. Padronizei infraestrutura como código e CI/CD com **Terraform / OpenTofu, Azure DevOps e GitOps**.
- Trabalhei com equipes de segurança, arquitetura corporativa e FinOps para transformar requisitos em padrões de plataforma e **mais de 20 RFCs/ADRs adotados**. Fiz mentoria de engenheiros e lideranças técnicas em diferentes regiões.

### Caju Benefícios · SRE Tech Lead / DevOps & Platform Engineer (2023–2026)

- Atuei com **12 squads, cerca de 60 microsserviços e cinco clusters EKS** em uma fintech regulada, combinando trabalho técnico em produção e liderança.
- Estruturei **SLIs/SLOs, error budgets, observabilidade, runbooks, postmortems e plantões**. O tempo de detecção de incidentes caiu de **~30 para ~2 minutos** e os incidentes recorrentes diminuíram **~40%**.
- Aumentei a segurança das entregas com **Argo CD, Flux, Argo Rollouts e Flagger**, além de ampliar o autosserviço com padrões de infraestrutura baseados em Terraform.
- Trabalhei com **requisitos PCI-DSS**, controles de identidade e acesso, secrets e segurança de infraestrutura na operação. Isso **não** significa que conduzi auditorias ou certificações PCI.

### Endurance International Group / HostGator · Senior DevOps & Infrastructure Engineer (2013–2020)

- Participei da modernização de sistemas de hospedagem de alto tráfego, com operação 24×7; liderei a migração de **~80% dos workloads de produção** de infraestrutura local para AWS.
- Automatizei o provisionamento e padronizei infraestrutura Linux, melhorando a consistência operacional de **mais de 1.000 servidores**.

## Projeto de engenharia em destaque: [AI SRE RCA](https://github.com/marcocristofolini/ai-sre-rca)

**Sistema de investigação de incidentes baseado em evidências verificáveis para Kubernetes e aplicações distribuídas.** Desenvolvi o projeto para explorar uma questão prática: como acelerar investigações com IA **sem permitir que um modelo invente causas raiz ou ultrapasse limites de segurança**?

| Decisão arquitetural | Implementação |
| --- | --- |
| **Manter o diagnóstico verificável** | RCA determinística vincula causas confirmadas a evidências de Kubernetes e telemetria com integridade verificada; evidências insuficientes resultam em diagnóstico inconclusivo |
| **IA como apoio, não autoridade** | Copilot opcional explica achados e cita evidências; sua resposta não pode alterar vereditos persistidos nem iniciar remediação |
| **Limitar a investigação** | Escopos autorizados de tenant/cluster/workload e tempo, coleta somente leitura, limites de consulta, jobs persistidos e progresso SSE com replay |
| **Separar análise de ação** | A remediação fica atrás de permissões próprias, políticas e aprovação humana explícita |
| **Testar modos de falha** | Benchmarks sintéticos e cenários controlados em Kind, incluindo múltiplas causas independentes e respostas inconclusivas corretas |

<a href="https://github.com/marcocristofolini/ai-sre-rca/blob/main/docs/images/app-multicausal-kind-running.png"><img src="https://raw.githubusercontent.com/marcocristofolini/ai-sre-rca/main/docs/images/app-multicausal-kind-running.png" width="700" alt="Interface AI SRE RCA mostrando causas independentes e evidências vinculadas em incidente controlado no Kind" /></a>

*Imagem: investigação local controlada em Kind, exibida como resultado somente leitura; não é um incidente de produção. O projeto é um release candidate em desenvolvimento, sem alegação de implantação em produção.*

[Arquitetura e segurança](https://github.com/marcocristofolini/ai-sre-rca#architecture-and-safety) · [Capturas da aplicação](https://github.com/marcocristofolini/ai-sre-rca#application-screenshots--running-local-demo) · [Relatórios de validação](https://github.com/marcocristofolini/ai-sre-rca#local-validation-recorded-results)

## Outros projetos públicos

- **[Production Readiness Framework](https://github.com/marcocristofolini/production-readiness-framework):** revisão de serviços com SLOs, sobrecarga, modos de falha e recuperação.
- **[Platform Engineering Reference](https://github.com/marcocristofolini/platform-engineering-reference):** padrões Backstage, Kubernetes e Argo CD para autosserviço.
- **[Kubernetes Incident Evidence Collector](https://github.com/marcocristofolini/kubernetes-incident-evidence-collector):** coletor Python somente leitura; protótipo testado com mocks, validação em cluster real pendente.
- **[Observability Stack](https://github.com/marcocristofolini/observability-stack):** ambiente local com OpenTelemetry, Prometheus, Loki, Tempo e Grafana.
- **[Terraform Cloud Platform](https://github.com/marcocristofolini/terraform-cloud-platform):** exemplos modulares de infraestrutura Terraform/OpenTofu.

*São implementações de referência, protótipos e laboratórios; cada repositório documenta suas limitações.*

## Como abordo o desenho de sistemas

- **Confiabilidade é prática operacional:** definir SLIs/SLOs, observar mudanças e preparar a recuperação antes dos incidentes.
- **Plataformas precisam ser adotadas:** tornar o caminho padrão mais seguro, documentado e simples do que construir infraestrutura isolada.
- **Segurança começa no desenho:** isolamento, privilégio mínimo, alterações revisáveis e limites explícitos de operação.
- **Evidência antes de convicção:** separar fatos de hipóteses; um diagnóstico inconclusivo é melhor do que uma causa inventada.

**Tecnologias principais:** AWS · Azure / AKS · GCP · Kubernetes · Terraform / OpenTofu / Bicep · Backstage · Azure DevOps · Argo CD · Python / Go · OpenTelemetry · Prometheus / Grafana · Datadog · operação sob requisitos PCI-DSS.

**Certificações obtidas:** CKA (2023) · AWS Solutions Architect – Associate (2023) · Istio Certified Associate (2022) · Terraform Associate (2022). *Não afirmo validade ou renovação atual.*

**Idiomas:** Português (nativo) · Inglês (avançado profissional) · Espanhol (proficiência profissional limitada).

**Contato:** [LinkedIn](https://www.linkedin.com/in/marcocristofolini/) · [Portfólio](https://marcocristofolini.dev)
