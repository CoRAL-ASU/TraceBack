import pandas as pd
import numpy as np
from LLM import Call_OpenAI, Call_Gemini, Call_DeepSeek
import json

def get_result(id):
    for item in res:
        if item["feta_id"]==id:
            return item["highlighted_cell_ids"]

def load_prompt(txt_file_path):
    try:
        # Try reading with UTF-8 encoding
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except UnicodeDecodeError:
        print(f"UTF-8 decoding failed for {txt_file_path}. Trying ISO-8859-1...")
        try:
            # Fallback to ISO-8859-1 encoding
            with open(txt_file_path, 'r', encoding='ISO-8859-1') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading prompt file with fallback encoding: {str(e)}")
            return ""
    except FileNotFoundError:
        print(f"Prompt file not found at {txt_file_path}")
        return ""
    except Exception as e:
        print(f"Error reading prompt file: {str(e)}")
        return ""

def model_response(message):
    try:
        return model.call(message)
    except Exception as e:
        print(f"An unexpected error occurred in LLM: {e}")

def run_inference(instructions,question,table_title,column_headers,feta_id):
    set1_facts = set1[str(feta_id)]
    set2_facts = set2[str(feta_id)]
    
    message = f"{instructions}\nInput :\nSet-1\n{set1_facts}\nSet-2\n{set2_facts}\nQuestion : {question}\nColumn Headers: {column_headers}\n"
    # print(message)
    response = model_response(message)
    return response

file_path = '../Datasets/FetaQA/fetaQA_dev_processed.jsonl'
model_name = 'gpt-4o'
model = Call_OpenAI(model_name)
output_file_path = f'fetaqa_results/fetaqa_pred_alignment_{model_name}.json'
prompt_file_path = f"../Prompts/alignment.txt"
count = 0
all_results = {}
with open("fetaqa_results/fetaqa_gold_answeratomicfacts_gpt-4o.json","r") as f:
    set1 = json.load(f)
with open("fetaqa_results/fetaqa_pred_atomicfacts_gpt-4o.json","r") as f:
    set2 = json.load(f)

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
        highlighted_cell_ids = data.get("highlighted_cells")
        table_page_title = data.get("table_page_title")
        table_section_title = data.get("table_section_title")
        table_title = f"{table_page_title} - {table_section_title}"
        #table_title = f"AITQA-{feta_id}"
        
        if highlighted_cell_ids is None:
            continue
        # Insert table into database
        
        instructions = load_prompt(prompt_file_path)

        response = run_inference(instructions,question,table_title,column_headers,feta_id)
        all_results[feta_id] = response

        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=4)
            

        print(f"Done for query-{count}")
        
        

        