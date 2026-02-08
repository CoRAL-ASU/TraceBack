import os
import json
import pandas as pd
import time
import re
from datetime import datetime
from LLM import Call_OpenAI, Call_Gemini, Call_DeepSeek
from subqueries import get_subqueries


def main():
	all_results = []
	file_path = '../Datasets/FetaQA/fetaQA_dev_processed.jsonl'
	model_name = 'gpt-4o'
	output_file_path = f'fetaqa_subqueries.json'
	count = 0
	#logging.basicConfig(filename = f'logs/fetaqa_{model_name}_subqueries.log', level=logging.INFO,format='%(asctime)s - %(message)s')
			
	with open(file_path, "r", encoding="utf-8") as file:
		for line in file:
			count += 1
	
			data = json.loads(line)

			# Extract desired fields
			feta_id = data.get("feta_id")
			question = data.get("question")
			answer = data.get("answer")
			table_array = data.get("table_array")
			column_headers = table_array[0]
			table_page_title = data.get("table_page_title")
			table_section_title = data.get("table_section_title")
			table_title = f"{table_page_title} - {table_section_title}"
			#table_title = f"AITQA-{feta_id}"

			logging.info(table_array)
			logging.info(question)

			logging.info('-'*50)
			logging.info(answer)
			logging.info(highlighted_cell_ids)


			
			
			#sub queries
			subqueries = get_subqueries(question,answer,column_headers,table_title)
			
			all_results.append({"feta_id": feta_id, "question":question, "sub-queries":subqueries})

			with open(output_file_path, "w", encoding="utf-8") as f:
				json.dump(all_results, f, indent=4)
			
			print(f"Done for query-{count}")

main()