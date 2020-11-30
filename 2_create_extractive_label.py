#!/usr/bin/env python
# coding: utf-8

import os
import hashlib
import struct
import subprocess
import collections
import tensorflow as tf
import json, glob, math
import numpy as np
from multiprocessing import Process
import argparse
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

MAX_SENTENCE = 100

def get_string(sentences):
    all_sentence = []
    for sentence in sentences:
        all_sentence.append(' '.join(sentence))
    return ' '.join(all_sentence).lower()

def harmonic_mean(precision, recall):
    if precision == 0 and recall == 0:
        return 0
    return 2 * precision * recall / (precision + recall)

def compute_dictionary (string):
    unigram = {}
    for word in string.split():
        unigram[word] = unigram.get(word, 0) + 1
    return unigram

def rouge1 (summary, reference):
    overlap = 0
    denominator = 0
    for key in reference.keys():
        denominator += reference[key]
        overlap += min(summary.get(key, 0), reference[key])
    return overlap / denominator

def get_score(cur_range, article, unigram_summary):
    cur_article = article[cur_range]
    unigram_article = compute_dictionary(get_string(cur_article).lower())
    precision = rouge1(unigram_summary, unigram_article)
    recall = rouge1(unigram_article, unigram_summary)
    return harmonic_mean(precision, recall)

def get_list(cur_list, size):
    arrays = np.arange(size)
    next_array = set(arrays) - set(cur_list)
    return list(next_array)

def find_label(fname):
    data = json.loads(open(fname, 'r').readline())
    article = np.array(data['clean_article'][:MAX_SENTENCE])
    summary = get_string(data['clean_summary']).lower()
    unigram_summary = compute_dictionary(summary)
    temp_result = []
    for idx in range(len(article)):
        cur_id = idx
        global_best = None
        ids = [cur_id]
        while (True):
            cur_score = {}
            next_list = get_list(ids, len(article))
            if len(next_list) == 0:
                if global_best is not None and len(temp_result) == 0:
                    temp_result.append(global_best)
                break
            for idy in next_list:
                cur_range = np.array(ids + [idy])
                score = get_score(cur_range, article, unigram_summary)
                cur_score[cur_range.tostring()] = score
            # sort by value 
            cur_best = sorted(cur_score, key=cur_score.get, reverse=True)[0]
            cur_best_array = np.fromstring(cur_best, dtype=int)
            if global_best is None:
                global_best = (cur_best_array, cur_score[cur_best])
                ids = list(cur_best_array)
            else:
                if global_best[1] > cur_score[cur_best]: #stop
                    temp_result.append(global_best)
                    break
                else:
                    global_best = (cur_best_array, cur_score[cur_best])
                    ids = list(cur_best_array)
    try:
        data['extractive_summary'] = sorted(temp_result, key=lambda tup: tup[1], reverse=True)[0][0].tolist()
    except:
        assert (len(article) == 1)
        data['extractive_summary'] = [0]
    return data

def proceed(source_path, num_thread):
    target_path = source_path.replace('*', '')
    files = glob.glob(source_path)

    size = int(math.ceil(1.0*len(files)/num_thread))
    processes = list()
    def run_thread(files):
        for f in files:
            data = find_label(f)
            with(open(target_path + f.split('/')[-1], 'w')) as json_file:
                json.dump(data, json_file)
    for i in range(num_thread):
        start = i * size
        end = start + size
        if end > len(files):
            end = len(files)
        p = files[start:end]
        process = Process(target=run_thread, args=(p,))
        process.start()
        processes.append(process)
        if end == len(files):
            break
    for process in processes:
        process.join()


THREADS = 20
source_path = 'data/clean/'
print("Working on All Files, Wait for 10-15 mins")
proceed(source_path+'train/*', THREADS)
proceed(source_path+'test/*', THREADS)
proceed(source_path+'dev/*', THREADS)


