from os import listdir
import click
import logging
from top_domains import generate_top_domain_rows


@click.command()
@click.option('--cc_extraction', help='Month and year of Common crawl extraction. Example: November 2020')
@click.option('--dir_path', help='Path to [extraction]/3_wdcurlstats!')
@click.option('--output_dir', help='Path to [extraction]/stats!')
def main(cc_extraction, dir_path, output_dir):
    """Create top domain by extracted triples html pages"""
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    html_head = None
    with open('utils/top_domains_head.html', 'r') as html_head_file:
        html_head = html_head_file.readlines()



    for f in listdir(dir_path):
        if 'domaintriple.stats' in f:

            extractor = f.replace('.domaintriple.stats', '')
            extractor = extractor.replace('html-', '')

            if 'mf' in extractor:
                extractor_long = extractor.replace('mf-', 'Microformats ')
            else:
                extractor_long = extractor

            logging.info('Start to generate HTML page for extractor {}'.format(extractor))

            output_path = '{}/top_domains_by_extracted_triples_for_extractor_html-{}.html'.format(output_dir, extractor)
            with open(output_path, 'w') as output_file:
                output_file.writelines(html_head)
                output_file.write('<body><a name=\'top\'></a><h1>Top Domains by Extracted Triples for Extractor {}</h1>\n'.format(extractor_long))

                output_file.write('<br /><a href="stats.html">Back to Statistics</a><br /><br />\n')
                output_file.write('<p>This page contains the list of top domains using ')
                output_file.write(extractor)
                output_file.write(' of the extraction of {} of the <a target="_blank" href="http://webdatacommons.org">Web Data Commons</a> project.'.format(cc_extraction))
                output_file.write('The page shows the top domains employing {} within their websites, ordered by the number of triples found in the crawl corpus.</p><br />\n'.format(extractor_long))

                output_file.write('<ol>\n')

                file_path = '{}/{}'.format(dir_path, f)
                rows = generate_top_domain_rows(file_path, 'triples', 1000)

                for row in rows:
                    output_file.write('{}\n'.format(row) )
                output_file.write('</ol></body> \n</html>')

                logging.info('Generated HTML page for extractor {}'.format(extractor))


if __name__ == '__main__':
    main()