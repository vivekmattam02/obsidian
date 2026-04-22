import os

vault_dir = "/home/vivek/Desktop/Projects/server/vault/"
output_file = "/home/vivek/Desktop/Projects/server/README.md"

# Logical order for the combined document
files = [
    "00 Active Perception Bible.md",
    "Active Inference.md",
    "Extended Kalman Filter.md",
    "Mahalanobis Distance.md",
    "Data Association.md",
    "Triangulation.md",
    "Behavior Trees.md",
    "ROS 2 TF Trees.md",
    "DDS Quality of Service.md",
    "KAMRUI AK1PLUS Mini PC.md",
    "Jetson Edge Node.md",
    "Pan-Tilt Actuation.md",
    "Digital Twin.md"
]

with open(output_file, 'w') as out:
    out.write("<h1 align='center'>The Active Perception Engine</h1>\n\n")
    out.write("> *A First-Principles Distributed Architecture for Embodied Cognition*\n\n---\n\n")
    
    for f in files:
        fpath = os.path.join(vault_dir, f)
        if os.path.exists(fpath):
            with open(fpath, 'r') as infile:
                content = infile.read()
                # Strip Obsidian YAML frontmatter (tags, etc.)
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()
                out.write(content + "\n\n---\n\n")

print("Combined vault into README.md successfully!")
