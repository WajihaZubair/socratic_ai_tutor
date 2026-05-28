import json

import re

def clean_socratic_output(user_input, assistant_output):
    user_input = user_input.strip()
    assistant_output = assistant_output.strip()

    # 1. Remove the exact user input from the assistant response
    if user_input in assistant_output:
        # Replace the question with an empty string
        cleaned = assistant_output.replace(user_input, "").strip()

        # 2. Clean up punctuation artifacts left behind (e.g., ": ?", "??", "colon followed by space")
        cleaned = cleaned.replace(": ?", "?")
        cleaned = cleaned.replace(":\n", "")
        cleaned = re.sub(r':\s*[A-Z]', lambda m: '. ' + m.group()[-1], cleaned) # turns ": Why" into ". Why"
        cleaned = cleaned.replace("  ", " ") # Remove double spaces

        # 3. Final polish if a colon or extra punctuation is stuck at the front or middle
        cleaned = re.sub(r'\s+([?.!,])', r'\1', cleaned) # fix spaces before punctuation
        return cleaned.strip()

    return assistant_output

def to_qwen(example):
    # Pass input and output to the cleaner function
    cleaned_output = clean_socratic_output(example["input"], example["output"])

    return {
        "messages": [
            {
                "role": "system",
                "content": example.get("instruction", "Socratic programming tutor") # Default to your tutor prompt
            },
            {
                "role": "user",
                "content": example["input"]
            },
            {
                "role": "assistant",
                "content": cleaned_output # Now using the beautiful, cleaned version!
            }
        ]
    }

input_file = "dataset.json"
train_out = "train.jsonl"
valid_out = "valid.jsonl"

# ✅ load safely (JSON or JSONL)
with open(input_file, "r", encoding="utf-8") as f:
    try:
        data = json.load(f)  # JSON array case
    except json.JSONDecodeError:
        f.seek(0)
        data = [json.loads(line) for line in f if line.strip()]  # JSONL case

# split
split = int(0.9 * len(data))
train_data = data[:split]
valid_data = data[split:]

# write train
with open(train_out, "w", encoding="utf-8") as f:
    for item in train_data:
        json.dump(to_qwen(item), f, ensure_ascii=False)
        f.write("\n")

# write valid
with open(valid_out, "w", encoding="utf-8") as f:
    for item in valid_data:
        json.dump(to_qwen(item), f, ensure_ascii=False)
        f.write("\n")

print("✅ Cleaned Qwen dataset ready with zero repetitions!")
