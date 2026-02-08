# Table-Attribution

This repository contains table-answer attribution code centered on:
- TraceBack (ours)
- CITEBENCH evaluation
- FAIRScore (reference-less evaluation)
- CITEBENCH baseline included in this repo: ICL

This cleaned version intentionally excludes GenerationPrograms and Inseq components.

## 1) Project Layout

Key scripts:
- `traceback_workflow.py`: shared 5-step TraceBack workflow used by dataset runners
- `Code/main.py`: TraceBack runner for AITQA
- `Code_with_rows/main.py`: TraceBack runner for FetaQA
- `Code_with_rows/totto_traceback.py`: TraceBack runner for ToTTo
- `Code/eval_script.py`, `Code_with_rows/eval_script.py`, `Code_with_rows/eval_totto.py`: per-dataset P/R evaluation
- `Code/eval_traceback_md.py`: one-shot markdown table for AITQA/FetaQA/ToTTo
- `Code/traceback_citebench_full.py`: TraceBack over unified CITEBENCH
- `Code/eval_citebench_all.py`: CITEBENCH evaluator for style-based outputs
- `Code/eval_fairscore.py`: FAIRScore evaluation
- `Code/icl_runner.py`: CITEBENCH ICL baseline

Prompt files:
- TraceBack prompts: `Prompts/`
- ICL prompt templates: `Prompts_2/`

Datasets:
- `Datasets/AITQA/aitqa_processed.jsonl`
- `Datasets/FetaQA/fetaQA_dev_processed.jsonl`
- `Datasets/Totto/totto_processed.jsonl`
- `Datasets/CITEBENCH.json`

## 2) Environment

Required (core):
```bash
pip install pandas sqlalchemy pymysql tqdm openai
```

Optional by backend:
- Gemini backend: `pip install google-genai`
- Local HF backend: `pip install torch transformers accelerate`

Environment variables (as needed by backend):
- `OPENAI_API_KEY`
- `GEMINI_API_KEY` or `GEMINI_API_KEYS`
- `DEEPINFRA_API_KEY` or `DEEPSEEK_API_KEY`
- `NOVITA_API_KEY`
- `HF_TOKEN` or `HUGGINGFACE_HUB_TOKEN` (for gated HF models)

## 3) TraceBack on AITQA / FetaQA / ToTTo

### AITQA
Run:
```bash
python Code/main.py
```
Evaluate:
```bash
python Code/eval_script.py
```

### FetaQA
Run:
```bash
python Code_with_rows/main.py
```
Evaluate:
```bash
python Code_with_rows/eval_script.py
```

### ToTTo
Run:
```bash
python Code_with_rows/totto_traceback.py
```
Evaluate:
```bash
python Code_with_rows/eval_totto.py
```

### Local HF TraceBack runs
```bash
python Code/main.py --backend hf --model Qwen/Qwen2.5-7B-Instruct --resume
python Code_with_rows/main.py --backend hf --model google/gemma-3-4b-it --resume
python Code_with_rows/totto_traceback.py --backend hf --model Qwen/Qwen2.5-3B-Instruct --resume
```

Notes:
- For paper-faithful Step 2 row filtering, use MySQL setup in `MYSQL_USAGE.txt`.
- For quick runs without MySQL, add `--no-mysql` or `--no-row-filtering`.
- Use `--output` to avoid overwriting existing prediction files.
- Use `--resume` to continue interrupted runs.

### Combined TraceBack markdown table (AITQA/FetaQA/ToTTo)
```bash
python Code/eval_traceback_md.py --percent --output results/eval/metrics_traceback.md
```

## 4) CITEBENCH Experiments

### 4.1 TraceBack full pipeline on CITEBENCH
Run:
```bash
python Code/traceback_citebench_full.py \
  --citebench Datasets/CITEBENCH.json \
  --outdir results/TraceBack_full \
  --model gpt-4o
```

Evaluate:
```bash
python Code/eval_citebench_all.py \
  --results-root results/TraceBack_full \
  --gt Datasets/CITEBENCH.json \
  --styles traceback-full \
  --output results/eval/metrics_citebench_traceback_full.json
```

### 4.2 ICL baseline (CITEBENCH)
ICL prompt templates:
- `Prompts_2/answer_attr_zero.txt`
- `Prompts_2/answer_attr_zero_cot.txt`
- `Prompts_2/answer_attr_few.txt`
- `Prompts_2/answer_attr_few_cot.txt`

Run (OpenAI example):
```bash
python Code/icl_runner.py \
  --backend openai \
  --models gpt-4o \
  --styles zero zero-cot few few-cot \
  --limit 0 \
  --resume
```

Evaluate:
```bash
python Code/eval_citebench_all.py \
  --results-root results/ICL \
  --gt Datasets/CITEBENCH.json \
  --styles zero zero-cot few few-cot \
  --output results/eval/metrics_citebench_icl.json
```

## 5) FAIRScore (Reference-less)

Default run over TraceBack outputs:
```bash
python Code/eval_fairscore.py --cells pred --backend openai --model gpt-4o
```

Parallel requests (be mindful of rate limits):
```bash
python Code/eval_fairscore.py --cells pred --backend openai --model gpt-4o --workers 4 --max-inflight 4
```

Score both predicted and gold cells:
```bash
python Code/eval_fairscore.py --cells both --backend openai --model gpt-4o
```

Outputs:
- Summary markdown: `results/eval/metrics_fairscore.md`
- Summary JSON: `results/eval/metrics_fairscore.json`
- Cache files: `results/fairscore/`

Use a unified CITEBENCH-style prediction file via `--preds`:
```bash
python Code/eval_fairscore.py \
  --preds results/ICL/gpt-4o/few-cot.json \
  --pred-tag few-cot \
  --cells pred \
  --backend openai --model gpt-4o \
  --workers 4 --max-inflight 4 \
  --summary-md results/eval/metrics_fairscore_few-cot.md \
  --summary-json results/eval/metrics_fairscore_few-cot.json
```

## 6) MySQL (Optional, for strict TraceBack Step 2)

See `MYSQL_USAGE.txt` for full setup/start/stop instructions.
