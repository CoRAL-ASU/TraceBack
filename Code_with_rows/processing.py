import ast
import json

# Assume 'data' is your huge pasted list (just assign your data to this variable)
predicted_file_path = "totto_results/directPrompting_answer_attribution_gpt-4o_totto.json"
with open(predicted_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
   # <- Replace this with your list

# Convert each "result" to a proper list of lists
for item in data:
    result = item.get("result")
    if result is None:
        item["result"] = []
    else:
        try:
            # Handle messy formatting: newlines, missing brackets
            fixed_result = result.replace("\n", ",").replace("[", "(").replace("]", ")")
            # If not starting with '[', wrap it for safe eval
            parsed = ast.literal_eval(f"[{fixed_result}]") if not fixed_result.strip().startswith("[") else ast.literal_eval(fixed_result)
            # Convert tuples to lists
            item["result"] = [list(tup) for tup in parsed]
        except Exception as e:
            print(f"Error parsing feta_id {item.get('feta_id')}: {e}")
            item["result"] = []

# (Optional) Save the fixed data to a file
with open("converted_results.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Conversion Done. Ready to use!")
