import os
from datetime import datetime

folders = ["Cywilna", "Apelacja", "Egzekucja"]

for folder in folders:
    path = os.path.join(os.getcwd(), folder)
    if not os.path.isdir(path):
        continue

    files = []
    for fname in os.listdir(path):
        if fname.lower() in ["knowledge.md", "reader.txt", "readme.md"]:
            continue
        fpath = os.path.join(path, fname)
        if os.path.isfile(fpath):
            stat = os.stat(fpath)
            files.append({
                "name": fname,
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "ext": os.path.splitext(fname)[1][1:].upper()
            })

    files.sort(key=lambda x: x["mtime"], reverse=True)

    knowledge_path = os.path.join(path, "knowledge.md")
    with open(knowledge_path, "w", encoding="utf-8") as f:
        f.write(f"# Indeks dokumentów – {folder}\n\n")
        f.write(f"**Ostatnia aktualizacja:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Lista plików:\n\n")
        for file in files:
            f.write(f"- **{file['name']}** ({file['ext']}, {file['size']} bajtów, dodano: {file['mtime']})\n")
        f.write("\n---\n")
        f.write("## Notatki i podsumowania (do uzupełnienia przez zespół):\n\n")
        f.write("- [Dodaj tu streszczenia, kluczowe informacje, komentarze do nowych dokumentów]\n")
