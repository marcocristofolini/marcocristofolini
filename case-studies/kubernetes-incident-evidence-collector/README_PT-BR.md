# Case técnico: coleta de evidências de incidentes no Kubernetes com apoio de IA

**Área:** SRE, Kubernetes, resposta a incidentes e geração de código com IA  
**Período:** outubro de 2026  
**Maturidade:** protótipo revisado, com testes simulados. A validação em cluster real ainda está pendente.

[English](README.md) · [Código Python](collector.py) · [Testes](tests/test_collector.py) · [Relatório do experimento](docs/experiment.md)

## O problema

Na investigação de um incidente em Kubernetes, um SRE normalmente precisa executar vários comandos kubectl, correlacionar eventos Warning, verificar reinicializações de containers e conferir o rollout de Deployments. Essa coleta manual demora e pode variar entre profissionais ou ocorrências.

A ideia foi construir um coletor **somente leitura** que, com um comando, entregue um JSON padronizado para ajudar o engenheiro a investigar o incidente.

O coletor **não determina a causa raiz**, não prevê incidentes e não executa remediações. Ele organiza evidências para análises futuras.

## O experimento

Durante um desafio de sete etapas, defini o problema, comparei ferramentas de geração de código, escrevi um prompt com critérios de segurança, gerei uma primeira implementação e revisei suas limitações.

- **Ferramenta escolhida no desafio:** GitHub Copilot no VS Code.
- **Ferramenta que gerou o código inicial documentado:** ChatGPT. A execução do mesmo prompt no Copilot não foi comprovada.
- **Stack:** Python 3.11+, kubectl, JSON e pytest.
- **Revisão:** análise de estados de Pods, readiness, rollout, segurança dos dados e erros de coleta.

## Arquitetura

~~~mermaid
flowchart LR
  A[Incidente] --> B[CLI Python somente leitura]
  B --> E[Eventos]
  B --> P[Pods e containers]
  B --> D[Deployments]
  E --> J[Normalização]
  P --> J
  D --> J
  J --> R[Relatório JSON]
  R --> H[Investigação humana]
  R -. integração futura .-> X[Motor RCA]
~~~

## Melhorias após revisão

A primeira implementação já coletava dados e passava nos testes iniciais, mas havia limitações importantes. A versão revisada passou a identificar Pods em execução sem prontidão, rollouts incompletos, controladores atrasados e históricos de OOMKilled.

Também passou a ocultar mensagens livres de eventos por padrão, limitar os recursos consultados, sinalizar falhas parciais de coleta e gravar JSON de forma atômica com permissões restritas em sistemas POSIX.

## Resultados comprovados

| Verificação | Inicial | Após revisão |
| --- | --- | --- |
| Testes automatizados aprovados | 11 | 19 |
| Execução em cluster real | Não realizada | Não realizada |
| Redução do tempo de investigação | Não medida | Não medida |
| Melhoria de MTTR | Não medida | Não medida |

Todos os testes foram executados com mocks e dados sintéticos. O aumento do número de testes representa cobertura adicional de cenários, não uma melhoria quantificada da confiabilidade.

## Reproduzir

No diretório do case:

~~~bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m compileall -q collector.py tests
python -m json.tool sample-report.json
~~~

Para testar em um cluster controlado, com kubectl configurado e RBAC apropriado:

~~~bash
python collector.py --namespace default --since-minutes 60 --output incident-evidence.json
~~~

O relatório de exemplo é **sintético**. Antes de compartilhar relatórios reais, revise os metadados porque nomes de recursos e mensagens podem conter informações sensíveis.

## Próximo passo

Rodar em um namespace descartável com falhas simuladas de readiness e rollout. Comparar as evidências com uma investigação manual, medir tempo de coleta, falsos positivos, lacunas e compatibilidade de RBAC. Só então considerar a integração ao motor determinístico de RCA.

[Leia o case completo em inglês](README.md), com decisões técnicas, código, limitações e evidências da revisão.
