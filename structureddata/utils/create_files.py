import click
import re

@click.command()
@click.option('--dir_path', help='Path to [extraction]/files/raw_file.list!')
@click.option('--extraction', help='Example: 2021-12')
def main(dir_path, extraction):
    """Create files on folder /files.
        Initially run command "ls -R /5_data_per_format > raw_file.list" to obtain list of files.
    """
    paths = []
    paths_per_extractor = {}

    # Collect paths
    file_path = '{}/files/raw_file.list'.format(dir_path)
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if re.match('^dpef\.', line):
                line_values = line.split('.')
                if line_values[1] not in  paths_per_extractor:
                    paths_per_extractor[line_values[1]] = []

                full_path = 'http://data.dws.informatik.uni-mannheim.de/structureddata/{}/quads/{}'.format(extraction, line)
                paths.append(full_path)
                paths_per_extractor[line_values[1]].append(full_path)

    # Write results to files - General
    output_file_path ='{}/files/file.list'.format(dir_path)
    with open(output_file_path, 'w') as file:
        for path in paths:
            file.write(path)

    # Write results to files - Per extractor
    for extractor in paths_per_extractor:
        output_file_path = '{}/files/{}.list'.format(dir_path, extractor)
        with open(output_file_path, 'w') as file:
            for path in paths_per_extractor[extractor]:
                file.write(path)

if __name__ == '__main__':
    main()