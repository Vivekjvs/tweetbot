def match(string) -> int:
    pattern = "place:"
    arr = z(pattern+"/0"+string)
    for i in range(len(arr)):
        if arr[i] == len(pattern):return i - (len(pattern) + 1) -1
    return -1

def z(string: str) -> list:
    z_val = [0] * len(string)
    i = left = right = 1
    while i < len(string):
        if right <= i:
            left = right = i
            while right < len(string) and string[right] == string[right - left]:
                z_val[i] += 1
                right += 1
            if right == len(string):break
            i += 1
        else:
            i = right
            j = left + 1
            while j < right and j + z_val[j - left] < right:
                z_val[j] = z_val[j - left]
                j += 1
            if j < right:
                left = j
                z_val[j] = right - j
                while string[right] == string[right - left]:
                    z_val[j] += 1
                    right += 1
    return z_val