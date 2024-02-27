import argparse
import deepl
import sys
import os
import requests
from googletrans import Translator
from tqdm import tqdm
# export DEEPL_API_KEY=<your-deepl-key...>
DEEPL_AUTH_KEY = os.environ.get('DEEPL_API_KEY')

class DeepLTranslator:
    def __init__(self):
        self.translator = deepl.Translator(DEEPL_AUTH_KEY)
                                
    def translate(self, inp, trg):
        try:
            return self.translator.translate_text(inp, target_lang=trg).text
        except Exception as e:
            sys.stderr.write("ERROR: Failed to translate '%s': %s" % (inp, str(e)))


class GoogleTranslator:
    def __init__(self):
        self.translator = Translator()

    def translate(self, inp, trg):
        try:
            return self.translator.translate(inp, dest=trg).text
        except Exception as e:
            sys.stderr.write("ERROR: Failed to translate '%s': %s" % (inp, str(e)))

def process_file(trans, lang, outdir, af, fname):
    
    outf = open(os.path.join(outdir, fname), 'w')
    for line in tqdm(open(af).readlines(), desc='translating %s' % fname):
        p = [x.strip() for x in line.split('|||')]
        assert len(p) == 4
        arg1 = p[2]
        arg2 = p[3]
        trans_arg1 = trans.translate(arg1, lang)
        trans_arg2 = trans.translate(arg2, lang)
        if isinstance(trans_arg1, str) and isinstance(trans_arg2, str):
            outf.write(' ||| '.join([p[0], p[1], trans_arg1, trans_arg2]) + '\n')
        

def translate(data, lang):

    #trans = DeepLTranslator()
    trans = GoogleTranslator()

    outdir = os.path.join(os.getcwd(), 'pdtb_%s' % lang, 'data')
    if not os.path.exists(os.path.dirname(outdir)):
        os.mkdir(os.path.dirname(outdir))
    if not os.path.exists(outdir):
        os.mkdir(outdir)
        
    for f in os.listdir(data):
        af = os.path.join(data, f)
        if af.endswith('train.txt'):
            process_file(trans, lang, outdir, af, 'train.txt')
        elif af.endswith('test.txt'):
            process_file(trans, lang, outdir, af, 'test.txt')
        elif af.endswith('dev.txt'):
            process_file(trans, lang, outdir, af, 'dev.txt')
            
        
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", required=True)
    parser.add_argument("-l", "--lang", required=True)
    args = parser.parse_args()
    if not args.data or not args.lang:
        parser.print_help()

    translate(args.data, args.lang)



if __name__ == '__main__':
    main()
    