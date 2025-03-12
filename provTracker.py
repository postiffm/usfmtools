# Verses per chapter in Proverbs
#       1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
Prov = [33,22,35,27,23,35,27,36,18,32,31,28,25,35,33,33,28,24,29,30,31,29,35,34,28,28,27,28,27,33,31]

for c, verses in enumerate(Prov):
    print(f"Proverbs {c+1} => ", end="")
    for v in range(verses):
        print(f"{v+1} ", end="")
    print("") # line end