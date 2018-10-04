import pickle as pickle
from pathlib import Path
from subprocess import check_output

phonetisaurus_bin = Path('/home/guest/apps/kaldi/tools/phonetisaurus-g2p/phonetisaurus-g2pfst')
model_fst = Path('model.fst')
transcriber_cache_name = Path('transcriber_cache.pkl')


class Transcriber:
    def __init__(self):
        self.cache = {}
        self.changed = False

        if transcriber_cache_name.exists():
            self.load(transcriber_cache_name)

    def transcribe(self, word):
        if word in self.cache:
            return self.cache[word]

        self.changed = True

        trans = []
        with open('/dev/null') as n:
            out = check_output(
                [f'{phonetisaurus_bin.absolute()}', f'--model={model_fst.absolute()}', '--nbest=100', '--beam=500',
                 '--thresh=10', '--pmass=0.8', f'--word={word}'], stderr=n)
        out = out.decode('utf-8').strip()
        for t in out.split('\n'):
            tok = t.split('\t')
            if len(tok) < 3:
                continue
            t = tok[2]
            trans.append(t.split(' '))

        self.cache[word] = trans
        return trans

    def load(self, path):
        with open(str(path), 'rb') as f:
            self.cache = pickle.load(f)

    def save(self, path=transcriber_cache_name):
        if self.changed:
            self.changed = False
            with open(path, 'wb') as f:
                pickle.dump(self.cache, f, protocol=pickle.HIGHEST_PROTOCOL)


# Unit test
if __name__ == '__main__':
    trans = Transcriber()
    print(trans.transcribe('auto'))
    print(trans.transcribe('brzmienie'))
