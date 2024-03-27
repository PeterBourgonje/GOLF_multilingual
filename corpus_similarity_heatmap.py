import os
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from scipy import spatial
import numpy
import pandas
import seaborn

model = SentenceTransformer('sentence-transformers/stsb-xlm-r-multilingual')
arg2embs = {}


def get_all_args(folder):

    train = os.path.join(folder, 'train.txt')
    dev = os.path.join(folder, 'dev.txt')
    test = os.path.join(folder, 'test.txt')
    args = get_args(train)
    args += get_args(dev)
    args += get_args(test)
    return args


def get_args(fname):
    args = []
    #for line in open(fname).readlines()[:3]:  # TODO: DEBUG ONLY!!!
    for line in open(fname).readlines():
        items = line.split('|||')
        assert len(items) == 4
        args.append(items[2].strip())
        args.append(items[3].strip())
    return args


def get_avg_sim(corp1, corp2):

    global arg2embs
    for arg in tqdm(corp1 + corp2, desc='Getting embeddings'):
        if arg not in arg2embs:
            embeddings = model.encode(arg)
            arg2embs[arg] = embeddings
    sims = []
    for arg_i in tqdm(corp1, desc='Getting cosims'):
        for arg_j in corp2:
            emb_i = arg2embs[arg_i]
            emb_j = arg2embs[arg_j]
            sim = 1 - spatial.distance.cosine(emb_i, emb_j)
            sims.append(sim)
    return numpy.mean(sims)


def main():
    luna_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\ita.pdtb.luna\data'
    luna_args = get_all_args(luna_folder)
    crpc_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\por.pdtb.crpc\data'
    crpc_args = get_all_args(crpc_folder)
    tdb_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\tur.pdtb.tdb\data'
    tdb_args = get_all_args(tdb_folder)
    pdtb_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\PDTB\Ji\data'
    pdtb_args = get_all_args(pdtb_folder)
    pdtb_it_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\pdtb_it\data'
    pdtb_it_args = get_all_args(pdtb_it_folder)
    pdtb_pt_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\pdtb_pt\data'
    pdtb_pt_args = get_all_args(pdtb_pt_folder)
    pdtb_tr_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\pdtb_tr\data'
    pdtb_tr_args = get_all_args(pdtb_tr_folder)

    all_corpora = {'luna': luna_args, 'crpc': crpc_args, 'tdb': tdb_args, 'pdtb': pdtb_args,
                   'pdtb_it': pdtb_it_args, 'pdtb_pt': pdtb_pt_args, 'pdtb_tr': pdtb_tr_args}

    matrix = []
    for c1 in all_corpora:
        row = []
        for c2 in all_corpora:
            row.append(get_avg_sim(all_corpora[c1], all_corpora[c2]))
        matrix.append(row)
    df = pandas.DataFrame(matrix, columns=['luna', 'crpc', 'tdb', 'pdtb', 'pdtb-it', 'pdtb-pt', 'pdtb-tr'],
                          index=['luna', 'crpc', 'tdb', 'pdtb', 'pdtb-it', 'pdtb-pt', 'pdtb-tr'])
    df.to_csv('corpus_similarity_df.csv', sep=',')
    hm = seaborn.heatmap(df, annot=True, cmap='YlOrBr')
    fig = hm.get_figure()
    fig.savefig("corpus_similarity_heatmap.png")


if __name__ == '__main__':
    main()

