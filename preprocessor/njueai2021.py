import os

import librosa
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm
from pypinyin import pinyin, Style
from text import _clean_text
def get_all_files(path, ext='.wav'):
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
    for speaker in tqdm(os.listdir(in_dir)):
        print("Processing {} speaker...".format(speaker))
        for text_path in tqdm(get_all_files(os.path.join(in_dir, speaker),'.trn')):
            base_name = os.path.basename(text_path)[:-4]
            text_path = os.path.join(
                in_dir, speaker, "{}.trn".format(base_name)
            )
            wav_path = os.path.join(
                in_dir, speaker, "{}.wav".format(base_name)
            )
            with open(text_path) as f:
                text = f.readline().strip("\n")
            text = _clean_text(text, cleaners)
            pinyins = [
                p[0]
                for p in pinyin(text, style=Style.TONE3, strict=False ,errors='ignore', neutral_tone_with_five=True)
            ]
            pyline = ' '.join(pinyins)
            if os.path.exists(text_path) and os.path.exists(wav_path):
                os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)
                #print(pyline)
                #print(os.path.join(out_dir, speaker,"{}.wav".format(base_name)))
                #print(os.path.join(out_dir, speaker,"{}.lab".format(base_name)))
                wav, _ = librosa.load(wav_path, sampling_rate)
                wav = wav / max(abs(wav)) * max_wav_value
                wavfile.write(
                    os.path.join(out_dir, speaker, "{}.wav".format(base_name)),
                    sampling_rate,
                    wav.astype(np.int16),
                )
                with open(
                    os.path.join(out_dir, speaker, "{}.lab".format(base_name)),
                    "w",
                ) as f1:
                    f1.write(pyline)

