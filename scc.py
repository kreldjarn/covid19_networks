#!/usr/bin/env python3

import argparse

import pandas as pd

def construct_graph(in_path):
    G = {}

    df = pd.read_excel(in_path, index_col=0)
    for r in df.iterrows():
        adj = r[1].connected_to_revised
        G[r[0]] = [t.strip() for t in adj.split(',')] if not pd.isna(adj) else []

    return G

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect cycles and cliques.')
    parser.add_argument('-i', type=str, dest='in_path', help='path to input file.')
    parser.add_argument('-o', type=str, dest='out_path', help='path to output file.')
    args = parser.parse_args()

    G = construct_graph(args.in_path)
    print(G)

