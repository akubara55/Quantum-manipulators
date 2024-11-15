from time import time
import numpy as np
import pyqiopt as pq


def get_n(fname: str) -> np.ndarray:
    return np.loadtxt(fname=fname, delimiter=',', dtype=np.int16).T


def gen_qubo() -> np.ndarray:
    p1 = 100
    p2 = 100
    p3 = 100
    p4 = 100000
    p5 = 100
    d = np.loadtxt(fname=r'task-2-nodes.csv', encoding='utf8', delimiter=',', usecols=1, dtype=np.int16)
    adjacency = np.loadtxt(fname=r'task-2-adjacency_matrix.csv', encoding='utf8', dtype=str, delimiter=',', skiprows=1, usecols=np.arange(1, 58))
    adj = np.where(adjacency == '-', 1000, adjacency)
    adj = np.array(adj, dtype=np.float64)
    n = get_n(fname=r'n.txt')
    q = np.einsum('ab,ij,kl->aikbjl', adj, np.identity(15), np.identity(15))
    # print(q[0].shape)
    for i_1 in np.arange(57):
        for i_2 in np.arange(57):
            if i_1 != i_2:
                for j in np.arange(15):
                    for k in np.arange(15):
                        q[i_1, j, k, i_2, j, k] += p2
            else:
                for j_1 in np.arange(15):
                    for j_2 in np.arange(15):
                        if j_1 != j_2:
                            for k in np.arange(15):
                                q[i_1, j_1, k, i_2, j_2, k] += p1
                        else:
                            for k in np.arange(15):
                                p = 1
                                for m in np.arange(5):
                                    p *= n[m, j_1] - d[i_1]
                                q[i_1, j_1, k, i_2, j_2, k] += p3 * p ** 2
    for i in np.arange(57):
        for j_1 in np.arange(15):
            for j_2 in np.arange(15):
                for k_1 in np.arange(15):
                    for k_2 in np.arange(15):
                        q[i, j_1, k_1, i, j_2, k_2] += p5
    for j in np.arange(15):
        for i in np.arange(57):
            for k in np.arange(15):
                q[i, j, k, i, j, k] += p4 * d[i]
        q[j] = q[j] @ q[j]
    for j in np.arange(15):
        for i in np.arange(57):
            for k in np.arange(15):
                for m in np.arange(5):
                    q[i, j, k, i, j, k] -= p4 * 2 * d[i] * n[m, j]
    # np.savetxt(fname=r'qubo.txt', X=q.reshape((57 * 15 * 15, 57 * 15 * 15)))
    # arr = sparse_matrix.todense()
    # arr = (arr + arr.T) / 2
    nz = np.count_nonzero(q)
    return q.reshape((57 * 15 * 15, 57 * 15 * 15))


def main():
    qubo = gen_qubo()
    t_start = time()
    sol = pq.solve(qubo, number_of_runs=1, number_of_steps=100, return_samples=False, verbose=10)
    np.savetxt(fname='vector.txt', X=sol.vector)
    # np.savetxt(fname='objective.txt', X=sol.objective)
    print('Script time: ', time() - t_start)


if __name__ == '__main__':
    main()
