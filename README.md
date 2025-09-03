# Guardrails Project

A practical framework to ensure safe, grounded, and policy-compliant interactions with large language models (LLMs).
This project implements input and output guardrails, a trust scoring system, and a decision policy engine to minimize risks such as hallucinations, jailbreaks, PII leakage, and policy violations.

## 🎯 Overview

The Guardrails Project provides a multi-layer defense pipeline:

- **Input Guardrails** – Detect jailbreaks, filter unsafe or PII-laden prompts
- **Retriever (optional)** – Retrieve supporting evidence from a knowledge base
- **Output Guardrails** – Check grounding, detect contradictions, assess relevance
- **Trust Score** – Aggregate signals (relevance, coverage, consistency) into a confidence score
- **Decision Policy** – Choose between accept, ask for clarification, citations-only, or block
- **Evaluation Harness** – Benchmark performance on general and domain-specific datasets

## 🏗️ Architecture

```
User Query → Input Guardrails → Retriever/Verifier → LLM → Output Guardrails → Trust Score → Decision Policy → Final Response
```

## 📁 Project Structure

```
guardrails-project/
├── README.md
├── requirements.txt
├── config/
│   ├── thresholds.yaml       # trust score thresholds, decision rules
│   ├── datasets.yaml         # dataset paths & metadata
│   └── policies.yaml         # PII & policy configs
├── data/
│   ├── generic/              # e.g., HotpotQA subset
│   ├── domain/               # enterprise handbook KB
│   ├── pii/                  # synthetic PII set
│   └── jailbreak/            # jailbreak & red-team prompts
├── src/
│   ├── input_guardrails/     # jailbreak + pii filters
│   ├── retriever/            # retrieval/fact checker
│   ├── output_guardrails/    # grounding, contradiction, judge
│   ├── trust_score/          # score aggregation
│   ├── decision_policy/      # policy engine
│   ├── evaluators/           # metrics: DeepEval, RAGAS
│   └── app/                  # API server / proxy
├── notebooks/                # Jupyter analysis
│   ├── exploration.ipynb
│   ├── evaluation.ipynb
│   └── ablation.ipynb
├── tests/
│   ├── unit/
│   ├── integration/
│   └── redteam/
└── results/
    ├── metrics/
    ├── dashboards/
    └── reports/
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip or conda
- OpenAI / HF model API key (optional for embeddings)

### Setup

```bash
git clone <repo-url>
cd guardrails-project
pip install -r requirements.txt
```

### Run Pipeline

```python
from src.app.guardrails_pipeline import GuardrailsPipeline

pipeline = GuardrailsPipeline(config_path="./config")

resp = pipeline.process_query("Who wrote Pride and Prejudice?")
print(resp.text, resp.trust_score, resp.decision)
```

## 🔧 Configuration

### Trust Score Thresholds (`config/thresholds.yaml`)

```yaml
trust_score:
  high_confidence: 0.75   # Accept
  medium_confidence: 0.55 # Clarify or citations-only
  low_confidence: 0.40    # Block or escalate
```

### Policy Rules (`config/policies.yaml`)

```yaml
pii_filters:
  email: true
  phone: true
  credit_card: true
jailbreak_patterns:
  - "ignore previous"
  - "reveal secret"
```

### Dataset Config (`config/datasets.yaml`)

```yaml
datasets:
  generic: "data/generic/hotpotqa_subset.json"
  domain: "data/domain/enterprise_handbook.json"
  pii: "data/pii/pii_test.csv"
  jailbreak: "data/jailbreak/jailbreak_prompts.json"
```

## 🧪 Evaluation

### Datasets

- **Generic** – HotpotQA subset (factual QA grounding)
- **Domain** – Enterprise handbook KB + 200 curated QAs
- **Stress Tests** – Synthetic PII set (Faker), jailbreak prompt suite

### Metrics

- **Safety** – jailbreak block rate, PII precision/recall
- **Quality** – grounding score, contradiction risk, citation coverage
- **Performance** – latency, cost overhead

Run evaluations:

```bash
jupyter notebook notebooks/evaluation.ipynb
```

## 🧩 Components

- **Input Guardrails**: `jailbreak_detector.py`, `pii_filter.py`
- **Retriever**: `vector_store.py` (ChromaDB or FAISS)
- **Output Guardrails**: `grounding_scorer.py`, `nli_checker.py`, `judge.py`
- **Trust Score**: `aggregator.py`, `thresholds.yaml`
- **Decision Policy**: `policy_engine.py` (accept / clarify / block)
- **Evaluators**: `ragas_eval.py`, `deepeval_runner.py`

## 📊 Deliverables

- Middleware proxy service with config-driven guardrails
- Evaluation harness with generic + domain datasets
- Metrics dashboard (grounding, hallucination reduction, block rates)
- Final report with ablations and thresholds

## ⚠️ Notes

- Guardrails reduce but do not eliminate hallucinations and risks
- Domain datasets must be carefully curated for best results
- Always complement with human oversight in high-stakes domains

---

**Built with safety and reliability in mind** 🛡️