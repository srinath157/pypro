def repeatcount(a):
    b = list(a)
    c = []
    idx = 0
    while idx < len(b):
        count=1
        if idx+1 < len(b):
            while b[idx] == b[idx+1]:
                count+=1
                idx+=1
                if idx + 1 == len(b):
                    break
            c.append(b[idx])
            c.append(str(count))
        else:
            c.append(b[idx])
            c.append(str(count))
        idx+=1
    return ''.join(c)


a = 'aabcdddrpppe'
print repeatcount(a)