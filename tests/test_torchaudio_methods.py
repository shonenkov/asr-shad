import dataclasses
import pytest
import torchaudio
import typing as tp

from utils.torchaudio_methods import draw_waveform, draw_spectrogram


@dataclasses.dataclass
class Case:
    waveform: tp.Any
    kind: tp.Optional[str]
    output_file: tp.Optional[str]
    name: tp.Optional[str] = None

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        return 'draw_waveform'


file = './sample.wav'
waveform, _ = torchaudio.load(file)


TEST_CASES = [
    Case(waveform=waveform, kind='spec', output_file='sample_draw'),
    Case(waveform=waveform, kind='melspec', output_file='sample_draw'),
    Case(waveform=waveform, kind='mfcc', output_file='sample_draw'),
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_draw(t: Case) -> None:
    draw_waveform(t.waveform)
    draw_waveform(t.waveform, t.output_file)
    draw_spectrogram(t.waveform)
    draw_spectrogram(t.waveform, kind=t.kind)
    draw_spectrogram(t.waveform, output_file=t.output_file)
    draw_spectrogram(t.waveform, t.kind, t.output_file)

    assert True


def test_incorrect_kind() -> None:
    with pytest.raises(ValueError, match='Kind should be spec, melspec, mfcc or None'):
        draw_spectrogram(waveform, kind='unknown_kind')
