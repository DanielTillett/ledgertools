import json
import os.path

config = None


def read_config():
    global config
    f = os.path.expanduser('~/.ltconfig')
    if not os.path.isfile(f):
        # file doesn't exist; empty config
        config = {}
    else:
        fp = open(f)
        config = json.load(fp)


def rootdir():
    if 'rootdir' not in config:
        return None
    return os.path.expanduser(config['rootdir'])


def outdir(acc):
    """
    Determine the outdir for the given account.

    Return None if not specified.
    """
    if not rootdir():
        return None
    try:
        return os.path.join(rootdir(), config['accounts'][acc]['outdir'])
    except KeyError:
        try:
            return os.path.join(rootdir(), config['outdir'])
        except KeyError:
            return None


def outpat(acc):
    """
    Determine the full outfile pattern for the given account.

    Return None if not specified.
    """
    if not outdir(acc):
        return None
    try:
        return os.path.join(outdir(acc), config['accounts'][acc]['outpat'])
    except KeyError:
        try:
            return os.path.join(outdir(acc), config['outpat'])
        except KeyError:
            return None


def format_outpat(outpat, xn):
    """
    Format an outpat for the given transaction.

    Currently recognised fields are:
    - date.<attr> where attr is a valid datetime.Date field
    """
    return outpat.format(date=xn.date)


def rulesdir(acc):
    """
    Determine the rulesdir for the given account.

    Return None if not specified.
    """
    if not rootdir():
        return None
    try:
        return os.path.join(rootdir(), config['accounts'][acc]['rulesdir'])
    except KeyError:
        try:
            return os.path.join(rootdir(), config['rulesdir'])
        except KeyError:
            return None


def rulefiles(acc):
    """
    Return a list of rulefiles for the given account (or the common rulefiles
    if None is given.

    Returns an empty list if none specified.
    """
    if acc is None:
        # return the common rulesfiles
        try:
            d = rulesdir(None)
            if d is None:
                return None
            return map(lambda x: os.path.join(d, x), config['rules'])
        except KeyError:
            return []
    try:
        d = rulesdir(acc)
        rules = [] if d is None else map(
            lambda x: os.path.join(d, x),
            config['accounts'][acc]['rules']
        )
        return rulefiles(None) + rules
    except KeyError:
        return rulefiles(None)


def reader(acc):
    """Return the reader for the given account, or None if none specified."""
    try:
        return config['accounts'][acc]['reader']
    except KeyError:
        try:
            return config['reader']
        except KeyError:
            return None


read_config()
