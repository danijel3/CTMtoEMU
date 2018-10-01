import codecs
import re
from collections import OrderedDict

import ID

pl_sampa_map = {'ni': "n'", 'si': "s'", 'tsi': "ts'", 'zi': "z'", 'dzi': "dz'", 'en': 'e~', 'on': 'o~'}
pl_ipa_map = {'e': u'ɛ', 'en': u'ɛ̃', 'I': u'ɨ', 'o': u'ɔ', 'on': u'ɔ̃', 'si': u'ɕ', 'dz': u'dz', 'dzi': u'dʑ',
              'dZ': u'dʐ', 'g': u'ɡ', 'ni': u'ɲ', 'S': u'ʂ', 'tsi': u'tɕ', 'ts': u'ts', 'tS': u'tʂ', 'zi': u'ʑ',
              'Z': u'ʐ'}

EPSILON = 5e-3
besi = re.compile('^.*_[BESI]$')


class Segment:
    def __init__(self, line=''):

        if len(line) == 0:
            self.id = ID.next()
            self.file = ''
            self.channel = ''
            self.start = 0
            self.dur = 0
            self.end = 0
            self.text = ''
            return

        tok = re.split('\\s+', line)

        if len(tok) < 5:
            raise RuntimeError(f'Expected line to have at least 5 tokens (found {len(tok)})')

        self.id = ID.next()
        self.file = tok[0]
        self.channel = tok[1]
        self.start = float(tok[2])
        self.dur = float(tok[3])
        self.end = self.start + self.dur
        self.text = tok[4]

    def wraps(self, other):
        return other.start - self.start > -EPSILON and other.end - self.end < EPSILON


class File:
    def __init__(self, name):
        self.name = name
        self.segments = []

    def getAnnotation(self, name, labelname, samplerate=16000, get_segments=True, phonemes=False):

        level = OrderedDict()

        level['name'] = name
        if get_segments:
            level['type'] = 'SEGMENT'
        else:
            level['type'] = 'ITEM'

        items = []
        level['items'] = items

        for seg in self.segments:
            item = OrderedDict()
            items.append(item)

            item['id'] = seg.id

            if get_segments:
                item['sampleStart'] = int(samplerate * seg.start)
                item['sampleDur'] = int(samplerate * seg.dur)

            labels = []
            item['labels'] = labels

            label = OrderedDict()
            labels.append(label)

            label['name'] = labelname
            text = seg.text
            if phonemes:
                if besi.match(text):
                    text = text[:-2]

                label_ph = OrderedDict()
                labels.append(label_ph)
                label_ph['name'] = 'SAMPA'
                ph = text
                if ph in pl_sampa_map:
                    ph = pl_sampa_map[ph]
                label_ph['value'] = ph

                label_ph = OrderedDict()
                labels.append(label_ph)
                label_ph['name'] = 'IPA'
                ph = text
                if ph in pl_ipa_map:
                    ph = pl_ipa_map[ph]
                label_ph['value'] = ph

            label['value'] = text



        return level

    def getLinks(self, other_ctm):

        links = []

        for seg in self.segments:
            for other_seg in other_ctm.segments:
                if seg.file == other_seg.file and seg.wraps(other_seg):
                    link = OrderedDict()
                    links.append(link)
                    link['fromID'] = seg.id
                    link['toID'] = other_seg.id

        return links

    def getUttFile(self):
        ctm = File(self.name)
        min = max = 0

        for seg in self.segments:
            if min > seg.start:
                min = seg.start
            if max < seg.end:
                max = seg.end

        seg = Segment()

        seg.start = min
        seg.end = max
        seg.dur = max - min
        seg.text = self.name

        seg.file = self.name
        seg.channel = self.segments[0].channel

        ctm.segments.append(seg)
        return ctm


class CTM:
    def __init__(self):
        self.files = {}

    def load(self, file):
        with codecs.open(str(file), encoding='utf-8') as f:
            for num, line in enumerate(f):
                try:
                    seg = Segment(line.strip())
                except Exception as err:
                    raise RuntimeError(err, f'Error in {file}:{num} >{line.strip()}<')
                if not seg.file in self.files:
                    self.files[seg.file] = File(seg.file)
                self.files[seg.file].segments.append(seg)

        for name, file in self.files.items():
            file.segments = sorted(file.segments, key=lambda seg: seg.start)
