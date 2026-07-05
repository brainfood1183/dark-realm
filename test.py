import itertools

result = set()
n = 5

def backtrack(s="", open_count=0, close_count=0):
    if len(s) == 2 * n:
        result.add(s)  # store as string
        return
    if open_count < n:
        backtrack(s + "(", open_count + 1, close_count)
    if close_count < open_count:
        backtrack(s + ")", open_count, close_count + 1)

backtrack()
print(list(result))




n = 4
result = set()

def new_backtrack(ret="", back_count=0, for_count=0):
    if len(ret) == 2 * n:
        result.add(ret)
        return
    if back_count < n:
        new_backtrack(ret + "a", back_count + 1, for_count)
    if for_count < back_count:
        new_backtrack(ret + "b", back_count, for_count + 1)

new_backtrack()
print(list(result))









