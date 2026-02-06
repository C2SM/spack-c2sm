from pathlib import Path

with Path("log/artifacts_summary.html").open("w") as f:
    f.write("<html>\n")
    f.write("<body>\n")
    for file in sorted(Path("log").iterdir()):
        if file.suffix != ".log":
            continue
        second_last_line = file.read_text().split("\n")[-2]
        if "OK" in second_last_line:
            circle = "🟢"
        else:
            circle = "🔴"
        f.write(f'<a href="{file.name}">{circle} {file.stem}</a><br>\n')
    f.write("</body>\n")
    f.write("</html>\n")
