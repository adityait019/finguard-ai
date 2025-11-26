# Helper to read prompt files
import os
def load_prompt(filename):
    # Assuming prompts are in a 'prompts' folder relative to this file
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'prompts', filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()