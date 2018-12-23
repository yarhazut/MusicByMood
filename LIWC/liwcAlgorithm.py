import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
with open('LIWC2007_English100131.dic') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
dicNames_toValues = dict()
names_toSuject=dict()
var = 'true';
for line in content:
    if (var=='true' and line != '%'):
        lines=line.split("\t");
        dicNames_toValues[lines[0]]=lines[1];
    elif(line != '%'):
        lines=re.split('\t|( )',line);
        lines = [x for x in lines if x is not None]
        myarray = np.asarray(lines)
        lines[0]=lines[0].replace('*', '')
        names_toSuject[lines[0]]=myarray[1:len(myarray)]
    if (line == '%'):
        var='false';
gettysburg = '''Four score and seven years ago our fathers brought forth on
  this continent a new nation, conceived in liberty, and dedicated to the
  proposition that all men are created equal. Now we are engaged in a great
  civil war, testing whether that nation, or any nation so conceived and so
  dedicated, can long endure. We are met on a great battlefield of that war.
  We have come to dedicate a portion of that field, as a final resting place
  for those who here gave their lives that that nation might live. It is
  altogether fitting and proper that we should do this.'''
gettysburg_tokens = re.split('\t|( )',gettysburg);
gettysburg_tokens = [x for x in gettysburg_tokens if x is not None]
buckets = [0] * 464
for word in gettysburg_tokens:
    if (word.lower() in names_toSuject):
        subjects=names_toSuject[word.lower()]
        for subject in subjects:
            buckets[int(subject)]+=1
bucket1 = [0] * 464
print(cosine_similarity([buckets], [buckets]))