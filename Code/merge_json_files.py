import json
import glob

def merge_json_files(input_files, output_file):
    merged_data = []

    for file in input_files:
        with open(file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)

                # If the file contains a list, extend it
                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    # If the file contains a single object, append it
                    merged_data.append(data)

            except json.JSONDecodeError as e:
                print(f"Error reading {file}: {e}")

    # Write to output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2)

    print(f"Merged {len(input_files)} files into '{output_file}' with {len(merged_data)} entries.")


if __name__ == "__main__":
    # Example: If all your files are named data1.json, data2.json, ..., data5.json
    input_files = ["aitqa_results/aitqa_answer_attribution_gpt-4o.json","aitqa_results/aitqa_answer_attribution_gpt-4o_1.json","aitqa_results/aitqa_answer_attribution_gpt-4o_2.json","aitqa_results/aitqa_answer_attribution_gpt-4o_3.json","aitqa_results/aitqa_answer_attribution_gpt-4o_4.json" ]
    
    # Output file
    output_file = "aitqa_results/aitqa_gpt-4o_attribution_results.json"
    
    # Merge and save
    merge_json_files(input_files, output_file)
