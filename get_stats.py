import os
import ast
import pandas
from collections import defaultdict
import matplotlib.pyplot as plt


def get_dataset_stats(data_folder):
    train = os.path.join(data_folder, 'train.txt')
    dev = os.path.join(data_folder, 'dev.txt')
    test = os.path.join(data_folder, 'test.txt')

    top = defaultdict(int)
    second = defaultdict(int)
    top, second = read_file(train, top, second)
    top, second = read_file(dev, top, second)
    top, second = read_file(test, top, second)
    total = sum(top.values())
    top = {k: v / total for k, v in top.items()}
    second = {k: v / total for k, v in second.items()}

    return top, second


def read_file(fname, top, second):

    for row in open(fname).readlines():
        items = row.split('|||')
        fs = items[0].strip()
        sl = ast.literal_eval(fs)
        top[sl[0]] += 1
        second[sl[1]] += 1

    return top, second


def main():
    luna_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\ita.pdtb.luna\data'
    luna_top, luna_second = get_dataset_stats(luna_folder)
    crpc_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\por.pdtb.crpc\data'
    crpc_top, crpc_second = get_dataset_stats(crpc_folder)
    tdb_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\tur.pdtb.tdb\data'
    tdb_top, tdb_second = get_dataset_stats(tdb_folder)
    pdtb_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\PDTB\Ji\data'
    pdtb_top, pdtb_second = get_dataset_stats(pdtb_folder)

    """
    top_df = pandas.DataFrame([luna_top, crpc_top, tdb_top, pdtb_top])
    top_df['corpora'] = ['luna', 'crpc', 'tdb', 'pdtb']
    top_df = top_df.set_index('corpora')
    plt.style.use('fivethirtyeight')
    top_df.plot(kind="bar", figsize=(7, 6), alpha=0.8, xlabel="Corpus", ylabel="sense distribution", grid=True)
    plt.show()
    """

    second_df = pandas.DataFrame([luna_second, crpc_second, tdb_second, pdtb_second])
    second_df['corpora'] = ['luna', 'crpc', 'tdb', 'pdtb']
    second_df = second_df.set_index('corpora')
    second_df.plot(kind="bar", alpha=0.8, xlabel="Corpus", ylabel="sense distribution") # figsize=(7, 6) , grid=True
    #plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.show()


    print()




if __name__ == '__main__':
    main()
