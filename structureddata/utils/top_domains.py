import gzip

import click

@click.command()
@click.option('--dir_path', help='Path to [extraction]/3_wdcurlstats!')
@click.option('--aggregation', help='Aggregation parameter triples/urls')
@click.option('--number_records', help='Number of records', type=int)
@click.option('--file', help='domainurlwtriple.stats.gz or domaintriple.stats.gz')
def main(dir_path, aggregation, number_records, file):
    """Create top domain tables for top domains by urls with triples"""

    file_path = '{}/3_wdcurlstats/{}'.format(dir_path, file)
    rows = generate_top_domain_rows(file_path, aggregation, number_records)
    for row in rows:
        print(row)


def generate_top_domain_rows(file_path, aggregation, number_records):
    rows = []
    with gzip.open(file_path, 'rb') as file:
        counter = 0
        while counter < number_records:
            line_values = file.readline().decode('utf-8').split('\t')
            domain = line_values[0]
            if len(line_values) > 1:
                count = line_values[1]

                row = '<li> <a rel=\'nofollow\' target=\'_blank\' href=\'https://{}\'>{}</a> ({:,} {})</li>'.format(domain, domain, int(count), aggregation)
                rows.append(row)
                counter +=1
            else:
                break

    return rows

if __name__ == '__main__':
    main()