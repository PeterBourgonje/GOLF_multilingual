import os
import re
import ast
import pandas
from collections import defaultdict
import matplotlib.pyplot as plt

ALL_SECOND_SENSES = ['Comparison.Concession',
                     'Comparison.Contrast',
                     'Contingency.Cause',
                     'Contingency.Pragmatic cause',
                     'Expansion.Alternative',
                     'Expansion.Conjunction',
                     'Expansion.Instantiation',
                     'Expansion.List',
                     'Expansion.Restatement',
                     'Temporal.Asynchronous',
                     'Temporal.Synchrony']


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
    top = {k: v / total for k, v in sorted(top.items(), key=lambda x: x[0])}
    #second = {k: v / total for k, v in sorted(second.items(), key=lambda x: x[0])}
    second = {k: second[k] / total for k in ALL_SECOND_SENSES}

    return top, second


def read_file(fname, top, second):

    for row in open(fname).readlines():
        items = row.split('|||')
        fs = items[0].strip()
        sl = ast.literal_eval(fs)
        sl_0 = sl[0].strip()
        top[sl_0] += 1
        sl_1 = sl[1].strip()
        second[sl_1] += 1

    return top, second


def main():
    luna_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\ita.pdtb.luna\data'
    luna_top, luna_second = get_dataset_stats(luna_folder)
    crpc_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\por.pdtb.crpc\data'
    crpc_top, crpc_second = get_dataset_stats(crpc_folder)
    tdb_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data\tur.pdtb.tdb\data'
    tdb_top, tdb_second = get_dataset_stats(tdb_folder)
    pdtb_folder = r'C:\Users\bourg\Desktop\various\GOLF_multilingual\data-backup\PDTB\Ji\data'
    pdtb_top, pdtb_second = get_dataset_stats(pdtb_folder)

    plt.style.use('ggplot')

    top_df = pandas.DataFrame([luna_top, crpc_top, tdb_top, pdtb_top])
    top_df['corpora'] = ['luna', 'crpc', 'tdb', 'pdtb']
    toplevelcolors = [
        '#15B01A',
        '#000080',
        '#FFA500',
        '#13EAC9'
    ]
    top_df = top_df.set_index('corpora')
    top_df.plot(kind="bar", alpha=0.8, xlabel="Corpus", ylabel="Relative Sense Distribution", figsize=(12, 11), fontsize=24, grid=False, color=toplevelcolors)
    plt.legend(loc=2, prop={'size': 24})
    plt.xlabel('Corpus', fontsize=24)
    plt.ylabel('Relative Sense Distribution', fontsize=24)
    plt.savefig('top-level-sense-distributions.png')
    #plt.show()


    second_df = pandas.DataFrame([luna_second, crpc_second, tdb_second, pdtb_second])
    corpora = ['luna', 'crpc', 'tdb', 'pdtb']
    second_df['corpora'] = corpora
    second_df = second_df.set_index('corpora')
    secondlevelcolors = ['#15B01A',  # this is hardcoded and linked to 11-classes (see ALL_SECOND_SENSES above)
                         '#008000',
                         '#000080',
                         '#01153E',
                         '#FFA500',
                         '#F97306',
                         '#FF4500',
                         '#DC143C',
                         '#8C000F',
                         '#13EAC9',
                         '#04D8B2'

    ]
    second_df.plot(kind="bar", alpha=0.8, xlabel="Corpus", ylabel="Relative Sense Distribution", figsize=(12, 8), fontsize=14, grid=False, width=0.9, color=secondlevelcolors)
    plt.legend(loc="upper right", prop={'size': 12}, framealpha=1)
    [plt.axvline(x + 0.5, color='black', linestyle='dotted') for x in range(len(corpora)-1)]
    plt.xlabel('Corpus', fontsize=14)
    plt.ylabel('Relative Sense Distribution', fontsize=14)

    plt.savefig('second-level-sense-distributions.png')
    #plt.show()


    print()




if __name__ == '__main__':
    main()
