import os
skills_path = "/Users/mike/.openclaw/workspace-bacottibot/skills"
for name in sorted(os.listdir(skills_path)):
    desc = ""
    sk = os.path.join(skills_path, name, "SKILL.md")
    if os.path.exists(sk):
        with open(sk) as f:
            for line in f:
                if line.startswith("**Description:**") or line.startswith("Use when") or line.startswith("#"):
                    desc = line.strip().strip("#").strip()
                    break
    print(f"{name}: {desc or 'no description'}")
