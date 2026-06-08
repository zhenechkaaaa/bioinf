import re

with open("qc/flagstat.txt") as f:
    text = f.read()

match = re.search(r"mapped \(([\d\.]+)%", text)

if not match:
    print("Mapping rate not found")
    exit(1)

rate = float(match.group(1))

print(f"Mapped: {rate}%")

if rate > 90:
    print("OK")
else:
    print("not OK")
