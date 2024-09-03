import os
import sys
import ast
import argparse
from sklearn import metrics

def get_goldlabels(gold, level):
    labels = []
    for line in open(gold):
        p = [x.strip() for x in line.split('|||')]
        fg = ast.literal_eval(p[0])
        if level == 'top':
            labels.append(fg[0])
        elif level == 'sec':
            labels.append(fg[1])
    return labels

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gold')
    parser.add_argument('-p', '--pred')
    parser.add_argument('-l', '--level')
    args = parser.parse_args()
    if not args.gold or not args.pred or not args.level:
        sys.stderr.write('Please specify all args.\n')
        sys.exit()
    assert args.level in ['top', 'sec']
    
    gold = get_goldlabels(args.gold, args.level)
    pred = [x.strip() for x in open(args.pred).readlines()]

    assert len(gold) == len(pred)
    acc = metrics.accuracy_score(gold, pred)
    f1 = metrics.f1_score(gold, pred, average='macro')
    print('accuracy:', acc)
    print('macro f1:', f1)
        

if __name__ == '__main__':
    main()
    
