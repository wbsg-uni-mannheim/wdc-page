import pandas as pd
import click

@click.command()
@click.option('--dir_path', help='Path to [extraction]/3_wdcurlstats!')
def main(dir_path):
    """Create general tables and bar charts for stats.html"""
    file_agg_matrix_per_format = '{}\\aggMatrixPerFormat.stats'.format(dir_path)

    df_stats = pd.read_csv(file_agg_matrix_per_format, sep='\t', index_col=0, dtype={'Domains': 'Int64', 'URLs': 'Int64', 'Triples': 'Int64'})
    order = ['html-microdata', 'html-embedded-jsonld', 'html-mf-hcard','html-rdfa', 'html-mf-xfn','html-mf-adr','html-mf-geo','html-mf-hcalendar','html-mf-hreview',
             'html-mf-hlisting','html-mf-hrecipe', 'html-mf2-h-adr','html-mf-hresume','html-mf-species','overall']

    # Create Results per Format
    for value in order:
        row = df_stats.loc[value]

        print('<tr>')
        print('<th>{}</th>'.format(value))
        print('<td align="right">{:,}</td>'.format(row['Domains']))
        print('<td align="right">{:,}</td>'.format(row['URLs']))
        print('<td align="right">{:,}</td>'.format(0))
        print('<td align="right">{:,}</td>'.format(row['Triples']))
        print('</tr>')


    create_bar_charts(df_stats, order, 'Domains')
    create_bar_charts(df_stats, order, 'URLs')

    create_pie_chart(df_stats, 'Triples')


def create_bar_charts(df_stats, order, column):
    print('{} with Triples'.format(column))

    colors = {'html-microdata': '#D11919', 'html-embedded-jsonld': '#29A329', 'html-mf-hcard': '#FFD633',
              'html-rdfa': '#5E8FD8', 'html-mf-xfn': '#FFF5DD', 'html-mf-hcalendar': '#FFDB4D',
              'html-mf-hreview': '#FFEB99'}

    # Create Bar chart - Domain with Triples
    sum_other_values = 0
    for value in order:
        row = df_stats.loc[value]
        if value in colors:
            print('[\'{}\', {}, \'{}\', \'{} : {:,} \'],'.format(value, row[column], colors[value],
                                                                 value.replace('html-', ''), row[column]))

        elif value != 'overall':
            sum_other_values += row['Domains']

    print('[\'{}\', {}, \'{}\', \'{} : {:,} \'],'.format('others', sum_other_values, '#FFE066', 'others',
                                                         sum_other_values))


def create_pie_chart(df_stats, column):
    print('Pie triples - {}'.format(column))

    order = ['html-rdfa', 'html-microdata', 'html-embedded-jsonld', 'html-mf-geo', 'html-mf-hcard', 'html-mf-hcalendar',
             'html-mf-hlisting','html-mf-hresume', 'html-mf-hreview', 'html-mf-species', 'html-mf-hrecipe','html-mf-xfn']

    for value in order:
        row = df_stats.loc[value]

        print('[\'{}\', {}],'.format(value, row[column]))

if __name__ == '__main__':
    main()