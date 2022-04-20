#!/bin/sh
if [ $# != 2 ];then
echo "e.g:$0 <model> <restore_step>"
exit 1;
fi
model=$1
restore_step=$2
for text in $(cat datasets/test.txt)
do
   # echo $text
    python3 synthesize.py --text $text  --speaker_id 0  --restore_step $restore_step  --mode single  -p config/$model/preprocess.yaml -m config/$model/model.yaml -t config/$model/train.yaml
done
