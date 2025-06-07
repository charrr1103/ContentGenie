# check_null_bytes.py
import os

def check_file_for_null_bytes(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        if b'\x00' in content:
            print(f"❌ Null byte found in: {file_path}")
        else:
            print(f"✅ Clean: {file_path}")

files_to_check = [
    "agents/subagents/audience_analyst_agent.py",
    "agents/subagents/copywriter_agent.py",
    "agents/subagents/formatter_agent.py",
]

for path in files_to_check:
    if os.path.exists(path):
        check_file_for_null_bytes(path)
    else:
        print(f"⚠️ File not found: {path}")
