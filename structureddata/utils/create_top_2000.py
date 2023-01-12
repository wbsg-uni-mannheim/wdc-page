
import gzip
import itertools
from tqdm import tqdm


def create_top_files():
    #formats = ['html-embedded-jsonld', 'html-microdata', 'html-rdfa']
    formats = ['html-rdfa']
    types = ['class', 'prop', 'vocab']
    for format, type in tqdm(list(itertools.product(formats, types))):
        # Input Files
        input = '/ceph/alebrink/WDC_Extraction_2022/6_stats_per_format/{}/{}.stats.gz'.format(format, type)
        output = '/ceph/alebrink/WDC_Extraction_2022/6_stats_per_format/{}/TOP2000_{}.stats.csv'.format(format, type)
        # Create empty output file
        out_f = open(output, "w")
        #f.close()
        with gzip.open(input, 'rb') as f:
            counter = 0
            for line in f:
                #print(line.decode('utf-8'))
                out_f.write(line.decode('utf-8'))
                counter += 1
                if counter > 2000:
                    break

        out_f.close()


def stats_per_format():
    #formats = ['html-embedded-jsonld', 'html-microdata', 'html-rdfa']
    formats = ['html-rdfa']
    types = ['class']
    for format, type in list(itertools.product(formats, types)):
        # Input Files
        input = '/ceph/alebrink/WDC_Extraction_2022/6_stats_per_format/{}/{}.stats.gz'.format(format, type)
        # f.close()
        stats = {'domains': 0, 'urls': 0, 'triples': 0}
        with gzip.open(input, 'rb') as f:
            for line in tqdm(f):
                split_values = line.decode('utf-8').replace('\n', '').split('\t')
                if split_values[0] != 'class':
                    try:
                        stats['domains'] += int(split_values[-3])
                        stats['urls'] += int(split_values[-2])
                        stats['triples'] += int(split_values[-1])
                    except:
                        print("No able to parse: {}".format(line.decode('utf-8')))


        print('Format: {} Domains: {} URLs: {} Triples: {}'.format(format, stats['domains'], stats['urls'], stats['triples']))

create_top_files()
stats_per_format()
