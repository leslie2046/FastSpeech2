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

###### njueai2021:

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
