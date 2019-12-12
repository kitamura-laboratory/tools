#!/usr/bin/python
"""
All source sound files must be same length and rate.
"""

import argparse
import json
import soundfile as sf
import numpy as np
from pathlib import Path
import scipy.signal as signal

IMPULSE_RATE = 48000

def normalize(cfg_path, path):
    if path.is_absolute():
        return path
    else:
        return cfg_path.joinpath(path) 

def convolute(x, impluse):
    L, = x.shape
    L2, = impluse.shape
    convoluted = np.zeros([L])
    for i in range(L):
        convoluted[i:min(L, i+L2)] = convoluted[i:min(L, i+L2)] + x[i:min(L, i+L2)] * impluse[:min(L2, L-i)]
    return convoluted

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convolution')
    parser.add_argument('-c', '--config', required=True)

    args = parser.parse_args()
    cfg_path = Path(args.config)

    sounds_root = cfg_path.parent

    # This script currently convolute sounds in time domain. 
    with open(cfg_path) as f:
        cfg = json.load(f)

        N = len(cfg.keys())
        sample, rate = sf.read(normalize(sounds_root, Path(list(cfg.keys())[0])))
        L, = sample.shape

        results = np.zeros([L, N])

        for key in cfg.keys():
            key_path = normalize(sounds_root, Path(key))
            x, _ = sf.read(key_path)
            for j in range(N):
                impluse_file = open(normalize(sounds_root, Path(cfg[key][j])), 'rb')
                raw = np.fromfile(impluse_file, np.float32, -1)
                impluse = signal.resample_poly(raw, up=rate, down=IMPULSE_RATE)
                results[:,j] += convolute(x, impluse)

        for i in range(N):
            sf.write(f'convoluted{i}.wav', results[:,i], rate)
