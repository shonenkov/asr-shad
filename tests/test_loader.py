import pytest
import torchaudio
from utils.SoundDataset import SoundDataset


def test_loader_len() -> None:
    u_set = SoundDataset('./test_loader_data/test-example.csv', './test_loader_data')
    assert len(u_set) == 4


def test_loader_nextitem() -> None:
    u_set = SoundDataset('./test_loader_data/test-example.csv', './test_loader_data')
    sample = u_set[2]
    assert sample['number'] == 33


def test_loader_wavefront() -> None:
    u_set = SoundDataset('./test_loader_data/test-example.csv', './test_loader_data')
    sample = u_set[3]
    wave, sample_rate = torchaudio.load('./test_loader_data/' + sample['path'])

    assert sample['waveform'][0][12] == wave[0][12]


def test_loader_gender() -> None:
    u_set = SoundDataset('./test_loader_data/test-example.csv', './test_loader_data')
    sample = u_set[0]
    assert sample['gender'] == 'male'


def test_loader_rate() -> None:
    u_set = SoundDataset('./test_loader_data/test-example.csv', './test_loader_data')
    sample = u_set[0]
    assert sample['sample_rate'] == 24000

