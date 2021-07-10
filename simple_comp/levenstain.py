import numpy as np

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    # print(matrix)
    return matrix[size_x - 1, size_y - 1]


if __name__ == '__main__':
    f1 = open("../examples/file1.py", 'r')
    f2 = open("../examples/file2.py", 'r')
    data1 = list(filter(lambda x: len(x) > 0, f1.readlines()))
    data2 = list(filter(lambda x: len(x) > 0, f2.readlines()))

    same = {}
    for line1 in data1:
        line1 = line1.strip()
        for line2 in data2:
            line2 = line2.strip()
            dist = levenshtein(line1, line2)
            # print(line1, line2, dist)
            if dist < max(len(line1), len(line2)) // 2:
                same[dist] = same.get(dist, []) + [(line1, line2)]

    for k, v in same.items():
        print(k, ": ")
        for pair in v:
            print('\t', pair[0], '&&', pair[1])
