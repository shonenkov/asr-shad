import torchaudio
import os
import pandas as pd


def get_audio_meta(filename):
    """
    Compute audio stats for a single file
    :param filename: path to file relative to current working directory
    :return: dict
    """
    waveform, sample_rate = torchaudio.load(filename)
    size_bytes = os.path.getsize(filename)
    return dict(
        filename=os.path.basename(filename),
        channels=waveform.size()[0],
        frames=waveform.size()[1],
        sample_rate_hz=sample_rate,
        size_bytes=size_bytes,
        duration_s=waveform.size()[1] / sample_rate,
        bitrate=int(size_bytes * 8 / waveform.size()[1])
    )


def get_audio_stats(dirname):
    """
    Get a pandas DataFrame with audio stats for every file in provided dir
    :param dirname: path to directory with audiofiles relative to current working directory
    :return: pandas.DataFrame
    """
    records = []
    for filename in os.listdir(dirname):
        audio_meta = get_audio_meta(os.path.join(dirname, filename))
        records.append(audio_meta)
    return pd.DataFrame(records)
