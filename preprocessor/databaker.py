import os

import librosa
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm

from pypinyin import pinyin, Style
from text import _clean_text


def prepare_align(config):
    in_dir = config["path"]["corpus_path"]
    out_dir = config["path"]["raw_path"]
    sampling_rate = config["preprocessing"]["audio"]["sampling_rate"]
    max_wav_value = config["preprocessing"]["audio"]["max_wav_value"]
    cleaners = config["preprocessing"]["text"]["text_cleaners"]
    speaker = "DataBaker"
    with open(os.path.join(in_dir, "ProsodyLabeling/000001-010000.txt"), encoding="utf-8") as f:
        line_count = 0
        for line in tqdm(f):
            print(line)
            line_count += 1
            if(line_count%2==1):
                parts = line.strip().split()
                base_name = parts[0]
                text = parts[1].strip()
                text = _clean_text(text, cleaners)
                pinyins = [
                    p[0]
                    for p in pinyin(text, style=Style.TONE3, strict=False, neutral_tone_with_five=True)
                ]
                print(pinyins)
                print(text)
                pyline = ' '.join(pinyins)
            if(line_count%2==0):
                continue
            print(base_name)
            print(pyline)
            wav_path = os.path.join(in_dir, "Wave", "{}.wav".format(base_name))
            if os.path.exists(wav_path):
                os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)
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
