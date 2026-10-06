import re

pattern = re.compile(r"ab{2,3}")
for sample in ("abb", "abbb", "ab", "abbbb"):
    print(f"{sample!r}: {bool(pattern.fullmatch(sample))}")
