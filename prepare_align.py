import argparse

import yaml

from preprocessor import ljspeech, aishell3, libritts,databaker,b030,njueai2021


def main(config):
    if "LJSpeech" in config["dataset"]:
        ljspeech.prepare_align(config)
    if "AISHELL3" in config["dataset"]:
        aishell3.prepare_align(config)
    if "LibriTTS" in config["dataset"]:
        libritts.prepare_align(config)
    if "DataBaker" in config["dataset"]:
        databaker.prepare_align(config)
    if "B030" in config["dataset"]:
        b030.prepare_align(config)
    if "njueai2021" in config["dataset"]:
        njueai2021.prepare_align(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="path to preprocess.yaml")
    args = parser.parse_args()

    config = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    main(config)
