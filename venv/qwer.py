def test(word, word2):
    return len(word) == len(word2) and all(t in word2 for t in word)


n = int(input())
words = []
for _ in range(n):
    word = input().lower()
    if word not in words:
        words.append(word)
words = sorted(words, words.lower())
while len(words) > 0:
    wer = [words.pop(0)]
    k = 0
    while k < len(words):
        word2 = words[k]
        if test(wer[0], word2):
            wer.append(word2)
            words.remove(word2)
        else:
            k += 1
    if len(wer) > 1:
        print(*wer)