# Marco Cristofolini

**Principal Site Reliability Engineer | Cloud & Platform Engineering**

I build the systems and engineering practices that make production easier to operate: **reliable services, shared cloud platforms, safe delivery and faster incident response**.

[LinkedIn](https://www.linkedin.com/in/marcocristofolini/) · [Portfolio](https://marcocristofolini.dev) · [Featured project: AI SRE RCA](https://github.com/marcocristofolini/ai-sre-rca) · [Português](README_PT-BR.md)

I'm a **Principal SRE and former SRE Tech Lead** with **13+ years** in infrastructure, distributed systems and platform engineering. I've worked hands-on across AWS, Azure and GCP, while setting technical direction and engineering standards for teams operating critical services. My background ranges from 24×7 hosting to global developer platforms and a regulated fintech.

## Outcomes, not just technologies

| Scope | Documented impact |
| --- | --- |
| **Platform adoption - Ambev / AB InBev** | Backstage-based internal platform used by **250+ squads**, with **800+ services** cataloged across Latin America and Europe |
| **Developer experience - Ambev / AB InBev** | New-service onboarding reduced from **~2 weeks to under 1 day** through reusable templates and self-service |
| **Incident recovery - Caju** | MTTR reduced from **~120 to ~40 minutes (-67%)**; critical-service availability improved from **99.5% to 99.9%** |
| **Delivery - Caju** | Change lead time reduced from **~2 weeks to under 2 days** through GitOps and progressive releases |
| **Cloud efficiency - Caju** | AWS costs reduced **~28% (~BRL 45k/month)** through rightsizing, autoscaling and resource cleanup |

*These results belong to the roles described below, not to my personal GitHub projects.*

## Engineering leadership in practice

### Ambev / AB InBev · Principal Site Reliability Engineer / Platform Engineer (2020-2023)

- Led the development and adoption of a **Backstage internal developer platform** with Golden Paths, service catalog, documentation and reusable self-service templates; worked across engineering organizations in Latin America and Europe.
- Designed and operated multi-cloud Kubernetes platform capabilities across **Azure AKS, AWS EKS and GCP GKE**. Standardized Infrastructure as Code and CI/CD with **Terraform / OpenTofu, Azure DevOps and GitOps**.
- Partnered with security, enterprise architecture and FinOps stakeholders to turn requirements into platform guardrails and **20+ adopted RFCs/ADRs**. Mentored engineers and technical leaders across regions.

### Caju Benefícios · SRE Tech Lead / DevOps & Platform Engineer (2023-2026)

- Worked across **12 squads, ~60 microservices and five EKS clusters** in a regulated fintech, combining hands-on reliability work with technical leadership.
- Established **SLIs/SLOs, error budgets, actionable observability, runbooks, postmortems and on-call practices**. Improved incident detection from **~30 to ~2 minutes** and reduced recurring incidents by **~40%**.
- Improved release safety with **Argo CD, Flux, Argo Rollouts and Flagger**; expanded developer self-service with Terraform-based infrastructure patterns.
- Worked with **PCI-DSS requirements**, identity/access controls, secrets and security guardrails in production operations. This does **not** imply ownership of a PCI audit or certification.

### Endurance International Group / HostGator · Senior DevOps & Infrastructure Engineer (2013-2020)

- Helped modernize high-traffic, 24×7 hosting systems; led migration of **~80% of production workloads** from on-premises infrastructure to AWS.
- Automated provisioning and standardized Linux infrastructure, improving the operational consistency of a fleet of **1,000+ servers**.

## Featured engineering work: [AI SRE RCA](https://github.com/marcocristofolini/ai-sre-rca)

**A controlled, evidence-first incident investigation system for Kubernetes and distributed applications.** I built it to explore a practical engineering question: how do we use AI to accelerate investigation **without letting an LLM invent the root cause or cross security boundaries**?

| Design decision | Implementation |
| --- | --- |
| **Keep diagnosis verifiable** | Deterministic RCA links confirmed causes to integrity-checked Kubernetes/telemetry evidence; missing evidence yields an inconclusive outcome |
| **Use AI as an assistant, not an authority** | Optional Copilot explains verified findings and cites evidence; model output cannot change persisted verdicts or trigger remediation |
| **Constrain the investigation** | Authorized tenant/cluster/workload and time scope, read-only collection, query budgets, persisted jobs, replayable SSE progress |
| **Separate action from analysis** | Remediation lives behind its own permissions, policy checks and explicit human approval |
| **Test failure modes** | Documented synthetic benchmarks and controlled Kind scenarios, including multiple independent causes and correct abstentions |

<a href="https://github.com/marcocristofolini/ai-sre-rca/blob/main/docs/images/app-multicausal-kind-running.png"><img src="https://raw.githubusercontent.com/marcocristofolini/ai-sre-rca/main/docs/images/app-multicausal-kind-running.png" width="700" alt="AI SRE RCA interface showing independent causes and linked evidence in a controlled Kind incident" /></a>

*Screenshot: controlled local Kind investigation displayed as a read-only result; not a production incident. The project is a development release candidate, not a production deployment.*

[Architecture and security boundaries](https://github.com/marcocristofolini/ai-sre-rca#architecture-and-safety) · [Running UI screenshots](https://github.com/marcocristofolini/ai-sre-rca#application-screenshots--running-local-demo) · [Reproducible validation reports](https://github.com/marcocristofolini/ai-sre-rca#local-validation-recorded-results)

## Other public engineering projects

- **[Production Readiness Framework](https://github.com/marcocristofolini/production-readiness-framework):** service reviews for SLOs, overload behavior, failure modes and recovery.
- **[Platform Engineering Reference](https://github.com/marcocristofolini/platform-engineering-reference):** Backstage, Kubernetes and Argo CD patterns for developer self-service.
- **[Kubernetes Incident Evidence Collector](https://github.com/marcocristofolini/kubernetes-incident-evidence-collector):** read-only Python collector; mock-tested prototype, live-cluster validation pending.
- **[Observability Stack](https://github.com/marcocristofolini/observability-stack):** local OpenTelemetry, Prometheus, Loki, Tempo and Grafana environment.
- **[Terraform Cloud Platform](https://github.com/marcocristofolini/terraform-cloud-platform):** modular Terraform/OpenTofu infrastructure examples.

*These repositories are reference implementations, prototypes and labs; each has its own documented limitations.*

## How I approach system design

- **Reliability is operational:** define what matters through SLIs/SLOs, make changes observable, and rehearse recovery before incidents.
- **A platform succeeds when teams adopt it:** keep the default path safe, documented and easier than bespoke infrastructure.
- **Security is part of the design:** enforce isolation, least privilege, reviewable changes and explicit operational boundaries.
- **Evidence beats confidence:** distinguish observed facts from hypotheses; an inconclusive diagnosis is better than an invented one.

**Core stack:** AWS · Azure / AKS · GCP · Kubernetes · Terraform / OpenTofu / Bicep · Backstage · Azure DevOps · Argo CD · Python / Go · OpenTelemetry · Prometheus / Grafana · Datadog · PCI-DSS-aware operations.

**Credentials earned:** CKA (2023) · AWS Solutions Architect - Associate (2023) · Istio Certified Associate (2022) · Terraform Associate (2022). *Current renewal/expiration status is not asserted.*

**Languages:** Portuguese (native) · English (advanced professional) · Spanish (limited working proficiency).

**Contact:** [LinkedIn](https://www.linkedin.com/in/marcocristofolini/) · [Portfolio](https://marcocristofolini.dev)
