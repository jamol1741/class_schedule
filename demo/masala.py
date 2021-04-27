n = int(input())
items = list(map(int, input().split()))

found_lmin = False
found_lmax = False
l_min = 0
l_max = 0

for i in range(1, len(items)-1):
    if not found_lmin:
        if items[i-1] > items[i] < items[i+1]:
            l_min = i+1
            found_lmin = True
    if items[i-1] < items[i] > items[i+1]:
        l_max = i + 1
        found_lmax = True

if found_lmin and found_lmax:
    print(l_min, l_max)
else:
    print(0)
