from LLM import Call_OpenAI, Call_Gemini, Call_DeepSeek
import json

prompt = "Given a table, question and answer, give the attribution for the answer based on the table as a list of (row_index,column_index) in plain text format. Just return the final answer and nothing else. Use 0-based indexing.\n"

all_results = []
file_path = '../Datasets/Totto/totto_processed.jsonl'
model_name = 'gpt-4o'
output_file_path = f'totto_results/directPrompting_answer_attribution_{model_name}_totto.json'
count = 0
model = Call_OpenAI(model_name)

def model_response(message):
	try:
		return model.call(message)
	except Exception as e:
		print(f"An unexpected error occurred in LLM: {e}")

with open(file_path, "r", encoding="utf-8") as file:
	for line in file:
		count += 1
		
		data = json.loads(line)

		# Extract desired fields
		feta_id = data.get("example_id")
		question = data.get("question")
		answer = data.get("answer")
		table_array = data.get("table_array")
		column_headers = table_array[0]
		highlighted_cell_ids = data.get("highlighted_cells")
		table_page_title = data.get("table_page_title")
		#table_section_title = data.get("table_section_title")
		#table_title = f"{table_page_title} - {table_section_title}"
		#table_title = f"AITQA-{feta_id}"
		table_title = table_page_title

		prompt += f"Table : {table_array}\n Question : {question}\nAnswer : {answer}\nJust give the finall attribution as a list of (row_index,column_index) in plain text format."

		response  = model_response(prompt)

		all_results.append({"feta_id": feta_id, "result": response})


		with open(output_file_path, "w", encoding="utf-8") as f:
			json.dump(all_results, f, indent=4)
			

		print(f"Done for query-{count}")
