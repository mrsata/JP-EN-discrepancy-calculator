def transcript(wi):
    t = wi
    t = t.replace('r', 'ɹ')
    t = t.replace('ja', 'd͡ʒja')
    t = t.replace('ju', 'd͡ʒju')
    t = t.replace('jo', 'd͡ʒjo')
    t = t.replace('j', 'd͡ʒ')
    t = t.replace('sha', 'ʃja')
    t = t.replace('shu', 'ʃju')
    t = t.replace('sho', 'ʃjo')
    t = t.replace('sh', 'ʃ')
    t = t.replace('cha', 't͡ʃja')
    t = t.replace('chu', 't͡ʃju')
    t = t.replace('cho', 't͡ʃjo')
    t = t.replace('ch', 't͡ʃ')
    t = t.replace('ts', 't͡s')
    t = t.replace('y', 'j')
    return t

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
    t = transcript(w)
    t = t.replace('-', '').replace(' ','').replace('(','').replace(')','')
    # ti = index_t(t)
    # print("{}, {}".format(t, ti))
    print(t)
