# Neuro-Symbolic Math Data Generation

Implementation of the neuro-symbolic data generation framework for mathematical reasoning, based on the NeurIPS 2024 paper "Neuro-Symbolic Data Generation for Math Reasoning" by Li et al.

## Problem Statement

Large Language Models struggle with mathematical reasoning. A key challenge in improving this is the lack of high quality math training data. Existing methods face a diversity-validity dilemma:
- Methods that produce diverse problems often introduce errors
- Methods that ensure valid problems sacrifice diversity

## Solution

This project solves the dilemma by mutating math problems in symbolic space using Z3 SMT solver, then converting back to natural language using GPT-4o. The solver guarantees every mutation is valid while MCMC sampling ensures diversity.

## Pipeline

    Natural Language Problem
            Down
       Formalization (Z3)
            Down
       Simplification Mutation
            Down
       Complication Mutation
            Down
       Informalization (GPT-4o)
            Down
       Generated Dataset

## Phases

### Phase 1 — Formalization
Converts natural language math problems into Z3 symbolic constraints.
Variables are typed (Int or Real), constraints are added to a solver,
and the problem is verified as solvable before mutation.

### Phase 2 — Simplification
Reduces problem complexity by removing one variable using Gaussian
elimination. The answer remains unchanged.

### Phase 3 — Complication
Increases difficulty by introducing new variables and constraints.
Projected MCMC sampling ensures diversity while the solver guarantees validity.

### Phase 4 — Informalization
GPT-4o converts the mutated symbolic problem back into a natural
language word problem with real world context.

## Example

Original GSM8K Problem:
Natalia sold clips to 48 of her friends in April, and then she sold
half as many clips in May. How many clips did Natalia sell altogether?
Answer: 72

Simplified Version:
Natalia sold 48 hair clips in April and half as many in May.
How many did she sell in total?
Answer: 72

Complicated Version:
In April, Natalia organized a fundraiser selling clips to 48 friends.
In May she continued selling at half the April rate while tracking
additional bonus sales. How many clips did she sell across both months?
Answer: 72

## Results

- 10 GSM8K seed problems processed
- 30 total problem variations generated
- 3 difficulty levels per problem
- 100 percent answer preservation across all mutations
- Zero failures in batch processing

## Tech Stack

- Python 3.12
- Z3 Solver — symbolic reasoning and constraint solving
- OpenAI GPT-4o — natural language informalization
- GSM8K Dataset — seed math problems
- Google Colab — development environment

## Setup

Install dependencies:
    pip install z3-solver openai datasets

Add your OpenAI API key to Colab secrets as OPENAI_API_KEY.

## Usage

Open pipeline.ipynb in Google Colab and run all cells.
The pipeline will process GSM8K problems and save results to
gsm8k_generated_dataset.json.

## Dataset

gsm8k_generated_dataset.json contains 30 generated math problems
with original, simplified, and complicated versions, each with
verified correct answers.

## Reference

Li, Z., Zhou, Z., Yao, Y., Li, Y., Cao, C., Yang, F., Zhang, X., and Ma, X.
Neuro-Symbolic Data Generation for Math Reasoning. NeurIPS 2024.

## Author

Harsha — Masters in Computer Science
github.com/Harsha123v
