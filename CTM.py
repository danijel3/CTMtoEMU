import codecs
import re
from collections import OrderedDict

import ID

EPSILON = 5e-3


class Segment:
    def __init__(self, line=''):

        if len(line) == 0:
            self.id = next(ID)
            self.file = ''
            self.channel = ''
            self.start = 0
            self.dur = 0
            self.end = 0
            self.text = ''
            return

        tok = re.split('\\s+', line)

        if len(tok) < 5:
            raise RuntimeError('Expected line to have at least 5 tokens (found {})'.format(len(tok)))

        self.id = next(ID)
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
        self.besi = re.compile('^.*_[BESI]$')

    def getAnnotation(self, name, labelname, samplerate=16000, get_segments=True, rmbesi=False):

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
            if rmbesi:
                text = seg.text
                if self.besi.match(text):
                    text = text[:-2]
                label['value'] = text
            else:
                label['value'] = seg.text

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
        with codecs.open(file, encoding='utf-8') as f:
            for num, line in enumerate(f):
                try:
                    seg = Segment(line.strip())
                except Exception as err:
                    raise RuntimeError(err, 'Error in {}:{} >{}<'.format(file, num, line.strip()))
                if not seg.file in self.files:
                    self.files[seg.file] = File(seg.file)
                self.files[seg.file].segments.append(seg)

        for name, file in self.files.items():
            file.segments = sorted(file.segments, key=lambda seg: seg.start)
