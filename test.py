
import re

from preprocessor.preprocessor import Preprocessor


if __name__ == "__main__":
    text = '君不见，黄河之水天上来，奔流到海不复回[=hui2]。君不见[=jian4]，高堂明镜悲白发，朝[=zhao3]如青丝暮成雪。'
    pattern = '([\u4e00-\u9fa5])\[=([a-z]+[1-5]{1})\]'
    print(text)
    print(re.sub(r'([\u4e00-\u9fa5])\[=([a-z]+[1-5]{1})\]',r'\2',text))
    text='今天是：11/28/2018'
    print(text)
    print(re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',text))
