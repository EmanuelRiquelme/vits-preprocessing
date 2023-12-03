import numpy as np
from scipy.io import wavfile
import numpy as np
from scipy.signal import resample
import soundfile as sf

def change_sr(data,current_sr,target_sr):
    data = np.mean(data,-1)
    data = data / np.max(np.abs(data))
    resampling_factor = target_sr / current_sr 
    resampled_audio = resample(data, int(len(data) * resampling_factor))
    return resampled_audio 

def load_wav_file(file_path):
    # Read the WAV file
    sample_rate, data = wavfile.read(file_path)
    return sample_rate, data

def extract_audio(audio_array,sample_rate,start,end,out_name,target_sr):
    chunk_left,chunk_right = int(sample_rate*start),int(sample_rate*end)
    audio_chunk = audio_array[chunk_left:chunk_right,:]
    audio_chunk = change_sr(audio_chunk,sample_rate,target_sr)
    audio_chunk = audio_chunk/ np.max(np.abs(audio_chunk))
    sf.write(out_name, audio_chunk, target_sr)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def create_or_update_file(file_path):
    with open(file_path, 'w'):
        pass 

def alignment_bug(results):
    to_delete = []
    for i in range(len(results['segments'])):
        if is_float(results['segments'][i]['text']):
            to_delete.append(i)
    to_delete.sort(reverse=True)
    for index in to_delete:
        if 0 <= index < len(results['segments']):
            results['segments'].pop(index)
    return results
