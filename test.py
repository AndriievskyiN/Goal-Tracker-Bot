a = [("Nikita", 15, 2, 14), ("Nikita", 20, 5, 10), ("Nikita", 10, 1, 40)]

data = sorted(a, key=lambda x: -x[3])
for i in data:
    print(i)