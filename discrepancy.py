import functools
import multiprocessing
import os

ENVOWEL = set(['a', 'e', 'i', 'o', 'u', 'ə', 'ɑ', 'æ', 'ʊ', 'ɪ', 'ɔ', 'ɛ'])
JPVOWEL = set(['a', 'e', 'i', 'o', 'u'])

def preprocess(j):
    prev_c = ""
    final_string = ""
    rules = []
    for i, c in enumerate(j):
        if c == prev_c and c not in JPVOWEL:
            rules.append((i-1, ("d", "")))
        else:
            final_string += c
        prev_c = c
    return (final_string, rules)

def alignment(pre_rule, main_rule):
    main_rule = main_rule[:]
    final_rule = []
    for pre in pre_rule:
        for rule in main_rule:
            if rule[0] >= pre[0]:
                final_rule.append((rule[0]+1, rule[1]))
            else:
                final_rule.append(rule)
        main_rule = final_rule
        final_rule = []
    final_rule = main_rule
    final_rule.extend(pre_rule)
    return list(sorted(final_rule, key=lambda x:x[0]))

def generate_lists(j, e, rule):
    counter = 1
    replace_results = ""
    jap_results = ""
    eng_results = ""
    for i, j_char in enumerate(j):
        matched = False
        for r in rule:
            if i == r[0]:
                matched = True
                if r[1][0] == "i":
                    eng_results += r[1][1] + str(counter)
                    replace_results += "{m}.ø/{i} ".format(m=str(counter), i=r[1][1])
                    if len(rule) == 1:
                        counter+=1
                        jap_results += j_char + str(counter)
                        eng_results += j_char + str(counter)
                elif r[1][0] == "d":
                    if j[i-1] == '͡':
                        eng_results = eng_results[:-2]
                        replace_results += "{m}.{i}/ø ".format(m=str(counter), i=j[i-2:i+1])
                    else:
                        replace_results += "{m}.{i}/ø ".format(m=str(counter), i=j_char)
                    jap_results += j_char + str(counter)
                elif r[1][0] == "c":
                    if j[i-1] == '͡':
                        eng_results = eng_results[:-2]
                        replace_results += "{m}.{o}/{i} ".format(m=str(counter), o=j[i-2:i+1], i=r[1][1])
                    else:
                        replace_results += "{m}.{o}/{i} ".format(m=str(counter), o=j_char, i=r[1][1])
                    jap_results += j_char + str(counter)
                    eng_results += r[1][1] + str(counter)
                else:
                    raise RuntimeError("invalid operation")
                counter += 1
        if not matched:
            if j[i] == '͡' or j[min(i+1, len(j)-1)] == '͡':
                jap_results += j_char
                eng_results += j_char
                counter -=1
            else:
                jap_results += j_char + str(counter)
                eng_results += j_char + str(counter)
            counter += 1
    return (jap_results, eng_results, replace_results)

def discrepancy(j, e):
    main_rule = editDist(j, e, len(j), len(e))[1]
    return main_rule

def editDist(j, e, m, n):
    # If first string is empty, the only option is to
    # insert all characters of second string into first
    if m == 0: return (n, [])

    # If second string is empty, the only option is to
    # remove all characters of first string
    if n == 0: return (m, [])

    # If character with '͡' encountered
    if (m > 2 and j[m-2] == '͡') or (n > 2 and e[n-2] == '͡'):

        if j[m-1] == e[n-1] and j[m-3] == e[n-3]:
            return editDist(j, e, m-3, n-3)

        if m > 2 and j[m-2] == '͡' and n > 2 and e[n-2] == '͡':
            IS, RM, RP = [editDist(j, e, m, n-3)     # Insert
                        , editDist(j, e, m-3, n)     # Remove
                        , editDist(j, e, m-3, n-3)]  # Replace
            MIN = min(IS[0], RM[0], RP[0])
            if MIN == IS[0]:
                s=IS[1][:]
                s.append((m-1, ("i", e[n-3:n])))
            elif MIN == RM[0]:
                s=RM[1][:]
                s.append((m-1, ("d", j[m-3:m])))
            else:
                s=RP[1][:]
                s.append((m-1, ("c", e[n-3:n])))
            return (1 + MIN, s)

        if j[m-2] == '͡':
            IS, RM, RP = [editDist(j, e, m, n-1)     # Insert
                        , editDist(j, e, m-3, n)     # Remove
                        , editDist(j, e, m-3, n-1)]  # Replace
            MIN = min(IS[0], RM[0], RP[0])
            if MIN == IS[0]:
                s=IS[1][:]
                s.append((m-1, ("i", e[n-1])))
            elif MIN == RM[0]:
                s=RM[1][:]
                s.append((m-1, ("d", j[m-3:m])))
            else:
                s=RP[1][:]
                s.append((m-1, ("c", e[n-1])))
            return (1 + MIN, s)

        if e[n-2] == '͡':
            IS, RM, RP = [editDist(j, e, m, n-3)     # Insert
                        , editDist(j, e, m-1, n)     # Remove
                        , editDist(j, e, m-1, n-3)]  # Replace
            MIN = min(IS[0], RM[0], RP[0])
            if MIN == IS[0]:
                s=IS[1][:]
                s.append((m-1, ("i", e[n-3:n])))
            elif MIN == RM[0]:
                s=RM[1][:]
                s.append((m-1, ("d", j[m-1])))
            elif j[m-1] not in JPVOWEL:
                s=RP[1][:]
                s.append((m-1, ("c", e[n-3:n])))
            else:
                MIN = min(IS[0], RM[0])
                if MIN == IS[0]:
                    s=IS[1][:]
                    s.append((m-1, ("i", e[n-3:n])))
                else:
                    s=RM[1][:]
                    s.append((m-1, ("d", j[m-1])))
            return (1 + MIN, s)

    # If last characters of two strings are same, nothing
    # much to do. Ignore last characters and get count for
    # remaining strings.
    if j[m-1] == e[n-1]:
        return editDist(j, e, m-1, n-1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all three operations and take
    # minimum of three values.
    IS, RM, RP = [editDist(j, e, m, n-1)     # Insert
                , editDist(j, e, m-1, n)     # Remove
                , editDist(j, e, m-1, n-1)]  # Replace
    MIN = min(IS[0], RM[0], RP[0])
    if MIN == IS[0]:
        s=IS[1][:]
        s.append((m-1, ("i", e[n-1])))
    elif MIN == RM[0]:
        s=RM[1][:]
        s.append((m-1, ("d", j[m-1])))
    elif ((e[n-1] in ENVOWEL and j[m-1] in JPVOWEL) or (e[n-1] not in ENVOWEL and j[m-1] not in JPVOWEL) or (j[m-1] == 'a' and e[n-1]=='ɹ')) and j[m-1] != 'j' and not (e[n-1] == "ɹ" and j[m-1] != "a"):
        s=RP[1][:]
        s.append((m-1, ("c", e[n-1])))
    else:
        MIN = min(IS[0], RM[0])
        if MIN == IS[0]:
            s=IS[1][:]
            s.append((m-1, ("i", e[n-1])))
        else:
            s=RM[1][:]
            s.append((m-1, ("d", j[m-1])))
    return (1 + MIN, s)

def proc(pair):
    j, e = pair
    no_sokuon, pre_rule = preprocess(j)
    main_rule = discrepancy(no_sokuon, e)
    final_rule = alignment(pre_rule, main_rule)
    jp, en, rp = generate_lists(j, e, final_rule)
    return "{}, {}, {}".format(jp, en, rp)

n = int(input())  # read a line with a single integer
pairs = []
for i in range(1, n+1):
    j, e = [s for s in input().split(" ")]
    pairs.append((j, e))
with multiprocessing.Pool(8) as p:
    results = p.map(proc, pairs)
print("\n".join(results))
