list=[1,2,3,4,5]
chance = None
for i in range(20):
    if chance:
        chance = ((chance) % len(list)) + 1
    else:
        chance = 1
    print(chance)
