DataBaker-origin-labeling: 
标注：*.lab使用标贝自带标注
辞典：lexicon/mandarin_pinyin.dict(mfa官方辞典,2003个拼音)
对齐所用声学模型：./aligner_models/mandarin.zip（mfa官方预训练的模型）
音素集：lexicon/mandarin_pinyin_phones.txt(mfa官方辞典统计而出),共计130个音素,训练或者合成时需要检查text/pinyin.py里是否一致


DataBaker1:
标注：*.lab使用pypinyin自动汉字转拼音,清除了标点符号
辞典：用上面的拼音标注使用mfa g2p得到的辞典，由于未覆盖所有拼音，合并了lexicon/mandarin_pinyin.dict
      得到lexicon/db_mandarin_pinyin.dict，2014个拼音
对齐所用声学模型：mfa train训练标贝语料，使用以上标注和辞典得到的声学模型。
音素集合：lexicon/db_mandarin_pinyin_phones.txt(本辞典统计而出)，比lexicon/mandarin_pinyin_phones.txt多
          5个音素(ei5 iu1 iu2 iu3 iu4),共计135个音素,训练或者合成时需要检查text/pinyin.py里是否一致

DataBaker:
标注：同1
辞典：同1
对齐所用声学模型：同1
音素集合：同1
最新版本的mfa已经不包含sp，所以此版本与1的唯一区别在于预处理时，把textgrid里的""替换为sp,以获得sp的正确标注来对sp建模
