# First find keyword based matcing strategy.

# Need to start reading form here - http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7477706

from os.path import join

from global_constants import *

from glob import glob

from collections import defaultdict

from sklearn.preprocessing import MultiLabelBinarizer

import csv

import re

file_categories = defaultdict(int)
file_tags = defaultdict(int)
for file_name in glob(join(data_path, tags_train, "*.txt")):
    for line in open(file_name).readlines():
        file_tags[line.strip().split(":")[0]] += 1
        file_categories[line.strip().split(":")[1]] += 1

labels = list(set(list(file_categories.keys()) + list(file_tags.keys())))

mlb = MultiLabelBinarizer()
mlb.fit([labels])

rows = [["Name"] + list(mlb.classes_)]

pattern = "\d.*txt"

encoded = {}
for file_name in glob(join(data_path, tags_train, "*.txt")):
    image_set = set()
    for line in open(file_name).readlines():
        image_set = image_set.union(set([line.strip().split(":")[0], line.strip().split(":")[1]]))

    rows.append([int(re.findall(pattern=pattern, string=file_name)[0].strip("\.txt"))] + list(mlb.transform([image_set])[0]))


csv.writer(open('processed_tags.csv', "w")).writerows(rows)
