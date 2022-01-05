import gzip

import click
import logging

import numpy as np

from top_domains import generate_top_domain_rows
import pandas as pd


@click.command()
@click.option('--dir_path', help='Path to [extraction]/3_wdcurlstats and [extraction]/6_stats_per_format!')
@click.option('--extraction', help='ID of extraction. Example: 2021-12')
def main(dir_path, extraction):
    """Create extractor tables for stats.html"""
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    file_agg_matrix_per_format = '{}\\3_wdcurlstats\\aggMatrixPerFormat.stats'.format(dir_path)
    df_stats = pd.read_csv(file_agg_matrix_per_format, sep='\t', index_col=0, dtype={'Domains': 'Int64', 'URLs': 'Int64', 'Triples': 'Int64'})
    order = ['html-microdata', 'html-embedded-jsonld', 'html-mf-hcard', 'html-rdfa', 'html-mf-xfn','html-mf-adr','html-mf-geo','html-mf-hcalendar','html-mf-hreview',
             'html-mf-hlisting','html-mf-hrecipe','html-mf-hresume','html-mf-species']

    # Load typed_entities.csv
    file_path = '{}\\typed_entities.csv'.format(dir_path)
    typed_entities = {}
    with open(file_path, 'r') as file:
        for line in file.readlines():
            values = line.split(',')
            typed_entities[values[0]] = int(values[1].replace('\\n', ''))

    # Create Results per Format
    for extractor in order:
        row = df_stats.loc[extractor]
        statistics = calc_statistics(row)

        file_path_triples = '{}\\3_wdcurlstats\\{}.domaintriple.stats'.format(dir_path, extractor)
        top_domains_by_triples = generate_top_domain_rows(file_path_triples, 'triples', 20)

        top_class = generate_top_classes_and_properties(extractor, dir_path, 20, 'class')
        top_prop = generate_top_classes_and_properties(extractor, dir_path, 20, 'prop')

        print('')
        generate_table(extractor, statistics, top_domains_by_triples, top_class, top_prop, typed_entities, extraction)


def calc_statistics(row):
    statistics = {'triples': row['Triples'], 'urls': row['URLs'], 'domains': row['Domains']}

    statistics['avg_per_url'] = round(statistics['triples'] / statistics['urls'], 2)
    statistics['avg_per_domain'] = round(statistics['triples'] / statistics['domains'], 2)

    return statistics


def generate_top_classes_and_properties(extractor, dir_path, number_records, type_class_prop):

    # CONTINUE HERE --> no uniform paths
    file_path = '{}\\6_stats_per_format\\{}\\{}.stats'.format(dir_path, extractor, type_class_prop)
    try:
        df_stats = pd.read_csv(file_path, encoding='utf-8', sep='\t', on_bad_lines='warn')
    except FileNotFoundError:
        file_path = '{}.gz'.format(file_path)
        df_stats = pd.read_csv(file_path, encoding='utf-8', sep='\t', compression='gzip', on_bad_lines='warn')

    def generate_rows(selector):
        rows = []
        df_sub_stats = df_stats.sort_values(by=['num{}'.format(selector)], ascending=False)[:number_records]
        for index, row in df_sub_stats.iterrows():
            entity_row = '<li>{} ({:,} {})</li>'.format(row[type_class_prop], round(row['num{}'.format(selector)]),
                                                        selector)
            rows.append(entity_row)

        return rows

    new_rows = {'entity': generate_rows('Entities'), 'domain': generate_rows('Domains')}

    return new_rows


def generate_table(extractor, statistics, top_domains_by_triples, top_class, top_prop, typed_entities, extraction):
    """
    :type extractor: String
    """
    print('	<a id=\'{}\'></a>	'.format(extractor))
    print('	<h3>Extractor {}</h3><br />	'.format(extractor))
    print('	<table>	')
    print('	  <tr>	')
    print('	    <th>Triples Extracted</th>	')
    print('	    <td>{:,}</td>	'.format(statistics['triples']))
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th>URLs with Triples</th>	')
    print('	    <td>{:,}</td>	'.format(statistics['urls']))
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th>Average Triples per URL</th>	')
    print('	    <td>{}</td>	'.format(statistics['avg_per_url']))
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th>Domains with Triples</th>	')
    print('	    <td>{:,}</td>	'.format(statistics['domains']))
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th>Average Triples per Domain</th>	')
    print('	    <td>{:,}</td>	'.format(statistics['avg_per_domain']))
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th>Typed Entities</th>	')
    print('	    <td>{:,}</td>	'.format(typed_entities[extractor]))
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th>Top Domains by Extracted Triples</th>	')
    element_top_domains_by_triples = '{}-top-domains-by-triples-{}'.format(extractor, extraction)
    print('	    <td><small><a href=\'\' onclick="document.getElementById(\'{}\').style.display=\'block\';this.style.display=\'none\';return false;">Show top domains</a></small>	'.format(element_top_domains_by_triples))
    print('	          	')
    print('	      <ol id=\'{}\' style=\'display:none\'>	'.format(element_top_domains_by_triples))
    for domain in top_domains_by_triples:
        print(domain)
    print('	        <li><a href="top_domains_by_extracted_triples_for_extractor_html-microdata.html">More</a></li>	')
    print('	      </ol><br />	')
    print('	    </td>	')
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th>Top Classes</th>	')
    element_top_class_values_by_domain_count = '{}-top-class-values-by-domain-count-{}'.format(extractor, extraction)
    print('	    <td><small><a href=\'\' onclick="document.getElementById(\'{}\').style.display=\'block\';this.style.display=\'none\';return false;">Show top values by domain count</a></small>	'.format(element_top_class_values_by_domain_count))
    print('	      <ol id=\'{}\' style=\'display:none\'>	'.format(element_top_class_values_by_domain_count))
    for top_class_value in top_class['domain']:
        print(top_class_value)
    print('	      </ol><br />	')
    print('	    </td>	')
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th></th>	')
    element_top_class_values_by_entity_count = '{}-top-class-values-by-entity-count-{}'.format(extractor, extraction)
    print('	    <td><small><a href=\'\' onclick="document.getElementById(\'{}\').style.display=\'block\';this.style.display=\'none\';return false;">Show  top values by entity count</a></small>	'.format(element_top_class_values_by_entity_count))
    print('	      <ol id=\'{}\' style=\'display:none\'>	'.format(element_top_class_values_by_entity_count))
    for top_class_value in top_class['entity']:
        print(top_class_value)
    print('	      </ol><br />	')
    print('	    </td>	')
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th>Top Properties</th>	')
    element_top_property_values_by_domain_count = '{}-top-property-values-by-domain-count-{}'.format(extractor, extraction)
    print('	    <td><small><a href=\'\' onclick="document.getElementById(\'{}\').style.display=\'block\';this.style.display=\'none\';return false;">Show top values by domain count</a></small>	'.format(element_top_property_values_by_domain_count))
    print('	      <ol id=\'{}\' style=\'display:none\'>	'.format(element_top_property_values_by_domain_count))
    for top_prop_value in top_prop['domain']:
        print(top_prop_value)
    print('		')
    print('	          </ol>	')
    print('	    </td>	')
    print('	  </tr>	')
    print('	  <tr>	')
    print('	    <th></th>	')
    element_top_property_values_by_entity_count = '{}-top-property-values-by-entity-count-{}'.format(extractor, extraction)
    print('	    <td><small><a href=\'\' onclick="document.getElementById(\'{}\').style.display=\'block\';this.style.display=\'none\';return false;">Show top values by entity count</a></small>	'.format(element_top_property_values_by_entity_count))
    print('	      <ol id=\'{}\' style=\'display:none\'>	'.format(element_top_property_values_by_entity_count))
    for top_prop_value in top_prop['entity']:
        print(top_prop_value)
    print('	      </ol><br />	')
    print('	    </td>	')
    print('	  </tr>	')
    if extractor in ['html-microdata', 'html-embedded-jsonld', 'html-rdfa']:
        print('	  <tr>	')
        print('	    <th>Detailed Statistics as Excel-File</th>	')
        print('	    <td><a target="_blank" href="{}.xlsx">{}.xlsx</a></td>	'.format(extractor, extractor))
        print('	  </tr>	')
    print('	</table>	')


if __name__ == '__main__':
    main()