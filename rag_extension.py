
# ============================================================
# RAG Extension - Neuro-Symbolic Math Data Generation
# My methodology contribution on top of NeurIPS 2024 paper
# ============================================================

# Install dependencies
# pip install faiss-cpu sentence-transformers openai z3-solver datasets

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import json
import time

# Initialize
embedder = SentenceTransformer("all-MiniLM-L6-v2")

class MathRAGIndex:
    """
    RAG Index for math problems using FAISS.
    Indexes verified problems and retrieves similar ones
    to guide future generation - no GPU required.
    """
    def __init__(self, embedding_dim=384):
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.problems = []
        self.embedder = embedder

    def add_problem(self, question, answer, problem_type):
        embedding = self.embedder.encode([question])[0]
        embedding = np.array([embedding], dtype=np.float32)
        self.index.add(embedding)
        self.problems.append({
            "question": question,
            "answer": answer,
            "type": problem_type
        })

    def retrieve(self, query, top_k=3):
        query_embedding = self.embedder.encode([query])[0]
        query_embedding = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.problems):
                results.append({
                    "problem": self.problems[idx],
                    "similarity_score": float(1 / (1 + dist))
                })
        return results

    def size(self):
        return self.index.ntotal


def retrieval_guided_informalize(client, symbolic_problem, 
                                  original_problem, rag_index):
    """
    My methodology contribution:
    Retrieve similar verified problems and use them as
    few-shot context to guide GPT-4o generation.
    Replaces fine-tuning with retrieval-based improvement.
    """
    # Step 1: Retrieve similar verified problems
    retrieved = rag_index.retrieve(original_problem, top_k=3)

    # Step 2: Build few-shot context
    few_shot_context = ""
    for i, result in enumerate(retrieved):
        few_shot_context += f"""
Example {i+1} (verified, answer={result["problem"]["answer"]}):
{result["problem"]["question"]}
"""

    # Step 3: Retrieval-guided generation
    prompt = f"""You are a math teacher creating word problems.

Here are {len(retrieved)} verified math word problems as examples:
{few_shot_context}

Now create a NEW math word problem based on these constraints:
{symbolic_problem}

Rules:
- Follow the style of the examples above
- Realistic word problem with real world context
- End with a clear question
- Do not reveal the answer
- Maximum 3-4 sentences

Output only the word problem, nothing else."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    generated = response.choices[0].message.content

    # Step 4: Add to index - self improving
    rag_index.add_problem(
        question=generated,
        answer="pending_verification",
        problem_type="rag_guided"
    )

    return generated, retrieved


# ============================================================
# Pipeline comparison
# Author:  SMT -> GPT -> Verified -> Fine-Tune LLM -> Loop
# Mine:    SMT -> GPT -> Verified -> RAG Index -> Retrieval-Guided GPT
# ============================================================
