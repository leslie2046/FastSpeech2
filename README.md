
### 预处理
---
###### 数据集准备对齐

```
python3 prepare_align.py config/DataBaker/preprocess.yaml
```


###### MFA制作辞典
[点此](https://github.com/MontrealCorpusTools/mfa-models/tree/main/g2p)下载的g2p模型，从自己的语料中生成辞典。

```
mfa g2p ./g2p/mandarin_pinyin_g2p_2.0.zip ./raw_data/DataBaker lexicon/db_mandarin_pinyin.dict
```
###### 生成音素符号表
```
cat db_mandarin_pinyin.dict |awk -F ' ' '{for(i=2;i<=NF;i++)print $i'}|sort|uniq > db_mandarin_pinyin_phones.txt
```

###### MFA模型训练
[项目源码地址](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner)
会顺带着输出声学模型和TextGrid文件
mfa train corpus_directory dictionary_path output_paths 

mfa训练一个用于音素对齐的声学模型
- corpus_directory:语料目录，成对的.lab和*.wav，.lab文件就是单词/拼音标注文件。
- dictionary_path:音素辞典路径，即训练得到的声学模型的音素来源于此辞典
- output_paths:模型输出目录


```


mfa train raw_data/testmandarin/  lexicon/db_mandarin_pinyin.dict ./textgrid/ -o ./aligner_models/ --overwrite -j 20 --clean --output_format long_textgrid
```
```
mfa train raw_data/DataBaker lexicon/db_mandarin_pinyin.dict ./textgrid/DataBaker -o ./aligner_models/ --overwrite -j 20 --clean --output_format long_textgrid
```

###### MFA下载
https://github.com/MontrealCorpusTools/mfa-models
MFA2.0版本的模型以后使用的是IPA音素集，若使用的是CMU dict或者汉语拼音音素集可以自行到以上链接去下载1.0版本的模型和字典。
[声学模型下载地址](https://github.com/MontrealCorpusTools/mfa-models/tree/main/acoustic)
[辞典下载地址](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary)


下载英文的根据IPA音素集训练的声学模型和字典

```
mfa models download acoustic english_mfa
```
```
mfa models download dictionary english_mfa
```

下载中文拼音的根据IPA音素表训练的声学模型和字典

```
mfa models download acoustic mandarin_mfa
```
```
mfa model download dictionary mandarin_mfa
```

###### MFA对齐

强制音素对齐命令输出TextGrid格式标注文件，可以使用下载下来的官方提供的预训练的声学模型和配套字典，也可以使用自己训练的声学模型和配套的字典。

mfa align corpus_directory dictionary_path acoustic_model_path output_directory --clean
```

mfa align raw_data/test english_mfa english_mfa ./textgrid --overwrite --clean --output_format long_textgrid
```
```
mfa align raw_data/testmandarin/ \
./lexicon/db_mandarin_pinyin.dict \
./aligner_models/db_mandarin_pinyin.zip \
textgrid/testmandarin \
--overwrite -j 20 --clean --output_format long_textgrid
```

###### 预处理
输出duration,energy,mel,pitch,speakers.json,stats.json,train.txt,val.txt

```
python3 preprocess.py config/DataBaker/preprocess.yaml
```

### 训练
---
###### 训练fastspeech2模型
```
python3 train.py -p config/DataBaker/preprocess.yaml -m config/DataBaker/model.yaml -t config/DataBaker/train.yaml --restore_step 111000
```
- restore-step：继续训练的模型

### 合成
---

- 单句合成
```
python3 synthesize.py --text "大家好" --speaker_id 0 --restore_step 200000 --mode single -p config/DataBaker/preprocess.yaml -m config/DataBaker/model.yaml -t config/DataBaker/train.yaml
```

- 批量合成
```
python3 synthesize.py --source preprocessed_data/DataBaker/val.txt --restore_step 200000 --mode batch -p config/DataBaker/preprocess.yaml -m config/DataBaker/model.yaml -t config/DataBaker/train.yaml
```


### tensorboard
---
```
tensorboard --logdir output/log/DataBaker --bind_all
```
### 学习笔记
---
###### DataBaker-origin-labeling: 
- 标注：*.lab使用标贝自带标注
- 辞典：lexicon/mandarin_pinyin.dict(mfa官方辞典,2003个拼音)
- 对齐所用声学模型：./aligner_models/mandarin.zip（mfa官方预训练的模型）
- 音素集：lexicon/mandarin_pinyin_phones.txt(mfa官方辞典统计而出),共计130个音素,训练或者合成时需要检查text/pinyin.py里是否一致


###### DataBaker1:
- 标注：*.lab使用pypinyin自动汉字转拼音,清除了标点符号
- 辞典：用上面的拼音标注使用mfa g2p得到的辞典，由于未覆盖所有拼音，合并了lexicon/mandarin_pinyin.dict
      得到lexicon/db_mandarin_pinyin.dict，2010个拼音
- 对齐所用声学模型：mfa train训练标贝语料，使用以上标注和辞典得到的声学模型。
- 音素集合：lexicon/db_mandarin_pinyin_phones.txt(本辞典统计而出)，比lexicon/mandarin_pinyin_phones.txt多
          5个音素(ei5 iu1 iu2 iu3 iu4),共计135个音素,训练或者合成时需要检查text/pinyin.py里是否一致

###### DataBaker:
- 标注：同1
- 辞典：同1
- 对齐所用声学模型：同1
- 音素集合：同1
最新版本的mfa已经不包含sp，所以此版本与1的唯一区别在于预处理时，把textgrid里的""替换为sp,以获得sp的正确标注来对sp建模
