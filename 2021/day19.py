import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import product


def parse_input(file_path):
    with open(file_path, 'r') as f:
        chunks = f.read().split('\n\n')
    reports = [
        np.array(
            [np.fromstring(r, sep=',') for r in c.splitlines()[1:]], dtype=int
        ) for c in chunks
    ]
    return reports


class Scanner:
    def __init__(self, report):
        self.report = report
        self.affine_trans = None

    def calc_overlap(self, other):
        """Finds indices of overlap beacons. """ 
        dists0 = squareform(pdist(self.report, 'sqeuclidean').astype(int))
        dists1 = squareform(pdist(other.report, 'sqeuclidean').astype(int))
        overlap = []
        for i in range(len(dists0)):
            for j in range(len(dists1)):
                d0 = dists0[i, :]
                d1 = dists1[j, :]
                if len(set(dists0[i, :]) & set(dists1[j, :])) >= 12:
                    overlap.append([i, j])
        return np.array(overlap)

    def calc_affine_trans(self, other):
        ov = self.calc_overlap(other)
        X = self.report[ov[:, 0]]
        Y = other.report[ov[:, 1]]
        X = np.row_stack((X, np.ones(3, dtype=int)))
        print(X.shape, Y.shape)
        M = np.linalg.solve(X, Y)
        return M


if __name__ == '__main__':
    reports = parse_input('./test.txt')

    s0 = Scanner(reports[0])
    s1 = Scanner(reports[1])

    # ov = s0.find_overlap(s1)
    # print(s0.report[ov[:, 0]])
    # print(s1.report[ov[:, 1]])
    print(s0.calc_affine_trans(s1))
