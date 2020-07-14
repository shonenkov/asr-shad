from torchaudio.transforms import Resample, MFCC
import torchaudio
import os
import numpy as np


def word_wave_iterator(filename, n=None):
    """Yields waveforms of single words transformed to [1, 10000] shape
    overlap of 2000 frames
    Beware! A lot of magic numbers!
    """
    new_sample_rate = 8000
    waveform, sample_rate = torchaudio.load(filename)
    # trimming silence in the end
    waveform = waveform[:, :-4000]
    if n is not None:
        # train
        i = 0
        step = waveform.shape[1] // n
        while i < waveform.shape[1] - 8000:
            chunk = waveform[:, i:i+step+1000]
            yield Resample(chunk.shape[1], new_sample_rate)(chunk)
            i += step
    else:
        # test
        # def get_chunks(arr, w_size):
        #     if arr.shape[0] == 1: arr = arr.reshape(-1)
        #     slices = []
        #     for i, window in enumerate(np.array_split(arr, range(w_size, len(arr), w_size))):
        #         if np.min(window.numpy()) < -0.4:
        #             slices.append(np.argmin(window) + i * w_size)
        #     return np.split(arr, slices)
        # for chunk in get_chunks(waveform, w_size=2000):
        #     if len(chunk) >= 5000: 
        #         chunk = chunk.reshape((1, chunk.shape[0]))
        #         yield Resample(chunk.shape[1], new_sample_rate)(chunk)
        i = 0
        step = 10000
        while i < waveform.shape[1] - 8000:
            chunk = waveform[:, i:i+step+1000]
            yield Resample(chunk.shape[1], new_sample_rate)(chunk)
            i += step


def word_feature_iterator(resources_path, df):
    """Yields features from given dataframe
    """
    for i, row in df.iterrows():
        filename = os.path.join(resources_path, row.path)
        if row.get('text') and row.get('num_words'):
            # train
            ww_iter = word_wave_iterator(filename, row.num_words)
            for word in row.text.split(' '):
                word_wave = next(ww_iter)
                mfcc = MFCC()(word_wave).log2()
                # replace nans with zeros
                mfcc[mfcc != mfcc] = 0
                yield word, word_wave, mfcc, row.gender
        else:
            # test
            ww_iter = word_wave_iterator(filename)
            for word_wave in ww_iter:
                mfcc = MFCC()(word_wave).log2()
                # replace nans with zeros
                mfcc[mfcc != mfcc] = 0
                yield None, word_wave, mfcc, None