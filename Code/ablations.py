import os
import json
import pandas as pd
import time
import re
from datetime import datetime
from LLM import Call_OpenAI, Call_Gemini, Call_DeepSeek
from relevant_col_gen import get_relevant_cols
from query_attribution import attribution
from subqueries import get_subqueries
from answer_attribution import answer_attribution

def col_filter_table(cols, table, header):
    indices = []
    for col in cols:
        indices.append(header.index(col))
    final = []
    for row in table:
        rows = []
        for index in indices:
            if index < len(row):
                rows.append(row[index])
            else:
                rows.append(row) # hierarchical table
        final.append(rows)
    return final

def main():
    all_results = []
    file_path = '../Datasets/FetaQA/fetaQA_dev_processed.jsonl'
    #file_path = '../Datasets/Totto/totto_processed.jsonl'
    model_name = 'gpt-4o'
    #output_file_path = f'aitqa_results/ablation/answer_attribution_{model_name}_subquery_each.json'
    output_file_path = f'fetaqa_results/ablation/answer_attribution_{model_name}_subquery_each.json'
    count = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            count += 1
            # if count < 38:
            #     continue
            # Extract desired fields
            feta_id = data.get("feta_id")
            question = data.get("question")
            answer = data.get("answer")
            table_array = data.get("table_array")
            column_headers = table_array[0]
            highlighted_cell_ids = data.get("highlighted_cells")
            table_page_title = data.get("table_page_title")
            table_section_title = data.get("table_section_title")
            table_title = f"{table_page_title} - {table_section_title}"

            # sub queries
            subqueries = get_subqueries(question, answer, column_headers, table_title)

            #relevant col extraction
            relevant_cols = get_relevant_cols(question, subqueries, answer, column_headers, table_title)
            table_array = col_filter_table(relevant_cols, table_array, column_headers)

            # attribution of subqueries with Table
            attributed_queries = attribution(subqueries, table_title, table_array, relevant_cols, answer)

            # Final Answer attribution
            attributed_answers = answer_attribution(answer, attributed_queries, table_title, table_array, relevant_cols)

            # Save Results
            all_results.append({"feta_id": feta_id, 'result': attributed_answers, "attributed_queries": attributed_queries, "column_headers": relevant_cols,
                                "highlighted_cell_ids": highlighted_cell_ids})

            with open(output_file_path, "w", encoding="utf-8") as f:
                json.dump(all_results, f, indent=4)

            print(f"Done for query-{count}")
main()