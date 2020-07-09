import pandas as pd
import os
import torchaudio
from torch.utils.data import Dataset


class SoundDataset(Dataset):

    def __init__(self, csv_file, root_dir, transform=None):
        self.root_dir = root_dir
        self.marking = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.marking)

    def __getitem__(self, idx):
        path = self.marking['path'][idx]
        gender = self.marking['gender'][idx]
        number = self.marking['number'][idx]

        all_path = os.path.join(self.root_dir, path)
        waveform, sample_rate = torchaudio.load(all_path)
        sample = {'waveform': waveform, 'gender': gender,
                  'number': number, 'sample_rate': sample_rate, 'path': path}

        if self.transform:
            sample = self.transform(sample)

        return sample
