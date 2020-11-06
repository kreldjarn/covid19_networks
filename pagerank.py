#!/usr/bin/env python3

import argparse

from scipy.sparse import csc_matrix as m
import numpy as np

def pagerank(G, d=.85, tol=1e-6, max_iter=10000, rev=False):
    if rev:
        G = G.T

    n, _ = G.shape

    print('Creating L1-normalized representation of G')
    M = G.copy()
    sums = np.sum(M, axis=1)
    M = np.nan_to_num(M / sums[:,None])

    sink_states = sums==0

    rank = np.ones(n)
    rank_prev = np.zeros(n)

    N = 1
    print('Starting PageRank')
    while np.sum(np.abs(rank-rank_prev)) > tol and N < max_iter:
        rank_prev = rank.copy()
        if N % 25 == 0:
            print(f'Iteration {N}')

        # Update ranks
        for i in range(n):
            # Find incoming edges
            E_in = M[:,i].astype(np.float)

            # Account for edges
            S = sink_states / n

            # Account for restart
            R = np.ones(n) / n

            # Weighted PageRank step
            rank[i] = rank_prev.dot((E_in + S)*d + R*(1-d)*G[i])
        N += 1

    if N < max_iter:
        print(f'Converged in {N} iterations')

    return rank/sum(rank)

def parse_dat_edges(path):
    print(f'Reading edges from {path}')
    to, frm, wt = [], [], []
    with open(path, 'r') as fh:
        # Skip header
        fh.readline()
        for line in fh:
            t, f, _, _, w = line.split()
            to.append(t)
            frm.append(f)
            wt.append(float(w.rstrip('\n')))

    nodes = list(set(to).union(set(frm)))
    nodes_map = {n: i for i, n in enumerate(nodes)}

    print(f'Parsing edges into adjacency list')
    G = np.zeros((len(nodes), len(nodes)))
    for t, f, w in zip(to, frm, wt):
        G[nodes_map[t],nodes_map[f]] = w

    return G, nodes, nodes_map

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the PageRank of a weighted, directed graph.')
    parser.add_argument('-i', type=str, dest='in_path', help='path to input file.')
    parser.add_argument('-o', type=str, dest='out_path', help='path to output file.')
    args = parser.parse_args()

    '''
    G = np.array([[1,1,0,0,0,0,0],
                  [1,1,0,0,0,0,0],
                  [0,0,1,0,0,0,0],
                  [0,0,0,1,0,0,0],
                  [0,0,0,0,1,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,1,1]])
    '''

    G, nodes, nodes_map = parse_dat_edges(args.in_path)
    ranks = pagerank(G)

    print(f'Writing PageRanks to {args.out_path}')
    with open(args.out_path, 'w') as fh:
        for idx, rank in enumerate(ranks):
            fh.write(f'{nodes[idx]}\t{rank}\n')


