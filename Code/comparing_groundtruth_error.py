import json

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def sort_highlighted_cells(entry):
    entry["highlighted_cell_ids"] = sorted(entry.get("highlighted_cell_ids", []))
    entry["highlighted_cells"] = sorted(entry.get("highlighted_cells", []))
    return entry

def compare_highlights(data):
    count = 0
    total = 0
    for entry in data:
        total+=1
        fid = entry.get("feta_id")
        sort_highlighted_cells(entry)

        ids = entry["highlighted_cell_ids"]
        cells = entry["highlighted_cells"]

        if ids != cells:
            count+=1
            print(f" Mismatch for feta_id: {fid}")
            print(f"  highlighted_cell_ids: {ids}")
            print(f"  highlighted_cells    : {cells}\n")
        else:
            print(f"Match for feta_id: {fid}")

    print("Error percent : ",(count/total)*100)

# Load your JSONL file
jsonl_path = "../Datasets/FetaQA/fetaQA_dev_processed.jsonl"  # Replace with actual path
data = load_jsonl(jsonl_path)

# Compare highlights
compare_highlights(data)
'''


import json

def load_jsonl_as_dict(path):
    data = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            feta_id = item["example_id"]
            # Ensure cells are sorted for clean comparison
            sorted_cells = sorted(tuple(pair) for pair in item.get("highlighted_cells", []))
            data[feta_id] = sorted_cells
    return data

def compare_highlighted_cells(gt_path, pred_path):
    gt_data = load_jsonl_as_dict(gt_path)
    pred_data = load_jsonl_as_dict(pred_path)

    count = 0
    total = 0
    for feta_id in gt_data:
        gt_cells = gt_data[feta_id]
        pred_cells = pred_data.get(feta_id)

        if pred_cells is None:
            print(f"⚠️  Missing feta_id in predictions: {feta_id}")
            continue

        if gt_cells == pred_cells:
            print(f"✅ Match for feta_id: {feta_id}")
        else:
            count+=1
            print(f"❌ Mismatch for feta_id: {feta_id}")
            print(f"   Ground Truth: {gt_cells}")
            print(f"   Prediction  : {pred_cells}\n")
        total+=1
    print(f"Error Rate : {(count/total)*100}")

# === USAGE ===
groundtruth_path = "../Datasets/Totto/totto_processed.jsonl"
predicted_path = "../Datasets/Totto/totto_dataset_w_questions.jsonl"

compare_highlighted_cells(groundtruth_path, predicted_path)
'''
#Totto Error Rate - 23.33%
#FetaQA Error Rate - 60.13

