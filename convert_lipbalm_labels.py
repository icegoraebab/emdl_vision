import os

LABEL_DIR = "lipbalm_dataset/labels"

for fname in os.listdir(LABEL_DIR):
    path = os.path.join(LABEL_DIR, fname)
    lines = open(path).readlines()

    new_lines = []
    for l in lines:
        parts = l.strip().split()
        if not parts:
            continue
        parts[0] = "1"  # lipbalm -> class 1
        new_lines.append(" ".join(parts) + "\n")

    with open(path, "w") as f:
        f.writelines(new_lines)

print("lipbalm labels converted to class 1")

