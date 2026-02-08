import json

input_file = '../Datasets/AITQA/aitqa.jsonl'
output_file = '../Datasets/AITQA/aitqa_processed.jsonl'
processed_ids = set()
try:
    with open(output_file, "r", encoding="utf-8") as f_out:
        for line in f_out:
            try:
                processed_entry = json.loads(line)
                processed_ids.add(processed_entry["id"])
            except json.JSONDecodeError:
                continue  # skip malformed lines
except FileNotFoundError:
    pass  # no output file yet

with open(input_file, "r", encoding="utf-8") as f_in:
    for line in f_in:
        entry = json.loads(line)
        if entry["id"] in processed_ids:
            continue
        print("\n=== Entry ID:", entry["id"])


        # Display the table
        print("Table:")
        table = entry.get("table", [])
        for i, row in enumerate(table):
            print(f"{i:2d}: {row}")

        print("Question:", entry.get("question", "N/A"))
        print('Answer: ', entry.get("answers", "N/A"))
        print('row_hierarchy_needed: ', entry.get("row_hierarchy_needed", "N/A"))

        # Prompt user for highlighted_cells
        raw_input_str = input("Enter highlighted_cells as list of (row_idx, col_idx), or press Enter to skip: ")
        try:
            if raw_input_str.strip():
                highlighted_cells = eval(raw_input_str)
                if isinstance(highlighted_cells, list):
                    entry["highlighted_cells"] = highlighted_cells
                else:
                    print("⚠️Input was not a list, skipping highlight.")
            else:
                print("No highlights added.")
        except Exception as e:
            print(f"Invalid input ({e}), skipping highlight.")

        with open(output_file, "a", encoding="utf-8") as f_out:
            f_out.write(json.dumps(entry) + "\n")
