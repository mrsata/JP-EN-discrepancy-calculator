def jtranscript(j):
    t = j.replace('-', '').replace(' ','').replace('(','').replace(')','')
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

def main():
    while True:
        try:
            w = input()
            t = jtranscript(w)
            print(t)
        except EOFError:
            break

if __name__ == '__main__':
    main()
