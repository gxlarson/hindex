from math import sqrt

def h_index(in_list):
    h = 0
    if len(in_list) < 1:
        return h
    for i, count in enumerate(sorted(in_list, reverse=True)):
        if count > i:
            h += 1
        else:
            break
    return h

def normalized_h_index(in_list, scale):
    h = h_index(in_list)
    return h / float(scale)

def i10_index(in_list):
    score = 0
    for count in in_list:
        if count >= 10:
            score += 1
    return score

def o_index(in_list):
    m = max(in_list)
    h = h_index(in_list)
    return sqrt(m*h)

def g_index(in_list):
    # number g elements with at least cumulative g^2
    g = 0
    if len(in_list) < 1:
        return g
    tally = 0
    for i, count in enumerate(sorted(in_list, reverse=True)):
        if (tally + count) >= (g+1)**2:
            tally += count
            g += 1
        else:
            break
    return g

def w_index(in_list):
    w = 0
    if len(in_list) < 1:
        return w
    for i, count in enumerate(sorted(in_list, reverse=True)):
        _w = w + 1
        f = 10 * _w
        if count >= f:
            w += 1
        else:
            break
    return w

def e_index(in_list):
    h = h_index(in_list)
    e_sq = 0
    for i, count in enumerate(sorted(in_list, reverse=True))[:h]:
        e_sq += (count - h)
    e = sqrt(e_sq)
    return e