import re

text = '''
		line:  To answer the sub-questions, we need to locate the specific rows and columns where "Masterpiece" received awards in 2010 and 2016, focusing on the specific awards and results.
line:  
line:  ### Answer:
line:  1. **What awards did Masterpiece receive in 2010?**
line:  - Rows and columns: [(1, 2), (2, 2)]
line:  
line:  In 2010, the rows involving "Masterpiece" receiving awards are:
line:  - Row 1: Award = "Most Popular Group"
line:  - Row 2: Award = "Best New Artist"
line:  
line:  2. **What were the results for each of these nominations/works?**
line:  - Rows and columns: [(1, 3), (2, 3)]
line:  
line:  The results for these are:
line:  - Row 1: Result = "Won"
line:  - Row 2: Result = "Won"
line:  
line:  3. **What awards did Masterpiece receive in 2016?**
line:  - Rows and columns: []
line:  
line:  There are no rows in 2016 where "Masterpiece" directly received an award as per the original table provided.
line:  
line:  4. **What were the results for each of these nominations/works?**
line:  - Rows and columns: []
line:  
line:  As there are no awards listed for "Masterpiece" in 2016 that were directly received in the original table, there are no results to report for this question.
line:  
line:  Thus, the final indexes where "<Original-Answer>" was found are:
line:  - Question 1: [(1, 2), (2, 2)]
line:  - Question 2: [(1, 3), (2, 3)]
line:  - Question 3 and 4: []
'''


def map_to_original_cols(ans,column_headers,relevant_cols):
	col_dict = {}
	for column_index in range(len(column_headers)):
		col_dict[column_headers[column_index]] = column_index
	print("Column Headers : ",column_headers,"\nRelevant Columns : ",relevant_cols)
	for i in range(len(ans)):
		cell = ans[i]
		if not cell:
			continue
		cell = list(cell)
		cell[1] = col_dict[relevant_cols[int(cell[1])]]
		ans[i] = cell

	return ans

def parse_attribution(text,column_headers,relevant_cols):
	pattern = re.compile(r'\[(.*?)\]$')

	final_answer = []

	# Split into lines and search for matches
	for line in text.splitlines():
		line = line.strip()
		'''
		match = pattern.search(line)

		if match:
			content = match.group(1).strip()  # The part inside [ ... ]
			content = '['+content+']'
			if content:
				try:
					lists = eval(content)
					print('lists', lists)

					# for l in lists:
					# 	if len(l) > 1:
					# 		final_answer.extend(l)
					# 	else:
					# 		final_answer.append(l)

				except:
					continue
				
			else:
				# If there's no content (i.e. an empty []), just store an empty tuple
				final_answer.append(())
		'''

		st = []
		for char in line:
			if char in ["(","[",","] or char.isnumeric():
				st.append(char)
			elif char in [")","]"]:
				res = ''
				while st:
					ch = st.pop()
					if ch in ["(","["]:
						break
					res+=ch
				try:
					tup = eval('('+res[::-1]+')')
					if tup:
						final_answer.append(tup)
				except:
					continue


	final_ans = map_to_original_cols(final_answer,column_headers,relevant_cols)
	print(final_answer)
	print(final_ans)
	return final_ans

parse_attribution(text,['Year', 'Nominee / work', 'Award', 'Result'],['Year', 'Nominee / work', 'Award', 'Result'])

'''import json
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


'''