# Marco Cristofolini

**Principal / Staff Site Reliability Engineer · Platform Engineer**  
*Engenharia de confiabilidade, plataformas cloud-native e experiência do desenvolvedor em escala.*

[Site](https://marcocristofolini.dev) · [LinkedIn](https://www.linkedin.com/in/marcocristofolini/) · [English version](README.md)

Projeto, escalo e opero **sistemas distribuídos confiáveis e plataformas internas para desenvolvedores**. São **mais de 13 anos** de experiência em SRE, DevOps e infraestrutura, atuando em ambientes críticos 24×7, Kubernetes multicloud, automação de infraestrutura, observabilidade e entrega segura de software.

Meu foco: **confiabilidade mensurável, plataformas self-service e investigação de incidentes baseada em evidências.**

## Experiência e resultados em destaque

- **Ambev / AB InBev — Principal SRE / Platform Engineer (2020–2023):** Liderança de iniciativas de uma **Internal Developer Platform baseada em Backstage**, com catálogo de **mais de 800 serviços** e alcance de **centenas de squads** na América Latina e Europa. Desenvolvimento de Golden Paths, templates e fluxos de autosserviço.
- **Caju Benefícios — SRE Tech Lead / DevOps & Platform Engineer (2023–2026):** Evolução das práticas de SLOs, readiness de produção, arquitetura AWS/EKS multirregião, GitOps, observabilidade, identidade e políticas de segurança no contexto de fintech regulada.
- **Endurance International Group / HostGator — Senior DevOps & Infrastructure Engineer (2013–2020):** Modernização de infraestrutura de hospedagem em alta escala, incluindo migração de on-premises para AWS. Automação que reduziu o provisionamento de ambientes **de horas para minutos** e fortalecimento de operações 24×7.

Esses resultados são da experiência profissional e **não** significam que os repositórios pessoais abaixo tenham sido implantados nos ambientes de produção dessas empresas.

## Projetos de engenharia selecionados

Os repositórios abaixo são **implementações de referência, laboratórios ou protótipos públicos**. Cada projeto documenta seu próprio escopo e estágio de validação.

| Projeto | Foco e evidências |
| --- | --- |
| [Kubernetes Incident Evidence Collector](https://github.com/marcocristofolini/kubernetes-incident-evidence-collector) | CLI **Python** somente leitura para coleta de evidências de incidentes; protótipo revisado com testes mockados. **Validação em cluster real pendente.** |
| [Kubernetes RCA Engine](https://github.com/marcocristofolini/kubernetes-rca-engine) | Análise determinística de incidentes em **Go**, orientada a evidências, para OOMKilled, evictions e CrashLoopBackOff; implementação inicial **v0.1**. |
| [Production Readiness Framework](https://github.com/marcocristofolini/production-readiness-framework) | Revisões operacionais com **SLOs, modos de falha, proteção contra sobrecarga, recuperação e resposta a incidentes**. |
| [Platform Engineering Reference](https://github.com/marcocristofolini/platform-engineering-reference) | Exemplos arquiteturais com **Backstage, Kubernetes e Argo CD** para GitOps e autosserviço. |
| [Observability Stack](https://github.com/marcocristofolini/observability-stack) | Stack de referência local com **OpenTelemetry, Prometheus, Loki, Tempo e Grafana**. |
| [Terraform Cloud Platform](https://github.com/marcocristofolini/terraform-cloud-platform) | Padrões modulares com **Terraform / OpenTofu** e exemplo intencionalmente enxuto de rede AWS. |
| [Kubernetes SRE Playbook](https://github.com/marcocristofolini/kubernetes-sre-playbook) | Cenários reproduzíveis de falha, sinais de investigação e runbooks Kubernetes. |

## Competências principais

| Área | Tecnologias e práticas |
| --- | --- |
| **SRE e resiliência** | SLIs / SLOs, error budgets, resposta a incidentes, postmortems, production readiness, load shedding, graceful degradation, disaster recovery, capacity planning |
| **Platform Engineering** | Kubernetes, EKS / AKS / GKE, Backstage, Helm, Karpenter, KEDA, plataformas internas e Golden Paths |
| **Cloud e infraestrutura** | AWS, Google Cloud, Azure, Terraform, OpenTofu, Terragrunt, Pulumi (Go), Crossplane |
| **Entrega e GitOps** | Argo CD, Flux, Argo Rollouts, GitHub Actions, CI/CD, canary e blue-green |
| **Observabilidade** | OpenTelemetry, Prometheus, Grafana, Loki, Tempo, Datadog, New Relic, tracing e alertas acionáveis |
| **Segurança e identidade** | Keycloak, Vault, IAM, RBAC, OPA / Rego, Gatekeeper, Kyverno, guardrails DevSecOps |
| **Desenvolvimento e operações** | Go, Python, Bash, TypeScript, Linux, Kafka, Redis, PostgreSQL, otimização de custos e capacidade |

## Certificações

- **Certified Kubernetes Administrator (CKA)** — CNCF, 2023
- **AWS Certified Solutions Architect – Associate** — AWS, 2023
- **Istio Certified Associate (ICA)** — CNCF, 2022
- **HashiCorp Certified: Terraform Associate** — HashiCorp, 2022
- **Site Reliability Engineering Nanodegree** — Udacity, 2017

*As certificações estão listadas conforme o currículo; não estou afirmando o status atual de renovação ou validade.*

## Princípios de engenharia

```mermaid
flowchart LR
    P[Plataforma e entrega] --> R[Readiness de produção]
    R --> O[Observabilidade desde o início]
    O --> S[Operações orientadas por SLOs]
    S --> I[Investigação com evidências]
    I --> L[Aprendizado e automação]
    L --> P
```

Valorizo **evidências verificáveis em vez de conclusões opacas**, operações seguras por padrão, entregas incrementais e sistemas que os times consigam operar com autonomia.

**Idiomas:** Português (nativo) · Inglês (avançado profissional) · Espanhol (proficiência profissional limitada)

**Contato:** [LinkedIn](https://www.linkedin.com/in/marcocristofolini/) · [marcocristofolini.dev](https://marcocristofolini.dev)
