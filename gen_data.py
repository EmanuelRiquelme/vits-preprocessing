import os
#import soundfile as sf
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
import whisperx
import gc
from utils import load_wav_file,extract_audio,alignment_bug,create_or_update_file
from text import read_lines,write_file
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--target_sr', type=int, default=22500, help='Target sampling rate')
parser.add_argument('--output_dir', type=str, default='dataset', help='Directory of the output files')
parser.add_argument('--audio_dir', type=str, default='audio', help='Directory of audio files')

device = "cuda" 
batch_size = 16 # reduce if low on GPU mem
language = 'es'
try: 
    model = whisperx.load_model("large-v2", device, compute_type='float16',language = language)
except:
    model = whisperx.load_model("large-v2", device, compute_type='int8',language = language)

def generate_clips_transcriptions(audio_file,array,sample_rate,root_dir,target_sr,global_index):
    #performs transcriptions saves the clips and generates txt files without phenomizers
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    model_a, metadata = whisperx.load_align_model(language_code=language, device=device)
    alignment_bug(result)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    time_range = [1,9]
    for i in range(len(result["segments"])):
        current_dir = result['segments'][i]
        text = current_dir['text']
        start,end = current_dir['start'],current_dir['end']
        duration = end-start
        if duration > time_range[0] and duration < time_range[1]:
            if len(text.split(' ')) > 1:
                global_index += i
                location = f'{root_dir}/audios/{global_index+i}.wav'
                line = f'{location}|{text}'
                file_path = f'{root_dir}/audios/{global_index+i}.wav'
                extract_audio(array,sample_rate,start,end,file_path,target_sr)
                with open(f'{root_dir}/data.txt', 'a') as file:
                    file.write(line + "\n")
    return global_index 

def queue(audio_list,target_sr,root_dir):
    global_index = 0
    create_or_update_file(f'{root_dir}/data.txt')
    for audio_file in os.listdir(audio_list):
        audio_file = f'{audio_list}/{audio_file}'
        try:
            sample_rate,array = load_wav_file(audio_file)
            global_index = generate_clips_transcriptions(audio_file,array,sample_rate,root_dir,target_sr,global_index)
        except Exception as e:
            print(f"Error processing {audio_file}: {str(e)}")

if __name__ == '__main__':
    #create directory file_path if it doesn't exist
    args = parser.parse_args()
    target_sr = args.target_sr
    file_path = args.output_dir
    audio_list = args.audio_dir
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    audios_dir = f'{file_path}/audios'
    if not os.path.exists(audios_dir):
        os.makedirs(audios_dir)
    queue(audio_list,target_sr,root_dir = file_path)
