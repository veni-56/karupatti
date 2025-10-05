# Python 3 script; v0 can execute scripts in /scripts.
import os

def remove_empty_dirs(root):
    removed = []
    for current, dirs, files in os.walk(root, topdown=False):
        # Only remove if truly empty
        if not dirs and not files:
            try:
                os.rmdir(current)
                removed.append(current)
            except OSError:
                pass
    return removed

if __name__ == "__main__":
    # v0 runs from project root; ensure correct relative path
    target = "frontend"
    if os.path.isdir(target):
        removed = remove_empty_dirs(target)
        print("[v0] Removed empty directories:", removed)
    else:
        print("[v0] frontend directory does not exist or already cleaned.")
