import pandas as pd
import click

@click.command()
@click.option('--dir_path', help='Path to [extraction]/3_wdcurlstats!')
@click.option('--aggregation', help='Aggregation parameter triples/urls')
@click.option('--number_records', help='Number of records', type=int)
def main(dir_path, aggregation, number_records):
    """Create top domain tables for top domains by urls with triples"""

    file_path = '{}/domainurlwtriple.stats'.format(dir_path)
    rows = generate_top_domain_rows(file_path, aggregation, number_records)
    for row in rows:
        print(row)


def generate_top_domain_rows(file_path, aggregation, number_records):
    rows = []
    with open(file_path, 'r') as file:
        counter = 0
        while counter < number_records:
            line_values = file.readline().split('\t')
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