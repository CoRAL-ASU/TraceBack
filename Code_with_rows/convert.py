import json
'''
input_file = 'fetaqa_results/fetaqa_pred_alignment_gpt-4o.json'
output_file = 'fetaqa_results/fetaqa_pred_alignment.json'
processed_ids = set()
try:
    with open(output_file, "r", encoding="utf-8") as f_out:
        file = json.load(f_out)
        for line in file:
            try:
                processed_ids.add(line)
            except json.JSONDecodeError:
                continue  # skip malformed lines
except:
    pass


out = {}
with open(input_file, "r") as f_in:
    file = json.load(f_in)
    for line in file:
        print("\n=== Entry ID:", line)
        if line in processed_ids:
            continue
        ans = file[line].split('\n')[1:]
        dic = {}
        # print(ans)
        for i in ans:
            a,b = i.split(':')
            dic[a.strip()] = int(b.strip())
        out[line] = dic
with open(output_file, "w") as f:
    json.dump(out, f, indent = 4)
'''

with open('fetaqa_results/fetaqa_pred_alignment.json',"r") as f:
    out = json.load(f)

a = 0
b = 0
c = 0
d = 0
for feta_id in out:
    item = out[feta_id]
    try:
        a += item["Number of atomic facts in 1 covered by 2"]
        b += (item["Total Number of facts in Set-1"] )
        c += item["Total number of facts in Set-2"]
        d += item["Number of atomic facts in 2 that are unnecessary"]
    except:
        print(feta_id)
print(a,b)
print("recall : ",(a/(b))*100)
print("precision : ",((c-d)/c)*100)
'''
Eval Model Prediction
Gold : recall :  55.51839464882943 precision :  69.43462897526503
Predicted : recall :  44.33164128595601 precision :  57.66192733017378

Groundtruth Prediction
cell_recall: 0.7502958579881657 cell_precision: 0.7115600448933782
'''