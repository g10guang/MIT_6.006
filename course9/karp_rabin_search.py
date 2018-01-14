#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2018-01-14 17:13
# 使用 karp-rabin 字符串匹配算法
# 算法思路：
# 使用 rolling hash ADT 从而可以 O(1) 地从 hash(txt[s:s+m-1]) 和 txt[s+m] 计算出 hash(txt[s+1...s+m])
# hash(txt[s+1:s+m]) = (d * (hash(txt[s:s+m-1]) - ord(txt[s]) * h) + ord(txt[s+m])) mod q
# d: 字母表中所有字母的数量，256 in ascii / 2**16 in unicode
# q: 一个素数
# h: d^(m-1)
# m: len(pat)
# n: len(txt)


def karp_rabin_search(txt, pat, q):
    """
    karp-rabin 字符串模式匹配算法
    这里最重要的是 roll-hash 数据结构
    这里当成是 unicode d = 2 ** 16
    :param txt:
    :param pat: 模式
    :param q: 一个素数
    :return: 能够匹配上的下标 tuple
    """
    d = 2 ** 16
    len_txt = len(txt)
    len_pat = len(pat)
    hash_pat = 0
    hash_txt = 0
    h = 1
    for i in range(len_pat - 1):
        h = (h * d) % q
    # 记录成功匹配的下标，用于最后返回
    match_indexes = []

    # 计算初始 hash
    # hash(pat)
    # hash(txt[:len_pat])
    for i in range(len_pat):
        hash_pat = (d * hash_pat + ord(pat[i])) % q
        hash_txt = (d * hash_txt + ord(txt[i])) % q

    for x in range(len_txt - len_pat + 1):
        s = x + len_pat
        if hash_pat == hash_txt:
            # 防止 hash 冲突，一个一个判断是否真的匹配成功
            if all(pat[i] == txt[x + i] for i in range(len_pat)):
                print('成功匹配：{}'.format(x))
                match_indexes.append(x)
        # 计算 hash(txt[x+len(x)])
        if x < len_txt - len_pat:
            hash_txt = (d * (hash_txt - ord(txt[x]) * h) + ord(txt[s])) % q
            # 如果保证 q > 0，hash_txt 不会出现 < 0
            if hash_txt < 0:
                hash_txt += q
    return match_indexes


def search(txt, pat, q):
    d = 2 ** 16

    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0  # hash value for pattern
    t = 0  # hash value for txt
    h = 1

    # The value of h would be "pow(d, M-1)%q"
    for i in range(M - 1):
        h = (h * d) % q

    # Calculate the hash value of pattern and first window
    # of text
    for i in range(M):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q

    # Slide the pattern over text one by one
    for i in range(N - M + 1):
        # Check the hash values of current window of text and
        # pattern if the hash values match then only check
        # for characters on by one
        if p == t:
            # Check for characters one by one
            for j in range(M):
                if txt[i + j] != pat[j]:
                    break

            j += 1
            # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
            if j == M:
                print("Pattern found at index " + str(i))

        # Calculate hash value for next window of text: Remove
        # leading digit, add trailing digit
        if i < N - M:
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q

            # We might get negative values of t, converting it to
            # positive
            if t < 0:
                t = t + q


if __name__ == '__main__':
    karp_rabin_search('hello world hello karp hell ? heeehehehehe', 'he', 1009)
    # search('hello world hello karp', 'he', 1009)
