#!/usr/bin/python
"""
National Institute of Technology, Kagawa College.
Nakano Masaki(namachan10777) <namachan10777@gmail.com>

truncate and resample audio files for preprocessing of ICA.
"""

import sys
import os.path
import soundfile as sf
import scipy.signal

if __name__ == "__main__":
    sounds = []
    min_len  = sys.maxsize
    target_rate = 16000
    for arg in sys.argv[1:]:
        sig, rate = sf.read(arg, always_2d=True)
        min_len = min(min_len, sig.shape[0] / target_rate)
        sounds.append((arg, sig, rate))

    results = []
    target_sample_n = int(min_len * target_rate)
    for name, sound, rate in sounds:
        cut = sound[0:int(min_len * rate), 0]
        new_name = 'truncated-' + os.path.basename(name) + '.wav'
        sf.write(new_name, scipy.signal.resample(cut, target_sample_n), target_rate)
