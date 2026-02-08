import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from tqdm import tqdm

# Load model and tokenizer
model_name = "roberta-large-mnli"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()

# Load your JSON file
with open("questions_and_subqueries.json", "r") as f:
    data = json.load(f)

# Label mapping
labels = ['entailment', 'neutral', 'contradiction']

non_entailing_subquery_count = 0
total_subqueries = 0

results = []

for entry in tqdm(data, desc="Processing questions"):
    question = entry["question"]
    subqueries = entry.get("subqueries", [])
    entry_result = {
        "question": question,
        "subqueries": []
    }

    for subq in subqueries:
        total_subqueries += 1
        # Encode pair: premise=question, hypothesis=subquery
        inputs = tokenizer.encode_plus(question, subq, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = F.softmax(logits, dim=1)
        pred_label = labels[torch.argmax(probs)]
        entailment_prob = probs[0][labels.index("entailment")].item()

        if pred_label != "entailment":
            non_entailing_subquery_count += 1

        entry_result["subqueries"].append({
            "subquery": subq,
            "label": pred_label,
            "entailment_prob": round(entailment_prob, 4)
        })

    results.append(entry_result)

print(f"\nTotal subqueries: {total_subqueries}")
print(f"Non-entailing subqueries: {non_entailing_subquery_count}")

