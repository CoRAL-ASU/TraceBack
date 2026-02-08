import json
import openai
from openai import OpenAI
from LLM import Call_OpenAI, Call_Gemini, Call_DeepSeek

def parse_json_line(json_line: str):
	"""
	Parses one JSON line of your file, returning:
	  - table_title (str)
	  - answer (str)
	  - highlighted_cells (list[list[int]])
	  - example_id (int or str)
	  - table_as_list (list[list[str]])
	"""
	data = json.loads(json_line.strip())

	# 1) Extract "table_title"
	#    Depending on your data, you might choose table_page_title
	#    or table_section_title. Adjust as needed.
	table_title = data.get("table_page_title", "") or data.get("table_section_title", "")

	# 2) Extract an answer from any one final_sentence in sentence_annotations
	#    We'll just pick the first one we see, if multiple exist.
	answer = None
	annotations = data.get("sentence_annotations", [])
	for annotation in annotations:
		fs = annotation.get("final_sentence")
		if fs:  # If there's a non-empty final_sentence, use it and break
			answer = fs
			break

	# 3) Extract highlighted_cells
	#    This might be a list of [row, col], e.g. [[3, 0], [3, 2], [3, 3]]
	#    We'll simply return it as is.
	highlighted_cells = data.get("highlighted_cells", [])

	# 4) Extract example_id
	example_id = data.get("example_id")

	# 5) Convert the "table" field to a 2D list of strings
	table_data = data.get("table", [])
	table_as_list = []
	for row in table_data:
		# Each 'row' is a list of cell dictionaries
		row_values = [cell.get("value", "") for cell in row]
		table_as_list.append(row_values)

	return table_title, answer, highlighted_cells, example_id, table_as_list

def model_response(message,model):
	try:
		return model.call(message)
	except Exception as e:
		print(f"An unexpected error occurred in LLM: {e}")


def main():
	# Update with the actual path to your JSONL file
	jsonl_file = "../../Datasets/totto_data/totto_dev_data.jsonl"
	model_name = 'DeepSeek-V3-0324'
	model = Call_DeepSeek(model_name)
	output_file_path = f'../Datasets/totto_dataset_w_questions.json'
	data = []
	count = 0

	with open(jsonl_file, "r", encoding="utf-8") as f:
		for line_idx, line in enumerate(f, start=1):
			# Parse each JSON record
			table_title, answer, highlighted_cells, example_id, table_as_list = parse_json_line(line)

			prompt = f"Given the answer based on a table, and the table column names. Construct a question for the answer based on the table. Just return the question and nothing else.\n <Table-Columns> : {table_as_list[0]}\n<Answer>:{answer}\n\nQuestion:"

			question = model.call(prompt)

			#question = question.split("</think>")[1]

			data.append({"example_id":example_id,"table_page_title":table_title,"question":question,"answer":answer,"highlighted_cells":highlighted_cells,"table_array":table_as_list})
			count+=1
			print(f"Done for example-{count}")


			with open(output_file_path, 'w', encoding='utf-8') as f:
				for item in data:
					json.dump(item, f)
					f.write('\n')



if __name__ == "__main__":
	main()
