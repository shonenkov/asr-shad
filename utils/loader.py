import pandas as pd
import torchaudio
import torch
import numpy as np


class LoadSound:
    def __init__(self, root: str, paths: pd.Series):
        self.root = root
        self.paths = paths
        self.Sample_Rates = []
        self.WaveForms = []
        self.max_duration = 0
        self.duration = []

    def loading(self):
        for i in range(len(self.paths)):
            waveform, sample_rate = torchaudio.load((self.root + '/' + self.paths[i]))
            self.WaveForms.append(waveform)
            self.Sample_Rates.append(sample_rate)
            self.duration.append(len(waveform[0]))
        self.max_duration = np.max(self.duration)

    def alignment(self):
        for i in range(self.paths):
            self.WaveForms[i] = torch.cat(
                (self.WaveForms[i], torch.zeros((1, self.max_duration - self.WaveForms[i].size()[1]))), 1)

