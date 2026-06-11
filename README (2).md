# Neuro-Symbolic Math Data Generation

Implementation of the neuro-symbolic data generation framework for mathematical
reasoning, based on the NeurIPS 2024 paper "Neuro-Symbolic Data Generation for
Math Reasoning" by Li et al. Extended with a novel RAG-based retrieval pipeline.

## Problem Statement

Large Language Models struggle with mathematical reasoning. A key challenge is
the lack of high quality math training data. Existing methods face a
diversity-validity dilemma:
- Methods that produce diverse problems often introduce errors
- Methods that ensure valid problems sacrifice diversity

## Two Pipelines

### Author's Pipeline
    SMT Solver → GPT Informalization → Symbolic Verification → Fine-Tune LLM → Loop

### My Extended Pipeline (RAG-based)
    SMT Solver → GPT Informalization → Symbolic Verification → RAG Index → Retrieval-Guided GPT

## Key Difference

| Aspect | Author | My Extension |
|---|---|---|
| Improvement method | Fine-tune LLM | RAG retrieval |
| GPU required | Yes (4x H800) | No |
| Scales by | Retraining | Adding to index |
| Gets better via | Model weights | Retrieved examples |

My approach improves generation quality through retrieval rather than model
training, making it accessible without GPU infrastructure.

## Pipeline Phases

### Phase 1 — Formalization
Converts natural language math problems into Z3 symbolic constraints.

### Phase 2 — Simplification
Reduces complexity by removing variables using Gaussian elimination.

### Phase 3 — Complication
Increases difficulty by adding new variables while preserving correct answer.

### Phase 4 — Informalization
GPT-4o converts symbolic problems back to natural language.

### Phase 5 — RAG Indexing (My Contribution)
Verified problems are embedded using SentenceTransformers and indexed in FAISS.

### Phase 6 — Retrieval
Similar verified problems are retrieved for any new generation query.

### Phase 7 — Retrieval-Guided Generation (My Contribution)
GPT-4o uses retrieved examples as few-shot context for higher quality output.
Every new problem is added back to the index, making it self-improving.

## Results

- 10 GSM8K seed problems processed
- 30 problems generated with standard pipeline
- 5 additional problems generated with RAG pipeline
- Index grew from 30 to 36 automatically
- Zero GPU required for full pipeline

## Example

Original GSM8K Problem:
Natalia sold clips to 48 friends in April, half as many in May. Total?
Answer: 72

RAG-Guided Version:
Emily runs a small accessories business. In April she sold clips to 48
customers. Due to seasonal demand, her May sales were exactly half of
April. What was her total sales count across both months?
Answer: 72

## Tech Stack

- Python 3.12
- Z3 Solver — symbolic reasoning
- OpenAI GPT-4o — informalization
- FAISS — vector similarity search
- SentenceTransformers — problem embeddings
- GSM8K Dataset — seed problems
- Google Colab — development

## Setup

    pip install z3-solver openai datasets faiss-cpu sentence-transformers

## Project Structure

    neuro-symbolic-math-datagen/
    ├── pipeline.ipynb
    ├── gsm8k_generated_dataset.json
    ├── rag_results.json
    ├── README.md
    └── tests/
        ├── test_pipeline.py
        └── test_mutations.py

## Reference

Li et al. Neuro-Symbolic Data Generation for Math Reasoning. NeurIPS 2024.

## Author

Harsha Siva Prasad Puvvada
MS Computer Science — Texas Tech University
github.com/Harsha123v
