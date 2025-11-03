#!/usr/bin/env python3
"""
Evaluate retrieval quality on the RAG sample dataset.

Computes Precision@K, Recall@K, and nDCG@K
for each query and averages the results.

Assumes the dataset columns:
  query_id, query_text, candidate_id, candidate_text,
  baseline_rank, baseline_score, gold_label
"""

import pandas as pd
import numpy as np
from smolagents import OpenAIServerModel
import dotenv
import os





# ---------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------
df = pd.read_csv("rag_sample_queries_candidates.csv")

#AIzaSyCx0qQuAKKNZsnqTEsHzSkvMDGpEgWuFOg
g_dotenv_loaded = False
def getenv(variable: str) -> str:
    global g_dotenv_loaded
    if not g_dotenv_loaded:
        g_dotenv_loaded = True
        dotenv.load_dotenv()
    value = os.getenv(variable)
    return value

api_key = getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY needs to be set in .env.")

model_id="gemini-2.5-flash"
model = OpenAIServerModel(model_id=model_id,
                          api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
                          api_key="AIzaSyCx0qQuAKKNZsnqTEsHzSkvMDGpEgWuFOg",
                          )

'''answer = model.generate(messages=[{
    "role": "user", 
    "content": "Which is warmer? Blue or red?"
}])'''

#print(f"Model returned answer: {answer.content}")


#responses = []
prompt = f"""
    You are evaluating search results.
    
    Rate how relavant each candidate is to it's corresponding query on a scale from 0-5.
    0 = not relevant at all, 5 = highly relevant
    Respond with ONLY a number {0, 1, 2, 3, 4, 5}. No words.
    """

for i in range(len(df)):
    prompt += f"""
    {i}:
    Query: {df['query_text'][i]}
    Candidate: {df['candidate_text'][i]}
    
    """



#for i in range(10):
    #print("Query Text: ", df['query_text'][i])
    #print("Candidate Text: ", df['candidate_text'][i])


resp = model.generate(messages=[{"role": "system", "content": "Respond only with a number 0-5"}, {"role": "user", "content": prompt}])
#responses.append(resp.content)
    #print(resp.choices[0].message.content)

#print(prompt)
#print(responses)
responses = resp.content.split("\n")

responses_clean = [item.strip() for item in responses if item.strip()]


resp_float = [float(item) for item in responses_clean]

if(len(resp_float) < len(df)):
    for i in range(len(resp_float), len(df)):
        resp_float.append(0.0)
elif(len(resp_float) > len(df)):
    for i in range(len(resp_float), len(df)):
        resp_float.pop()




df['llm_score'] = resp_float


# Ensure results are ordered by the baseline rank
df.sort_values(["query_id", "baseline_rank"], inplace=True)

# ---------------------------------------------------------------------
# 2. Metric helpers
# ---------------------------------------------------------------------
def precision_at_k(labels, k):
    """labels: list/array of 0/1 relevance sorted by baseline rank"""
    topk = labels[:k]
    return np.sum(topk) / len(topk)

def recall_at_k(labels, k):
    """Recall = retrieved relevant / total relevant"""
    total_relevant = np.sum(labels)
    if total_relevant == 0:
        return np.nan  # undefined
    topk = labels[:k]
    return np.sum(topk) / total_relevant

def ndcg_at_k(labels, k):
    """Compute nDCG@k with binary relevance (0/1)."""
    labels = np.array(labels)
    k = min(k, len(labels))
    gains = (2 ** labels[:k] - 1)
    discounts = 1 / np.log2(np.arange(2, k + 2))
    dcg = np.sum(gains * discounts)

    # Ideal DCG: sorted by true relevance
    ideal = np.sort(labels)[::-1]
    ideal_gains = (2 ** ideal[:k] - 1)
    idcg = np.sum(ideal_gains * discounts)
    return 0.0 if idcg == 0 else dcg / idcg

# ---------------------------------------------------------------------
# 3. Compute metrics per query
# ---------------------------------------------------------------------
results = []
K = 3

for qid, group in df.groupby("query_id"):
    labels = group["gold_label"].tolist()
    p = precision_at_k(labels, K)
    r = recall_at_k(labels, K)
    n = ndcg_at_k(labels, K)
    results.append({"query_id": qid, f"precision@{K}": p, f"recall@{K}": r, f"nDCG@{K}": n})

metrics = pd.DataFrame(results)

# ---------------------------------------------------------------------
# 4. Display per-query and average metrics
# ---------------------------------------------------------------------
print(metrics.round(3))
print("\nAverage metrics:")
print(metrics[[f"precision@{K}", f"recall@{K}", f"nDCG@{K}"]].mean().round(3))






#Re-ranking




df.sort_values(["query_id", "llm_score"], ascending=[True, False], inplace=True)
results = []
K = 3

for qid, group in df.groupby("query_id"):
    labels = group["gold_label"].tolist()
    p = precision_at_k(labels, K)
    r = recall_at_k(labels, K)
    n = ndcg_at_k(labels, K)
    results.append({"query_id": qid, f"precision@{K}": p, f"recall@{K}": r, f"nDCG@{K}": n})



metrics = pd.DataFrame(results)

# ---------------------------------------------------------------------
# 4. Display per-query and average metrics
# ---------------------------------------------------------------------
print(metrics.round(3))
print("\nAverage metrics:")
print(metrics[[f"precision@{K}", f"recall@{K}", f"nDCG@{K}"]].mean().round(3))


df_out = df[["query_id", "candidate_id", "llm_score"]].copy()


df_out.to_csv("results.csv", index=False)
