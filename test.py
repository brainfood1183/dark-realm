def combs(a):
    value = 0
    if len(a) == 0:
        return []
    for c in combs(a[1:]):
        cs = []
        cs = [c, c+[a[0]]]
    if len(cs) > 0:
        print(cs)
    return cs
    

nums = [1, 2, 3]
comb = combs(nums)

print(comb)

     # Expected output: [[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]]