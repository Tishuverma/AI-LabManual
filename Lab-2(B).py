import heapq
import re
import itertools  # Used for tie-breaking counter

def tokenize_sentences(text):
    sentences = re.split(r'[.!?]\s*', text.strip())
    return [s.lower().strip() for s in sentences if s.strip()]

def levenshtein(s1, s2):
    len1, len2 = len(s1), len(s2)
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,
                           dp[i][j - 1] + 1,
                           dp[i - 1][j - 1] + cost)
    return dp[len1][len2]

def a_star_alignment(doc1, doc2):
    sents1 = tokenize_sentences(doc1)
    sents2 = tokenize_sentences(doc2)
    n1, n2 = len(sents1), len(sents2)

    heap = []
    counter = itertools.count()  # tie-breaker counter
    start = (0, 0)
    heapq.heappush(heap, (0, next(counter), start, []))  # (f_cost, count, state, path)
    visited = set()

    def heuristic(i, j):
        return abs((n1 - i) - (n2 - j))

    while heap:
        f_cost, _, (i, j), path = heapq.heappop(heap)

        if (i, j) in visited:
            continue
        visited.add((i, j))

        if i == n1 and j == n2:
            return path

        # Align sentences
        if i < n1 and j < n2:
            ed = levenshtein(sents1[i], sents2[j])
            g_cost = f_cost - heuristic(i, j) + ed
            f_new = g_cost + heuristic(i + 1, j + 1)
            heapq.heappush(heap, (f_new, next(counter), (i + 1, j + 1), path + [((i, j), ed)]))

        # Skip sentence in doc1
        if i < n1:
            g_cost = f_cost - heuristic(i, j) + 1
            f_new = g_cost + heuristic(i + 1, j)
            heapq.heappush(heap, (f_new, next(counter), (i + 1, j), path + [((i, None), 1)]))

        # Skip sentence in doc2
        if j < n2:
            g_cost = f_cost - heuristic(i, j) + 1
            f_new = g_cost + heuristic(i, j + 1)
            heapq.heappush(heap, (f_new, next(counter), (i, j + 1), path + [((None, j), 1)]))

    return None

def detect_plagiarism(alignment, doc1, doc2, threshold=2):
    sents1 = tokenize_sentences(doc1)
    sents2 = tokenize_sentences(doc2)
    plagiarised_pairs = []
    for ((i, j), dist) in alignment:
        if i is not None and j is not None and dist <= threshold:
            plagiarised_pairs.append((sents1[i], sents2[j], dist))
    return plagiarised_pairs

if _name_ == "_main_":
    docA = "Artificial intelligence is fascinating. It is a growing field. Many applications utilize AI."
    docB = "Artificial intelligence is fascinating. AI is rapidly advancing. Applications use AI in many ways."

    alignment = a_star_alignment(docA, docB)

    if alignment:
        plag = detect_plagiarism(alignment, docA, docB)
        print("Potential plagiarism found in sentence pairs:")
        for s1, s2, dist in plag:
            print(f'"{s1}" <-> "{s2}" (Edit Distance: {dist})')
    else:
        print("No alignment found.")
