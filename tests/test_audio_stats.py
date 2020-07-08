import pytest

from utils.audio_stats import get_audio_stats, get_audio_meta


TEST_CASES_META = [
    {'filename': 'sample_data/0a0e03cd54.wav', 'result': {'filename': '0a0e03cd54.wav','channels': 1,'frames': 77412,'sample_rate_hz': 24000, 'size_bytes': 154868,'duration_s': 3.2255,'bitrate': 16}},
    {'filename': 'sample_data/0a1ed10f59.wav', 'result': {'filename': '0a1ed10f59.wav', 'channels': 1, 'frames': 77483, 'sample_rate_hz': 24000, 'size_bytes': 155010, 'duration_s': 3.228458333333333, 'bitrate': 16}},
    {'filename': 'sample_data/0a2df43d3e.wav', 'result': {'filename': '0a2df43d3e.wav', 'channels': 1, 'frames': 68607, 'sample_rate_hz': 24000, 'size_bytes': 137258, 'duration_s': 2.858625, 'bitrate': 16}},
    {'filename': 'sample_data/0a2f84a7f5.wav', 'result': {'filename': '0a2f84a7f5.wav', 'channels': 1, 'frames': 71262, 'sample_rate_hz': 24000, 'size_bytes': 142568, 'duration_s': 2.96925, 'bitrate': 16}},
    {'filename': 'sample_data/0a5ea040ea.wav', 'result': {'filename': '0a5ea040ea.wav', 'channels': 1, 'frames': 74285, 'sample_rate_hz': 24000, 'size_bytes': 148614, 'duration_s': 3.0952083333333333, 'bitrate': 16}}
]


TEST_CASES_STATS = [
    {
        'dirname': 'sample_data', 
        'result': [
            {'filename': '0a2f84a7f5.wav', 'channels': 1, 'frames': 71262, 'sample_rate_hz': 24000, 'size_bytes': 142568, 'duration_s': 2.96925, 'bitrate': 16}, 
            {'filename': '0a5ea040ea.wav', 'channels': 1, 'frames': 74285, 'sample_rate_hz': 24000, 'size_bytes': 148614, 'duration_s': 3.0952083333333333, 'bitrate': 16}, 
            {'filename': '0a1ed10f59.wav', 'channels': 1, 'frames': 77483, 'sample_rate_hz': 24000, 'size_bytes': 155010, 'duration_s': 3.228458333333333, 'bitrate': 16}, 
            {'filename': '0a2df43d3e.wav', 'channels': 1, 'frames': 68607, 'sample_rate_hz': 24000, 'size_bytes': 137258, 'duration_s': 2.858625, 'bitrate': 16}, 
            {'filename': '0a0e03cd54.wav', 'channels': 1, 'frames': 77412, 'sample_rate_hz': 24000, 'size_bytes': 154868, 'duration_s': 3.2255, 'bitrate': 16}
        ]
    }
]

@pytest.mark.audio_stats
@pytest.mark.parametrize('case', TEST_CASES_META)
def test_audio_meta(case) -> None:
    assert get_audio_meta(case['filename']) == case['result'] 


@pytest.mark.audio_stats
@pytest.mark.parametrize('case', TEST_CASES_STATS)
def test_audio_stats(case) -> None:
    assert get_audio_stats(case['dirname']).to_dict(orient='records') == case['result']