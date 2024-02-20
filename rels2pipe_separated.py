import os
import sys
import csv

sec = [
        'Temporal.Asynchronous',
        'Temporal.Synchrony',
        'Contingency.Cause',
        'Contingency.Pragmatic cause',
        'Comparison.Contrast',
        'Comparison.Concession',
        'Expansion.Conjunction',
        'Expansion.Instantiation',
        'Expansion.Restatement',
        'Expansion.Alternative',
        'Expansion.List'
        ]
top = [
        'Temporal',
        'Contingency',
        'Comparison',
        'Expansion'
        ]

def process(folder, outfolder):

    for f in os.listdir(folder):
        af = os.path.join(folder, f)
        if af.endswith('_train.rels'):
            outlines = convert(af)
            train_out = open(os.path.join(outfolder, 'train.txt'), 'w', encoding='utf8')
            for line in outlines:
                train_out.write(line + '\n')
                
        elif af.endswith('_dev.rels'):
            outlines = convert(af)
            dev_out = open(os.path.join(outfolder, 'dev.txt'), 'w', encoding='utf8')
            for line in outlines:
                dev_out.write(line + '\n')
         
        elif af.endswith('_test.rels'):
            outlines = convert(af)
            test_out = open(os.path.join(outfolder, 'test.txt'), 'w', encoding='utf8')
            for line in outlines:
                test_out.write(line + '\n')
           
def convert(relfile):
            
    rows = csv.DictReader(open(relfile), delimiter='\t')
    outlines = []
    for row in rows:
        sense = row['label']
        if sense:
            toplevel = sense.split('.')[0]
            seclevel = '.'.join(sense.split('.')[:2])
            sense_list = [toplevel, seclevel, 'and']
            arg1 = row['unit1_txt']
            arg2 = row['unit2_txt']
            if row['dir'] == '1>2':
                arg1 = row['unit2_txt']
                arg2 = row['unit1_txt']
            outline = ' ||| '.join([str(sense_list), str([None, None, None]), arg1, arg2])
            if toplevel in top and seclevel in sec:
                outlines.append(outline)
    
    return outlines
        

def main():
    if len(sys.argv) < 3:
        print('Usage: python %s <input_folder_with_disrpt_rels_files> <output_folder>' % sys.argv[0])
        sys.exit()
    folder = sys.argv[1] # folder with disrpt data, e.g. https://github.com/disrpt/sharedtask2023/tree/main/data/ita.pdtb.luna
    outfolder = sys.argv[2]
    process(folder, outfolder)
    

if __name__ == '__main__':
    main()