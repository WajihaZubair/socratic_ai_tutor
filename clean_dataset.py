import json
import re

def fix_socratic_text(user_input, assistant_output):
    user_input = user_input.strip()
    assistant_output = assistant_output.strip()

    # Extract just the question part if there's a prefix like "strings: "
    actual_question = user_input
    if ":" in user_input:
        parts = user_input.split(":", 1)
        actual_question = parts[1].strip()  # This grabs just "How does a program..."

    # Check using the actual question text instead of the full input string
    if actual_question in assistant_output:
        parts = assistant_output.split(actual_question)
        prefix = parts[0].strip()
        suffix = parts[1].strip() if len(parts) > 1 else ""

        # Smooth out broken grammar connections
        if prefix.endswith("happens when"):
            prefix = prefix.replace("happens when", "happens?")
        elif prefix.endswith("figure out:"):
            prefix = prefix.replace("figure out:", "figure it out?")
        elif prefix.endswith("consider:"):
            prefix = prefix.replace("consider:", "consider this.")
        elif prefix.endswith("think:"):
            prefix = prefix.replace("think:", "think about it.")

        if prefix.endswith(":"):
            prefix = prefix[:-1].strip() + "."

        if not prefix.endswith(('.', '?', '!')):
            prefix += "."

        combined = f"{prefix} {suffix}".strip()
        combined = combined.replace("  ", " ")
        return combined

    return assistant_output

def process_file(input_filename, output_filename):
    cleaned_lines = []
    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)

                user_content = data["messages"][1]["content"]
                assistant_content = data["messages"][2]["content"]

                # Transform the assistant text
                data["messages"][2]["content"] = fix_socratic_text(user_content, assistant_content)
                cleaned_lines.append(data)

        with open(output_filename, "w", encoding="utf-8") as f:
            for line in cleaned_lines:
                json.dump(line, f, ensure_ascii=False)
                f.write("\n")
        print(f"✅ Cleaned: '{input_filename}' -> Saved as: '{output_filename}'")
    except FileNotFoundError:
        print(f"❌ Error: Could not find the file '{input_filename}'.")

# Run it
process_file("train.jsonl", "cleaned_train.jsonl")
process_file("valid.jsonl", "cleaned_valid.jsonl")
