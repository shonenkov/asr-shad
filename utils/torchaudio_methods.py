import torch
import torchaudio
import matplotlib.pyplot as plt


def draw_waveform(waveform, output_file_name=None):
    plt.figure()
    plt.plot(waveform.t().numpy())
    plt.show()


def draw_spectrogram(waveform):
    spectrogram = torchaudio.transforms.Spectrogram()(waveform)
    plt.imshow(spectrogram.log2()[0, :, :].numpy(), cmap='nipy_spectral')
    plt.show()


def draw_mel_spectrogram(waveform):
    mel_spectrogram = torchaudio.transforms.MelSpectrogram()(waveform)
    plt.imshow(mel_spectrogram.log2()[0, :, :].detach().numpy(), cmap='nipy_spectral')
    plt.show()


def draw_mfcc_spectrogram(waveform):
    mfcc_spectrogram = torchaudio.transforms.MFCC()(waveform)
    plt.imshow(mfcc_spectrogram.log2()[0,:,:].detach().numpy())
    plt.show()
