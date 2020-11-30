import sys
import os
import hashlib
import struct
import subprocess
import collections
import tensorflow as tf
import json, glob

from tensorflow.core.example import example_pb2

VOCAB_SIZE = 200000
CHUNK_SIZE = 1000 # num examples per chunk, for the chunked data
SENTENCE_START = '<s>'
SENTENCE_END = '</s>'
main_path = 'data/clean/'
data_path = 'data/pointer_generator/'
os.mkdir(data_path)
chunks_dir = data_path + 'finished_files/'

def chunk_file(set_name):
    in_file = data_path+'%s.bin' % set_name
    reader = open(in_file, "rb")
    chunk = 0
    finished = False
    while not finished:
        chunk_fname = os.path.join(chunks_dir, '%s_%03d.bin' % (set_name, chunk)) # new chunk
        with open(chunk_fname, 'wb') as writer:
            for _ in range(CHUNK_SIZE):
                len_bytes = reader.read(8)
                if not len_bytes:
                    finished = True
                    break
                str_len = struct.unpack('q', len_bytes)[0]
                example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
                writer.write(struct.pack('q', str_len))
                writer.write(struct.pack('%ds' % str_len, example_str))
            chunk += 1

def get_string(sentences, is_article=True):
    all_sentence = []
    for sentence in sentences:
        all_sentence.append(' '.join(sentence))
    if is_article:
        return ' '.join(all_sentence).lower()
    else:
        return ' '.join(["%s %s %s" % (SENTENCE_START, sent, SENTENCE_END) for sent in all_sentence]).lower()

def chunk_all():
    # Make a dir to hold the chunks
    if not os.path.isdir(chunks_dir):
        os.mkdir(chunks_dir)
    # Chunk the data
    for set_name in ['train', 'val', 'test']:
    # for set_name in ['val', 'test']:
        print ("Splitting %s data into chunks..." % set_name)
        chunk_file(set_name)
    print ("Saved chunked data in %s" % chunks_dir)


def write_to_bin(in_folder, out_file, makevocab=False):
    if makevocab:
        vocab_counter = collections.Counter()
    files = glob.glob(in_folder)
    counter = 0
    
    with open(out_file, 'wb') as writer:
        for file in files:
            data = json.loads(open(file, 'r').readline())
            article = get_string(data['clean_article'])
            abstract = get_string(data['clean_summary'], is_article=False)
            
            # Write to tf.Example
            tf_example = example_pb2.Example()
            tf_example.features.feature['article'].bytes_list.value.extend([article.encode()])
            tf_example.features.feature['abstract'].bytes_list.value.extend([abstract.encode()])
            tf_example_str = tf_example.SerializeToString()
            str_len = len(tf_example_str)
            writer.write(struct.pack('q', str_len))
            writer.write(struct.pack('%ds' % str_len, tf_example_str))
            
            # Write the vocab to file, if applicable
            if makevocab:
                art_tokens = article.split(' ')
                abs_tokens = abstract.split(' ')
                abs_tokens = [t for t in abs_tokens if t not in [SENTENCE_START, SENTENCE_END]] # remove these tags from vocab
                tokens = art_tokens + abs_tokens
                tokens = [t.strip() for t in tokens] # strip
                tokens = [t for t in tokens if t!=""] # remove empty
                vocab_counter.update(tokens)

    print ("Finished writing file %s" % out_file)

    # write vocab to file
    if makevocab:
        print ("Writing vocab file...")
        with open(data_path+"vocab", 'w') as writer:
            for word, count in vocab_counter.most_common(VOCAB_SIZE):
                writer.write(word + ' ' + str(count) + '\n')
        print ("Finished writing vocab file")


write_to_bin(main_path+'train/*', data_path+'train.bin', makevocab=True)
write_to_bin(main_path+'dev/*', data_path+'val.bin')
write_to_bin(main_path+'test/*', data_path+'test.bin')
chunk_all()
