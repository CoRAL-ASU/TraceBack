import json
file = "totto_results/ablation/answer_attribution_gpt-4o_subquery_each.json"
with open(file, 'r', encoding='utf-8') as f:
	data = json.load(f)

def evaluate_prediction(pred_result, gt_result):
	
	pred_result = [list(t) for t in set(tuple(lst) for lst in pred_result)]
	

	pred_rows = set(r for r, c in pred_result)
	pred_cols = set(c for r, c in pred_result)
	gt_rows = set(r for r, c in gt_result )
	gt_cols = set(c for r, c in gt_result)

	#print(pred_rows,gt_rows,feta_id)
	row_tp = len(pred_rows & gt_rows)
	col_tp = len(pred_cols & gt_cols)

	gt_cells = set((r, c) for r, c in gt_result)

	pred_cells = set((r, c) for r, c in pred_result)
	gt_cells = set((r, c) for r, c in gt_result)

	cell_tp = len(pred_cells & gt_cells)  
	cell_pred_total = len(pred_cells)
	cell_gt_total = len(gt_cells)

	return {
		"row_tp": row_tp,
		"row_pred_total": len(pred_rows),
		"row_gt_total": len(gt_rows),
		"col_tp": col_tp,
		"col_pred_total": len(pred_cols),
		"col_gt_total": len(gt_cols),
		"cell_level_tp": cell_tp,
		"cell_pred_total":cell_pred_total,
		"cell_gt_total":cell_gt_total

	}


total_row_tp = total_row_pred = total_row_gt = 0
total_col_tp = total_col_pred = total_col_gt = 0
total_cell_tp = total_cell_pred = total_cell_gt = 0

exact_match_count = 0
total_examples = 201

for item in data:
	pred_data = item["result"]
	gt_data = item["highlighted_cell_ids"]

	if gt_data is None:
		total_examples-=1
		continue
	for i in range(len(pred_data)):
		pred_data[i][0]+=1

	result = evaluate_prediction(pred_data,gt_data)

	total_row_tp += result["row_tp"]
	total_row_pred += result["row_pred_total"]
	total_row_gt += result["row_gt_total"]
	total_col_tp += result["col_tp"]
	total_col_pred += result["col_pred_total"]
	total_col_gt += result["col_gt_total"]
	total_cell_tp += result["cell_level_tp"]
	total_cell_pred += result["cell_pred_total"]
	total_cell_gt += result["cell_gt_total"]

print(total_examples)
metrics = {
	"row_precision": total_row_tp / total_row_pred if total_row_pred else 0.0,
	"row_recall": total_row_tp / total_row_gt if total_row_gt else 0.0,
	"column_precision": total_col_tp / total_col_pred if total_col_pred else 0.0,
	"column_recall": total_col_tp / total_col_gt if total_col_gt else 0.0,
	"cell_precision": total_cell_tp / total_cell_pred if total_cell_pred else 0.0,
	"cell_recall": total_cell_tp / total_cell_gt if total_cell_gt else 0.0,
	# "exact_match": exact_match_count / total_examples if total_examples else 0.0
}

print(metrics)

#aitqa : {'row_precision': 0.8495575221238938, 'row_recall': 0.9552238805970149, 'column_precision': 0.336322869955157, 'column_recall': 0.3712871287128713, 'cell_precision': 0.292, 'cell_recall': 0.3613861386138614}
#fetaqa : {'row_precision': 0.7404371584699454, 'row_recall': 0.9344827586206896, 'column_precision': 0.8398058252427184, 'column_recall': 0.6975806451612904, 'cell_precision': 0.6602641056422569, 'cell_recall': 0.6193693693693694}
#totto : {'row_precision': 0.5698924731182796, 'row_recall': 0.7429906542056075, 'column_precision': 0.7099447513812155, 'column_recall': 0.6018735362997658, 'cell_precision': 0.4708029197080292, 'cell_recall': 0.48405253283302063}


