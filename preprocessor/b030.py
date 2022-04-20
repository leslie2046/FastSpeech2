import os

import librosa
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm
from pypinyin import pinyin, Style
from text import _clean_text

def get_all_files(path, ext='.pcm'):
    files = []
    children = os.listdir(path)
    for child in children:
        sub_path = os.path.join(path, child)
        if os.path.isdir(sub_path):
            sub_files = get_all_files(sub_path)
            files.extend(sub_files)
        else:
            if ext is None or sub_path.endswith(ext) == True:
                files.append(sub_path)

    return files

def prepare_align(config):
    in_dir = config["path"]["corpus_path"]
    out_dir = config["path"]["raw_path"]
    sampling_rate = config["preprocessing"]["audio"]["sampling_rate"]
    max_wav_value = config["preprocessing"]["audio"]["max_wav_value"]
    cleaners = config["preprocessing"]["text"]["text_cleaners"]
    wav_root_path=os.path.join(in_dir,"wav/B030")
    #for dataset in os.listdir(wav_root_path):
    #    print("Processing {} dataset...".format(dataset))
    with open(os.path.join(in_dir, 'transcript', "transcript_B030.txt"), encoding="utf-8") as f:
        for line in tqdm(f):
            wav_name, text = line.strip("\n").split()
            speaker = wav_name[:10]
            wav_path = os.path.join(wav_root_path, speaker, '{}.wav'.format(wav_name))
            text = _clean_text(text.strip(), cleaners)
            pinyins = [
                p[0]
                for p in pinyin(text, style=Style.TONE3, strict=False, neutral_tone_with_five=True)
            ]
            print(pinyins)
            print(text)
            pyline = ' '.join(pinyins)
            print(pyline)
            print(wav_path)
            if os.path.exists(wav_path):
                os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)
                wav, _ = librosa.load(wav_path, sampling_rate)
                wav = wav / max(abs(wav)) * max_wav_value
                wavfile.write(
                    os.path.join(out_dir, speaker, '{}.wav'.format(wav_name)),
                    sampling_rate,
                    wav.astype(np.int16),
                )
                with open(
                    os.path.join(out_dir, speaker, "{}.lab".format(wav_name)),
                    "w",
                ) as f1:
                    f1.write(" ".join(pyline))

