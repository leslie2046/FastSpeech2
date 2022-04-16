### 学习笔记
---
###### DataBaker-origin-labeling: 
- 标注：*.lab使用标贝自带标注
- 辞典：lexicon/mandarin_pinyin.dict(mfa官方辞典,2003个拼音)
- 音素集：lexicon/phones/mandarin_pinyin_phones.txt(mfa官方辞典统计而出),共计130个音素,训练或者合成时需要检查text/pinyin.py里是否一致
- mfa声学模型：./aligner_models/mandarin.zip（mfa官方预训练的模型）



###### DataBaker1:
- 标注：*.lab使用pypinyin自动汉字转拼音,清除了标点符号
- 辞典：用上面的拼音标注使用mfa g2p得到的辞典，由于未覆盖所有拼音，合并了lexicon/mandarin_pinyin.dict
      得到lexicon/db_mandarin_pinyin.dict，2010个拼音
- 音素集：lexicon/phones/db_mandarin_pinyin_phones.txt(lexicon/db_mandarin_pinyin.dict统计而出)，比lexicon/mandarin_pinyin_phones.txt多
          5个音素(ei5 iu1 iu2 iu3 iu4),共计135个音素,训练或者合成时需要检查text/pinyin.py里是否一致
- mfa声学模型：mfa train训练标贝语料，使用以上标注和辞典得到的声学模型。


###### DataBaker2:
- 标注：同1
- 辞典：同1
- mfa声学模型：同1
- 音素集合：同1
最新版本的mfa已经不包含sp，所以此版本与1的唯一区别在于预处理时，把textgrid里的""替换为sp,以获得sp的正确标注来对sp建模

###### DataBaker3:
- 修改preprocess.yaml max_wav_value 32768->32767,并修改为16K，其他与DataBaker2相同
- nohup mfa train raw_data/DataBaker/ lexicon/db_mandarin_pinyin.dict ./preprocessed_data/DataBaker/ -o DataBaker --phone_set PINYIN  --overwrite -j 30 --clean  -v --output_format long_textgrid >> nohup_db.log 2>&1 &


###### njueai2021:
- 发音人 liuyunchen:42283句
- 标注：采用讯飞ASR语音转写成文字，再用pypinyin转成拼音到lab
- 词典: lexicon/db_mandarin_pinyin.dict
- 音素集:lexicon/phones/db_mandarin_pinyin_phones.txt
- mfa声学模型:mfa train训练njueai2021，使用以上标注和辞典得到的声学模型。
- 

njueai客服2021年语料，过滤掉时长过小和过大的，保留2~10秒的。
```
find /mnt/share/ai/data_files/voice/liuyunchen/2021*/ -type f -name liuyunchen*.wav  -size +62k -size -320k|xargs  -n1 -I{} cp -n {}  /mnt/share/ai/njueai2021/liuyunchen/
```
```
find /mnt/share/ai/data_files/voice/2021*/*/liuyunchen  -type f -name liuyunchen*.wav  -size +62k -size -320k|xargs  -n1 -I{} cp -n {}  /mnt/share/ai/njueai2021/liuyunchen/
```
用讯飞的ASR进行自动转写,不要标点符号，数字要用中文来表示
```
./xunfei_decode.sh /home/njue/software/code/FastSpeech2/datasets/njueai2021/liuyunchen/ 7
```

删除空的标注文件
```
find . -name "*.trn" -type f -size 0c   |xargs -n1 -I{}  rm {}
```
过滤掉包含英文字母的语料
```
grep -r [a-zA-Z] *.trn |awk -F ':' '{print $1'} > eng.list
```
```
cat eng.list |xargs -n1 -I{}  rm {}
```
```
python3 prepare_align.py config/njueai2021/preprocess.yaml
```
修改preprocess.yaml max_wav_value 32768->32767
```
mfa g2p ./g2p/mandarin_pinyin_g2p_2.0.zip ./raw_data/njueai2021 lexicon/njueai2021_mandarin_pinyin.dict  -clean -v --overwrite -j 28
```
g2p得到的词典，为db_mandarin_pinyin.dict的子集，所以没有增加新的词，可以直接沿用db_mandarin_pinyin.dict

```
nohup mfa train raw_data/njueai2021/ lexicon/db_mandarin_pinyin.dict ./preprocessed_data/njueai2021/ -o njueai2021 --phone_set PINYIN  --overwrite -j 30 --clean  -v --output_format long_textgrid >> nohup_njueai.log 2>&1 &	    
```
训练声学模型时带上了phone_set为PINYIN，并设置为30线程并行,
