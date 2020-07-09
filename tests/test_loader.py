import pytest
import dataclasses
import torchaudio
from utils.sound_dataset import SoundDataset

FILE_CSV = './tests/test_loader_data/test-example.csv'
ROOT_DIR = './tests/test_loader_data'


@dataclasses.dataclass
class Case:
    marks: dict = None
    index: int = 0


TEST_CASES_LOADER = [
    Case(index=0,
         marks={'gender': 'male', 'number': 111, 'sample_rate': 24000,
                'path': 'test-example/c244c3dc1b.wav'}),
    Case(index=1,
         marks={'gender': 'female', 'number': 22, 'sample_rate': 24000,
                'path': 'test-example/36687b45a7.wav'}),
    Case(index=2,
         marks={'gender': 'male', 'number': 33, 'sample_rate': 24000,
                'path': 'test-example/c1d8ef6242.wav'}),
    Case(index=3,
         marks={'gender': 'female', 'number': 44, 'sample_rate': 24000,
                'path': 'test-example/209c6fb213.wav'})
]


@pytest.mark.parametrize('t', TEST_CASES_LOADER, ids=str)
def test_gender_loading(t: Case) -> None:
    u_set = SoundDataset(FILE_CSV, ROOT_DIR)
    assert u_set[t.index]['gender'] == t.marks['gender']


@pytest.mark.parametrize('t', TEST_CASES_LOADER)
def test_number_loading(t: Case) -> None:
    u_set = SoundDataset(FILE_CSV, ROOT_DIR)
    assert u_set[t.index]['number'] == t.marks['number']


@pytest.mark.parametrize('t', TEST_CASES_LOADER)
def test_sample_rate_loading(t: Case) -> None:
    u_set = SoundDataset(FILE_CSV, ROOT_DIR)
    assert u_set[t.index]['sample_rate'] == t.marks['sample_rate']


@pytest.mark.parametrize('t', TEST_CASES_LOADER)
def test_path_loading(t: Case) -> None:
    u_set = SoundDataset(FILE_CSV, ROOT_DIR)
    assert u_set[t.index]['path'] == t.marks['path']


@pytest.mark.parametrize('t', TEST_CASES_LOADER)
def test_wavefront_size(t: Case) -> None:
    u_set = SoundDataset(FILE_CSV, ROOT_DIR)
    sample = u_set[t.index]
    wave, sample_rate = torchaudio.load(ROOT_DIR + '/' + sample['path'])
    assert sample['waveform'].size() == wave.size()


@pytest.mark.parametrize('t', TEST_CASES_LOADER)
def test_wavefront_loading_1(t: Case) -> None:
    u_set = SoundDataset(FILE_CSV, ROOT_DIR)
    sample = u_set[t.index]
    wave, sample_rate = torchaudio.load(ROOT_DIR + '/' + sample['path'])
    idx = wave.size()[1] // 3
    assert sample['waveform'][0][idx] == wave[0][idx]


@pytest.mark.parametrize('t', TEST_CASES_LOADER)
def test_wavefront_loading_2(t: Case) -> None:
    u_set = SoundDataset(FILE_CSV, ROOT_DIR)
    sample = u_set[t.index]
    wave, sample_rate = torchaudio.load(ROOT_DIR + '/' + sample['path'])
    idx = wave.size()[1] // 2
    assert sample['waveform'][0][idx] == wave[0][idx]


def test_loader_len() -> None:
    u_set = SoundDataset(FILE_CSV, ROOT_DIR)
    assert len(u_set) == 4
