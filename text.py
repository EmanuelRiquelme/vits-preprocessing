import re
from unidecode import unidecode
from phonemizer import phonemize
import argparse

parser = argparse.ArgumentParser(description='Generate the phenomization of the audio transcriptions')

parser.add_argument('--data_dir', type=str, default='dataset', help='Directory of the Data')

_whitespace_re = re.compile(r'\s+')

def convert_to_ascii(text):
  return unidecode(text)

def lowercase(text):
  return text.lower()

def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)

def transliteration_cleaners(text):
  '''Pipeline for Spanish text that transliterates to ASCII.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = phonemize(text, language='es', backend='espeak', strip=True)
  text = collapse_whitespace(text)
  return text

def read_lines(txt_file):
    lines = []
    with open(txt_file, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            dir_name,text = line.split('|')
            text = transliteration_cleaners(text)
            line = f'{dir_name}|{text}'
            lines.append(line)
    return '\n'.join(lines)

def write_file(txt_file,lines):
    f = open(txt_file, 'w+')
    f.write(lines)
    f.close()

if __name__ == '__main__':
    args = parser.parse_args()
    pre_train = f'{args.data_dir}/train.txt'
    train = f'{args.data_dir}/train.txt.cleaned'
    train_files  = read_lines(pre_train)
    write_file(train,train_files)
    pre_train = f'{args.data_dir}/test.txt'
    train = f'{args.data_dir}/test.txt.cleaned'
    train_files  = read_lines(pre_train)
    write_file(train,train_files)
    print('Phenomizers done correctly!')
