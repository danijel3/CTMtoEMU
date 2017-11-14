import os
import pickle as pickle
from subprocess import Popen, PIPE

transcriber_path = '/home/guest/apps/transcriber'
transcriber_cache_name = 'transcriber_cache.pkl'


# WARNING: this class doesn't use replacement rules!
class Transcriber:
    def __init__(self):
        self.cache = {}
        self.changed = False

        if os.path.exists(transcriber_cache_name):
            self.load(transcriber_cache_name)

    def transcribe(self, word):
        if word in self.cache:
            return self.cache[word]

        self.changed = True

        trans = []
        with open(os.devnull, 'w') as n:
            p = Popen([transcriber_path + '/transcriber', '-r', transcriber_path + '/transcription.rules'],
                      stdin=PIPE, stdout=PIPE, stderr=n)
            p.stdin.write(word.encode('utf-8') + '\n')
            p.stdin.close()
            for t in p.stdout:
                trans.append(t[:-1].split(' ')[1:])

            self.cache[word] = trans
        return trans

    def load(self, path):
        with open(path) as f:
            self.cache = pickle.load(f)

    def save(self, path=transcriber_cache_name):
        if self.changed:
            self.changed = False
            with open(path, 'w') as f:
                pickle.dump(self.cache, f, protocol=pickle.HIGHEST_PROTOCOL)
