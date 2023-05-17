from collections import Counter
from datetime import datetime
import json
import re
import os


number = re.compile(r'[АВЕКМНОРСТУХавекмнорстух]\d{3}[АВЕКМНОРСТУХавекмнорстух]{2}[\s1]?\d{2,3}')
number2 = re.compile(r'[АВЕКМНОРСТУХавекмнорстух]\d{3}[АВЕКМНОРСТУХавекмнорстух]{2}')
number_lat = re.compile(r'[ABEKMHOPCTYXabekmhopctyx]\d{3}[ABEKMHOPCTYXabekmhopctyx]{2}[\s1]?\d{2,3}')
number2_lat = re.compile(r'[ABEKMHOPCTYXabekmhopctyx]\d{3}[ABEKMHOPCTYXabekmhopctyx]{2}')
number3_lat = re.compile(r'[ABEKMHOPCTYXabekmhopctyx]\d{3}[ABEKMHOPCTYXabekmhopctyx]{2}[\s1]?(\d{2,3})')
number4 = re.compile(r'(\d{2,3})1?\b')
# for filename in os.listdir('jsons'): # :      ['н312хв777.json']
	# with open(f'jsons/{filename}') as f:
	#	data = json.load(f)
		
	# print(f'{filename:>50}')
	# source = data['result']
	
	
def prepare(source):
    with open('list.json', mode='w', encoding='utf8') as f:
        json.dump({'result': source}, f, ensure_ascii=False)
    res = set()
    res1, res2, res3, res4, res5 = [], [], [], [], []
    p = set()
    word3 = []
    for word in source:
        word = word.upper()
        word1 = [word, word.replace(' ', '')]
        for s, f in [["O", '0'], ["8", 'B'], ["4", "A"],
         ["B", "3"], ['0', "O"], ['1', 'T'], ['T', '1'], ["B", "8"]]:
            word2 = []
            for w in word1:
                word2.append(w.replace(s, f))
            word1 = word1 + word2
        word1 = ' '.join(set(word1))
        word1 = word + ' ' + word1
        word3.append(word1)
        s = number2_lat.findall(word1)
        s2 = number_lat.findall(word1)
        s3 = number3_lat.findall(word1)
        s4 = number4.findall(word1)
		# print(s2, s, sep='\n')
        if s:
            # s1 = list(map(str.upper, s))
            res |= set(s)
            res1.extend(s)
        if s2:
            # s2 = list(map(str.upper, s2))
            p |= set(s2)
            res2.extend(s2)
        if s3:
            res3.extend(s3)
        if s4:
            res4.extend(s4)
    # print(source, res1, res2, res3, sep='\n')
    res2 = list(map(lambda x: x[:6] + x[7:] if x[6] in '1 ' else x, res2))
    out1 = Counter(res1)
    out2 = Counter(res2)
    out3 = Counter(res3)
    out4 = Counter(res4)
    print(out1, out2, out3, Counter(res4), sep='\n')
    try:
        assert len(res2) != 0
        num = max(out1.keys(), key=lambda x: out1[x])
        reg = max(out4.keys(), key=lambda x: out4[x])
        return num + reg
    except Exception as e:
        print(e.__class__.__name__, e)
        return None
    


if __name__ == '__main__':
    with open('list.json') as f:
        data = json.load(f)
    print(prepare(data['result']))
		
		

