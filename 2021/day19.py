import numpy as np
from scipy.spatial.distance import pdist


def parse_input(file_path):
    with open(file_path, 'r') as f:
        chunks = f.read().split('\n\n')
    reports = [[np.fromstring(r, sep=',') for r in c.splitlines()[1:]] for c in chunks]
    return np.array(reports, dtype=int)


if __name__ == '__main__':
    reports = parse_input('./test.txt')

    rep = reports[0]
    dists = pdist(rep, 'sqeuclidean')
    print(dists)
