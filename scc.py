#!/usr/bin/env python3

import argparse

import pandas as pd

class Graph:
    def __init__(self, in_path=None):
        self.G = {}
        if in_path is not None:
            self.construct_graph(in_path)

        # SCC variables
        self.disc = {}
        self.min_disc = {}
        self.stack = []
        self.sccs = []
        self.step = 0

    def __str__(self):
        return '\n'.join([f'{i}\t{",".join(scc)}' for i, scc in enumerate(self.sccs)])

    # Parse xlsx file into adjacency lists
    def construct_graph(self, in_path):
        df = pd.read_excel(in_path, index_col=0)
        for r in df.iterrows():
            adj = r[1].connected_to_revised
            self.G[r[0]] = [fix_t_id(t.strip()) for t in adj.split(',')] \
                                                    if not pd.isna(adj) else []

    def _scc_inner(self, t):
        self.disc[t] = self.step
        self.min_disc[t] = self.step
        self.step += 1
        self.stack.append(t)

        for tt in self.G[t]:
            try:
                # If we haven't discovered tt yet, we take a recursive step
                if self.disc[tt] == -1:
                    self._scc_inner(tt)
                    self.min_disc[t] = min(self.min_disc[t], self.min_disc[tt])

                elif tt in self.stack:
                    self.min_disc[t] = min(self.min_disc[t], self.min_disc[tt])
            except KeyError as e:
                print(f'Node {e} not present in graph')

        tt = ''
        if self.min_disc[t] == self.disc[t]:
            idx = len(self.sccs)
            self.sccs.append([])
            while t != tt:
                tt = self.stack.pop()
                self.sccs[idx].append(tt)

    # DFS baby
    def scc(self):
        self.disc = {t: -1 for t in self.G}
        self.min_disc = {t: -1 for t in self.G}
        self.stack = []
        self.step = 0

        for t in self.G:
            if self.disc[t] == -1:
                self._scc_inner(t)

    # Writes all SCCs of size greater than cap to path
    def write_sccs(self, path, cap=0):
        with open(path, 'w') as fh:
            scc_id = 0
            for scc in self.sccs:
                if len(scc) > cap:
                    fh.write('\n'.join(f'{t}\t{scc_id}' for t in scc))
                    fh.write('\n')
                    scc_id += 1


def fix_t_id(t_id):
    if t_id[1] == ' ':
        t_id = t_id[1:]
    if t_id[0] != 'T':
        t_id = 'T' + t_id
    return t_id

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect cycles and cliques.')
    parser.add_argument('-i', type=str, dest='in_path', help='path to input file.')
    parser.add_argument('-o', type=str, dest='out_path', help='path to output file.')
    args = parser.parse_args()

    '''
    # Test data
    G = Graph()
    G.G = {
        'T100': ['T101', 'T102'],
        'T101': ['T100', 'T102'],
        'T102': ['T103']
    }
    '''
    G = Graph(args.in_path)
    G.scc()
    G.write_sccs(args.out_path, cap=1)


