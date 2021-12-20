import numpy as np
import matplotlib.pyplot as plt


def propagate(v, num_steps=10):
    times = np.arange(0, num_steps)
    x = np.zeros((2, len(times)), dtype=int)
    v = np.asarray(v)
    for t in times[:-1]:
        x[0, t + 1] = x[0, t] + max(v[0] - t, 0)
        x[1, t + 1] = x[1, t] + (v[1] - t)
    return times, x


def visualize(v, box, num_steps=7):
    _, x = propagate(v, num_steps)
    print(f'max(y) = {np.max(x[1, :])}')
    fig, ax = plt.subplots()
    ax.plot(x[0, :], x[1, :], ls='none', marker='o')
    ax.plot([box[0, i] for i in [0, 1, 1, 0, 0]], [box[1, j] for j in [0, 0, 1, 1, 0]])
    plt.show()
    return fig, ax

if __name__ == '__main__':
    box = np.array([[20, 30], [-10, -5]])
    v = [6, 9]
    # visualize(v, box, 22)
