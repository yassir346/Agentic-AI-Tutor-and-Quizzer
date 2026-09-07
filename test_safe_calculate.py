from tools import calculate

print(calculate("12 * (7 + 3)"))
print(calculate("100 / 4 - 5"))

try:
    print(calculate("open('notes.txt').read()"))
except ValueError as e:
    print("Blocked as expected:", e)