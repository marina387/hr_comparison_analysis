# create_hf_csv.py
import json
import pandas as pd
import os

folder = "./data/huggingface/raw"
all_data = []

for file in os.listdir(folder):
    if file.endswith('.json'):
        with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data.get('output', {}).get('valid_resume_and_jd', False):
                row = {
                    'file_name': file,
                    'macro_scores_avg': data.get('output', {}).get('scores', {}).get('aggregated_scores', {}).get('macro_scores'),
                    'micro_scores_avg': data.get('output', {}).get('scores', {}).get('aggregated_scores', {}).get('micro_scores'),
                    'name': data.get('details', {}).get('name', ''),
                    'skills': ', '.join(data.get('details', {}).get('skills', [])[:5]),
                    'justification': data.get('output', {}).get('justification', [''])[0][:200] if data.get('output', {}).get('justification') else ''
                }
                all_data.append(row)

df = pd.DataFrame(all_data)
df.to_csv('./data/huggingface/resume_scores_clean.csv', index=False, encoding='utf-8')
print(f"✅ Создан CSV: {len(df)} строк")