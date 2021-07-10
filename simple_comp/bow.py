import re
import numpy as np
import keyword


class BagOfWords:
    KEYWORDS = sorted(keyword.kwlist)
    OPERATORS = sorted(['<', '>', '<=', '>=', '!=', '=='] + \
                       ['+', '-', '*', '/', '%', '**', '//'] + \
                       ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//='] + \
                       ['&', '|', '^', '<<', '>>', '~'] + \
                       ['&=', '|=', '^=', '<<=', '>>='])

    def __init__(self, lines=[], delimeters=' ()[]{}\n\r:,.=\'\"'):
        self.__delimeters = delimeters

        self.vocabular = self.buildVocabular(lines)
        print(self.vocabular)

    def buildVocabular(self, lines):
        words = []
        known = set(BagOfWords.KEYWORDS + BagOfWords.OPERATORS)
        for line in lines:
            for w in self.split(line):
                if w not in known:
                    words.append(w)
                    known.add(w)
        words.remove('')
        return BagOfWords.KEYWORDS + BagOfWords.OPERATORS + words

    def split(self, line):
        regexPattern = '|'.join(map(re.escape, self.__delimeters))
        return re.split(regexPattern, line, 0)

    def vectorize(self, line):
        bag_vector = np.zeros(len(self.vocabular))

        for w in self.split(line):
            for i, word in enumerate(self.vocabular):
                if word == w:
                    bag_vector[i] += 1
        return np.array(bag_vector)


if __name__ == "__main__":
    f1 = open("../examples/file1.py", 'r')
    data1 = list(filter(lambda x: len(x) > 0, f1.readlines()))
    b1 = BagOfWords(data1)

    f2 = open("../examples/file2.py", 'r')
    data2 = list(filter(lambda x: len(x) > 0, f2.readlines()))
    b2 = BagOfWords(data2)

    sqrSize = max(len(data1), len(data2))
    cross = np.ones((sqrSize, sqrSize)) * len(b1.vocabular)
    for i, line1 in enumerate(data1):
        for j, line2 in enumerate(data2):
            vect1 = b1.vectorize(line1)
            vect2 = b2.vectorize(line2)
            vect1 = np.append(vect1, [0] * abs(len(vect2) - len(vect1)))
            vect2 = np.append(vect2, [0] * abs(len(vect2) - len(vect1)))
            norm = np.linalg.norm(vect2 - vect1)
            cross[i, j] = min(cross[i, j], norm)
    print(cross)

    sum = 0
    for i, line1 in enumerate(data1):
        sum += np.min(cross, axis=0)[i]
        print(line1.strip(), np.argmin(cross, axis=0)[i])
    print()
    for i, line2 in enumerate(data2):
        sum += np.min(cross, axis=1)[i]
        print(line2.strip(), np.argmin(cross, axis=1)[i])

    print(sum)
