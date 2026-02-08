import pandas as pd
import numpy as np
from LLM import Call_OpenAI, Call_Gemini, Call_DeepSeek
import json
def create_table_from_attributed_cells(attributed_cells, df):
    # Create an empty result array filled with placeholders
    
    attributed_cells = set(tuple(cell) for cell in attributed_cells)
    result_arr = np.full(df.shape, '-', dtype=object)

    # Track which rows are used
    rows_to_keep = set()

    for row_pos, col_pos in attributed_cells:
        row_pos_adj = row_pos   # offset to account for skipped header
        if 0 <= row_pos_adj < df.shape[0] and 0 <= col_pos < df.shape[1]:
            result_arr[row_pos_adj, col_pos] = df.iat[row_pos_adj, col_pos]
            rows_to_keep.add(row_pos_adj)


    # Convert to DataFrame
    result_df = pd.DataFrame(result_arr, columns=df.columns)

    # Return only the rows that contain attributed cells
    result_df = result_df.loc[sorted(rows_to_keep)]
    # if 'row_id' in result_df.columns:
    #     result_df = result_df.drop(columns=['row_id'])

    return result_df
def make_unique(headers):
    counts = {}
    unique = []
    for h in headers:
        counts[h] = counts.get(h, 0) + 1
        if counts[h] == 1:
            unique.append(h)
        else:
            unique.append(f"{h}_{counts[h]}")
    return unique

def convert_to_df(table_rows):
    max_cols = max(len(row) for row in table_rows)
    # print('original:\n', table_rows)
    fill_value = ''
    # Step 2: Normalize each row to have max_cols entries
    padded_rows = [row + [fill_value] * (max_cols - len(row)) for row in table_rows]
    raw_header = padded_rows[0]

    header = make_unique(raw_header)
    padded_rows = [header] + padded_rows[1:]

    # Step 4: Add row ids
    row_numbers = list(range(len(padded_rows)))
    # Step 5: Build DataFrame with row number column
    df = pd.DataFrame(padded_rows, columns=header)
    df.insert(0, "row_id", row_numbers)
    # Try to coerce datatypes
    df = df.apply(pd.to_numeric, errors='ignore')
    return df

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

def run_inference(instructions,df,attributed_cells,question):
    
    message = f"{instructions}\nInput :\nTable\n{df.to_string()}\nQuestion : {question}\nAttributed Cells: {attributed_cells}\nNow create atomic facts. Don't make atomic facts for cells which have value '-'. Don't repeat any atomic facts.Just give the final output and nothing else.\n"
    # print(message)
    response = model_response(message)
    return response

file_path = '../Datasets/FetaQA/fetaQA_dev_processed.jsonl'
model_name = 'gpt-4o'
model = Call_OpenAI(model_name)
output_file_path = f'fetaqa_results/fetaqa_pred_atomicfacts_{model_name}.json'
prompt_file_path = f"../Prompts/atomic_facts_from_predicted_cells.txt"
count = 0
all_results = {}
with open("fetaqa_results/fetaqa_gpt-4o_attribution_results.json","r") as f:
    res = json.load(f)

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
        result = get_result(feta_id)

        if highlighted_cell_ids is None:
            continue
        # Insert table into database
        df = convert_to_df(table_array)

        res_df = create_table_from_attributed_cells(result,df)


        instructions = load_prompt(prompt_file_path)

        response = run_inference(instructions,res_df,result,question)
        all_results[feta_id] = response

        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=4)
            

        print(f"Done for query-{count}")
        

        