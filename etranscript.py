import conversion.conversion as c

def index_w(w):
    wi = ""
    n = 1
    for i in range(len(w)):
        wi += w[i]
        if w[i] == 'c' or w[i] == '-' or w[i] == ' ': continue
        elif w[i] == 't':
            if i < len(w) - 1 and w[i + 1] == 's':
                continue
        wi += str(n)
        n += 1
    return wi

def index_t(t):
    ti = ""
    n = 1
    for i in range(len(t)):
        ti += t[i]
        if t[i] == '͡' or t[i] == '-' or t[i] == ' ': continue
        elif t[i] == 'd' or t[i] == 't':
            if i < len(t) - 1 and t[i + 1] == '͡':
                continue
        ti += str(n)
        n += 1
    return ti

n = int(input())  # read a line with a single integer
for i in range(1, n + 1):
    w = input()
    t = c.convert(w)
    t = t.replace('r', 'ɹ')
    t = t.replace('-', '').replace(' ','')
    ti = index_t(t)
    print(t)