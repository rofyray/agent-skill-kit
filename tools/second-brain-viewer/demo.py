"""Create a clearly labeled synthetic vault for local viewer verification."""
import argparse
import random
import subprocess
import sys
from datetime import date
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("output", type=Path)
parser.add_argument("--pages", type=int, default=160)
args = parser.parse_args()
root = args.output.resolve()
if root.exists():
    parser.error("choose a new directory; existing data is never overwritten")
script = Path(__file__).resolve().parents[2]/"skills/build-and-maintain-a-second-brain/scripts/second_brain.py"
subprocess.run([sys.executable, str(script), "init", str(root), "--name", "The connected mind (demo)"], check=True, stdout=subprocess.DEVNULL)
(root/"raw/demo.txt").write_text("Synthetic demonstration material. Not research evidence.\n")
subprocess.run([sys.executable, str(script), "record-raw", str(root), "--all-new"], check=True, stdout=subprocess.DEVNULL)
groups = {
    "Learning & memory": ["Spaced repetition", "Retrieval practice", "Mental models", "Working memory", "Desirable difficulty", "Transfer of learning", "Metacognition", "Feedback loops"],
    "Creative practice": ["Visual storytelling", "Creative constraints", "Iteration", "Composition", "Rhythm", "Observation", "Analogical thinking", "Design critique"],
    "Systems & technology": ["Knowledge graphs", "Emergence", "Networks", "Information retrieval", "Agent workflows", "System boundaries", "Modularity", "Provenance"],
    "Work & decisions": ["Decision journals", "Opportunity cost", "Prioritization", "Team learning", "Experiments", "Uncertainty", "Long-term thinking", "Attention"]
}
names = list(groups)
random.seed(7)
index = {name: [] for name in names}
for i in range(args.pages):
    group = names[i % len(names)]
    items = groups[group]
    title = items[(i//len(names)) % len(items)]
    if i >= 32:
        title += f": exploration {i//32 + 1}"
    name = f"idea-{i:05d}"
    index[group].append(name)
    destinations = {(i + len(names)) % args.pages, (i + 1) % args.pages, random.randrange(args.pages), random.randrange(args.pages)} if args.pages else set()
    links = "\n".join(f"- [[idea-{j:05d}]]" for j in sorted(destinations) if j != i)
    status = "contested" if i % 23 == 0 else "provisional" if i % 11 == 0 else "current"
    (root/"wiki"/f"{name}.md").write_text(f'---\ntitle: "{title}"\nsummary: "A synthetic example of {title.lower()}, illustrating how an idea connects across a personal knowledge collection."\ntype: concept\nstatus: {status}\ncreated: {date.today()}\nupdated: {date.today()}\nsources:\n  - raw/demo.txt#example\ntags:\n  - demonstration\n---\n\nDemonstration only.\n\n{links}\n')
(root/"index.md").write_text("# Demonstration index\n\n" + "\n\n".join(f"## {group}\n" + "\n".join(f"- [[{name}]]" for name in entries) for group, entries in index.items()))
subprocess.run([sys.executable, str(script), "visualize", str(root), "--json"], check=True)
