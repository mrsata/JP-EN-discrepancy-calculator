import conversion.conversion as c

def etranscript(e):
    t = c.convert(e)
    t = t.replace('r', 'ɹ')
    t = t.replace('-', '').replace(' ','')
    return t

def main():
    while True:
        try:
            w = input()
            t = etranscript(w)
            print(t)
        except EOFError:
            break

if __name__ == '__main__':
    main()
