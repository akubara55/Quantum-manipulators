from time import time
import numpy as np
import pyqiopt as pq


def gen_qubo():
    beta = 0
    gamma = 10
    s = 1e6
    le = np.int32(10 * 100 + 20)
    le_big = np.round(np.log2(1e6)).astype(np.int16)
    p = np.loadtxt(fname=r'task-1-stocks.csv', encoding='utf8', delimiter=',', skiprows=1, usecols=np.arange(100), dtype=np.float64).T
    n = 100
    m = 10
    # p[j, i]
    qubo = np.zeros((le, le), dtype=np.float64)
    # r_i_0 = (np.roll(a=p[0], shift=-1) - p[0]) / p[0]
    r = np.array([(np.roll(a=p[j], shift=-1) - p[j]) / p[j] for j in np.arange(n)],  dtype=np.float64)
    # sigma_0 = np.sqrt(n * np.sum((r_i_0 - np.sum(r_i_0) / n) ** 2) / (n - 1))
    r_av = np.array([np.sum(r[j]) / n for j in np.arange(n)], dtype=np.float64)
    sigma = np.array([np.sqrt(n * np.sum((r[j] - r_av) ** 2) / (n - 1)) for j in np.arange(n)], dtype=np.float64)
    n_j = s / p[:, 0]
    for j in np.arange(n):
        for k in np.arange(m):
            qubo[j * (m - 1) + k, j * (m - 1) + k] += (-r_av[j] + beta * sigma[j]) * n_j[j] * 2 ** (-int(k) - 1)
    for j_1 in np.arange(n):
        for j_2 in np.arange(n):
            for k_1 in np.arange(m):
                for k_2 in np.arange(m):
                    if j_1 == j_2 and k_1 == k_2:
                        f = gamma * p[j_1, 0] * n_j[j_1] * 2 ** (int(k_1) - 1) * (p[j_1, 0] * n_j[j_1] * 2 ** (int(k_1) - 1) + s)
                    else:
                        f = gamma * p[j_1, 0] * p[j_2, 0] * n_j[j_1] * n_j[j_2] * 2 ** (-int(k_1) - int(k_2) - 2)
                    qubo[j_1 * (m - 1) + k_1, j_2 * (m - 1) + k_2] += f
    for l_1 in np.arange(le_big):
        for l_2 in np.arange(le_big):
            if l_1 == l_2:
                f = gamma * 2 ** l_1 * (4 + 1e6)
            else:
                f = gamma * 2 ** (l_1 + l_2)
            qubo[l_1 + m - 1 + n - 1, l_2 + m - 1 + n - 1] += f
    return qubo


def main():
    qubo = gen_qubo()
    t_start = time()
    sol = pq.solve(qubo, number_of_runs=1, number_of_steps=100, return_samples=False, verbose=10)
    np.savetxt(fname='vector.txt', X=sol.vector)
    # np.savetxt(fname='objective.txt', X=sol.objective)
    print('Script time: ', time() - t_start)


if __name__ == '__main__':
    main()
