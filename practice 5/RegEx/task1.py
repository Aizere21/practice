import re

pattern = re.compile(r"ab*")
for sample in ("a", "ab", "abbb", "ac", "ba"):
    print(f"{sample!r}: {bool(pattern.fullmatch(sample))}")

