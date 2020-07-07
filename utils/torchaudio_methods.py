import torchaudio
import matplotlib.pyplot as plt


def draw_waveform(waveform, output_file=None):
    """
    Draw plot of waveform
    :param waveform: torch.Tensor to visualize
    :param output_file: name of output image file without extension, in will automatically be .png.
    By default the plot is shown in the same window.
    """
    plt.figure()
    plt.plot(waveform.t().numpy())
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file)


def draw_spectrogram(waveform, kind='spec', output_file=None):
    """
    Draw plot of a spectrogram of a certain type,
    :param waveform: waveform: torch.Tensor to visualize
    :param kind: spec, melspec, mfcc for spectrogram, mel spectrogram, MFCC correspondingly, default spec
    :param output_file: name of output image file without extension, in will automatically be .png.
    By default the plot is shown in the same window.
    """
    if kind == 'spec':
        spectrogram = torchaudio.transforms.Spectrogram()(waveform)
    elif kind == 'melspec':
        spectrogram = torchaudio.transforms.MelSpectrogram()(waveform)
    elif kind == 'mfcc':
        spectrogram = torchaudio.transforms.MFCC()(waveform)
    else:
        raise ValueError('Kind should be spec, melspec, mfcc or None')

    plt.figure()
    plt.imshow(spectrogram.log2()[0, :, :].numpy(), cmap='nipy_spectral')
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file)
