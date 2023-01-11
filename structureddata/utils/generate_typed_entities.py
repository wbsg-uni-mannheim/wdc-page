import gzip
import logging
from tqdm import tqdm

import click


@click.command()
@click.option('--dir_path', help='Path to [extraction]/3_wdcurlstats and [extraction]/6_stats_per_format!')
@click.option('--extraction', help='ID of extraction. Example: 2021-12')
def main(dir_path, extraction):
    """Create extractor tables for stats.html"""
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    order = ['html-microdata', 'html-embedded-jsonld', 'html-mf-hcard','html-rdfa', 'html-mf-xfn','html-mf-adr','html-mf-geo',
             'html-mf-hcalendar','html-mf-hreview',
             'html-mf-hlisting','html-mf-hrecipe', 'html-mf2-h-adr','html-mf-hresume','html-mf-species']

    typed_entity_counts = {}

    for extractor in tqdm(order):
        file_path = '{}/6_stats_per_format/{}/class.stats.gz'.format(dir_path, extractor)
        with gzip.open(file_path, 'rb') as f:
            typed_entity_counts[extractor] = 0
            for line in f:
                line_values = line.decode('utf-8').split('\t')
                if line_values[0] != 'class':
                    #print(line_values)
                    typed_entity_counts[extractor] += int(line_values[-3])

    sum_typed_entities_counts = sum(typed_entity_counts.values())
    typed_entity_counts['overall'] = sum_typed_entities_counts

    with open('{}/typed_entities.csv'.format(dir_path), 'w') as file:
        for key in typed_entity_counts:
            file.write('{}\t{}\n'.format(key, typed_entity_counts[key]))

if __name__ == '__main__':
    main()