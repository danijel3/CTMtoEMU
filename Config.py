from uuid import uuid1
from collections import OrderedDict


def get_default_emu_config():
    config = OrderedDict()

    perspectives = []
    config['perspectives'] = perspectives

    def_perspective = OrderedDict()
    perspectives.append(def_perspective)

    def_perspective['name'] = 'default'

    sig_cnv = OrderedDict()
    def_perspective['signalCanvases'] = sig_cnv

    assign_spec = OrderedDict()
    assign_spec['signalCanvasName'] = 'SPEC'
    assign_spec['ssffTrackName'] = 'FORMANTS'

    formant_colors = OrderedDict()
    formant_colors['ssffTrackName'] = 'FORMANTS'
    formant_colors['colors'] = ['rgb(255,100,100)', 'rgb(100,255,100)', 'rgb(100,100,255)', 'rgb(100,255,255)']

    sig_cnv['order'] = ['OSCI', 'SPEC']
    sig_cnv['assign'] = [assign_spec]
    sig_cnv['contourLims'] = []
    sig_cnv['contourColors'] = [formant_colors]

    lev_cnv = OrderedDict()
    def_perspective['levelCanvases'] = lev_cnv

    lev_cnv['order'] = ['Word', 'Phoneme']

    twodim_cnv = OrderedDict()
    def_perspective['twoDimCanvases'] = twodim_cnv

    twodim_cnv['order'] = []

    restrictions = OrderedDict()
    config['restrictions'] = restrictions

    restrictions['showPerspectivesSidebar'] = False

    buttons = OrderedDict()
    config['activeButtons'] = buttons

    buttons['saveBundle'] = False
    buttons['showHierarchy'] = True

    return config


def getLevel(name, labelname, itemtype='SEGMENT', labeltype='STRING'):
    level = OrderedDict()

    level['name'] = name
    level['type'] = itemtype

    attrs = []
    level['attributeDefinitions'] = attrs

    if not type(labelname) is list:
        labelname = [labelname]

    for label in labelname:
        attr = OrderedDict()
        attrs.append(attr)

        attr['name'] = label
        attr['type'] = labeltype

    return level


def getLink(from_level, to_level, type='ONE_TO_MANY'):
    link = OrderedDict()
    link['type'] = type
    link['superlevelName'] = from_level
    link['sublevelName'] = to_level
    return link


def get_config(name):
    config = OrderedDict()

    config['name'] = name
    config['UUID'] = str(uuid1())
    config['mediafileExtension'] = 'wav'

    tracks = []
    config['ssffTrackDefinitions'] = tracks

    formants = OrderedDict()
    tracks.append(formants)

    formants['name'] = 'FORMANTS'
    formants['columnName'] = 'fm'
    formants['fileExtension'] = 'fms'

    levels = []
    config['levelDefinitions'] = levels

    levels.append(getLevel('Utterance', 'Utterance', itemtype='ITEM'))
    levels.append(getLevel('Word', 'Word'))
    levels.append(getLevel('Syllable', ['Syllable', 'Stress'], itemtype='ITEM'))
    levels.append(getLevel('Phonetic Syllable', ['Syllable', 'Stress'], itemtype='ITEM'))
    levels.append(getLevel('Phoneme', 'Phoneme'))

    links = []
    config['linkDefinitions'] = links

    links.append(getLink('Utterance', 'Word'))
    links.append(getLink('Word', 'Syllable'))
    links.append(getLink('Word', 'Phonetic Syllable'))
    links.append(getLink('Syllable', 'Phoneme'))
    links.append(getLink('Phonetic Syllable', 'Phoneme'))

    config['EMUwebAppConfig'] = get_default_emu_config()

    return config
