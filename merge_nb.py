import os
import re
import pickle
import argparse
import glob as glob
import nbformat as nbf
from nb2pdf import nb2pdf, nb2pdf_args
from yaspin import yaspin

class merge_args:
    def __init__(
        self,
        config_file='',
        input_pattern=r'**/*.ipynb',
        output_file='merged.ipynb',
        no_gen_toc=False,
        toc_title='Table of Contents',
        toc_header_pattern=r'# ',
        toc_subheader_pattern=r"## ",
        save_config=None
    ):
        self.config_file = config_file
        self.input_pattern = input_pattern
        self.output_file = output_file
        self.no_gen_toc = no_gen_toc
        self.toc_title = toc_title
        self.toc_header_pattern = toc_header_pattern
        self.toc_subheader_pattern = toc_subheader_pattern
        self.save_config = save_config
    config_file: str
    input_pattern: str
    output_file: str
    no_gen_toc: bool
    toc_title: str
    toc_header_pattern: str
    toc_subheader_pattern: str
    save_config: str


# Initial link id
link_id_counter = 0


def get_merge_args(parser: argparse.ArgumentParser) -> merge_args:
    parser.add_argument(
        'config_file',
        nargs='?',
        help='Configuration file'
    )
    parser.add_argument(
        '--input_pattern',
        default=merge_args().input_pattern,
        help='The glob filename pattern of jupyter notebooks to merge'
    )
    parser.add_argument(
        '--output_file',
        default=merge_args().output_file,
        help='The output filename of merged jupyter notebook'
    )
    parser.add_argument(
        '--no_gen_toc',
        action='store_true',
        help='Don\'t generate table of contents in merged file'
    )
    parser.add_argument(
        '--toc_title',
        default=merge_args().toc_title,
        help='Title of table of contents in merged file'
    )
    parser.add_argument(
        '--toc_header_pattern', '--toc_hp',
        default=merge_args().toc_header_pattern,
        help='Regex pattern to match for table of content headers'
    )
    parser.add_argument(
        '--toc_subheader_pattern', '--toc_sp',
        default=merge_args().toc_subheader_pattern,
        help='Regex pattern to match for table of content subheaders'
    )
    parser.add_argument(
        '--save_config',
        default=merge_args().save_config,
        help='Location to save configuration to. Should not be used with config_file argument'

    )
    return parser.parse_args()


def getNewLinkId():
    global link_id_counter
    link_id_counter += 1
    return link_id_counter


def check_non_ascii(str: str):
    for line in str.splitlines():
        try:
            line.encode('utf-8').decode('ascii')
        except:
            print("Warning! Non-ASCII character found in following line. These characters may not be rendered correctly")
            print(line)


def main(args: merge_args):
    merged = nbf.v4.new_notebook()
    if (not args.no_gen_toc):
        merged['cells'].append(nbf.v4.new_markdown_cell(''))
    toc = '# ' + args.toc_title

    for file in sorted(glob.glob(args.input_pattern)):
        if (os.path.normpath(file) == os.path.normpath(args.output_file)):
            continue
        print(f'Working on: {file}')
        toc = readFile(args, file, merged, toc)

    if (not args.no_gen_toc):
        merged['cells'][0]['source'] = toc

    # Create notebook
    with yaspin(text='Generating Notebook'):
        if (os.path.dirname(args.output_file) != ''):
            os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
        with open(args.output_file, 'w', encoding='utf-8') as f:
            nbf.write(nbf.validator.normalize(merged)[1], f)
    
    nb2pdf(nb2pdf_args(args.output_file, False, True))


def appendCells(args: merge_args, cells: list, merged: nbf.NotebookNode, toc: str):
    if (len(merged['cells']) > 0):
        merged['cells'].append(
            nbf.v4.new_markdown_cell(
                '<hr/>\n<p style="page-break-after:always;"></p>')
        )

    for cell in cells:
        check_non_ascii(cell['source'])
        if (cell['cell_type'].lower() == 'markdown'):
            match = re.match(args.toc_subheader_pattern, cell['source'])
            if (match):
                source = cell['source'].splitlines()
                sub_header = source[0].replace(match.group(), '')

                index = getNewLinkId()
                toc += f'\n\t* [{sub_header}](#{index})'
                source[0] += f'<a class="anchor" id="{index}"></a>'
                merged['cells'].append(
                    nbf.v4.new_markdown_cell('\n'.join(source))
                )
            else:
                merged['cells'].append(
                    nbf.v4.new_markdown_cell(cell['source'])
                )

        if (cell['cell_type'].lower() == 'code'):
            new_cell = nbf.v4.new_code_cell(cell['source'])
            new_cell['outputs'] = cell['outputs']
            merged['cells'].append(new_cell)

        if (cell['cell_type'].lower() == 'raw'):
            merged['cells'].append(
                nbf.v4.new_raw_cell(cell['source'])
            )

    return toc


def readFile(args: merge_args, file: os.PathLike, merged: nbf.NotebookNode, toc: str) -> str:
    nb = nbf.read(file, as_version=4)
    if (len(nb['cells']) == 0):
        print('No cells found, ignoring')
        return toc

    match = re.match(args.toc_header_pattern, nb['cells'][0]['source'])
    if (match == None):
        print('No matching header found, ignoring file')
        return toc

    index = getNewLinkId()
    title = nb['cells'][0]['source'].replace(match.group(), '')
    toc += f'\n* **[{title}](#{index})**'
    nb['cells'][0]['source'] += f'<a class="anchor" id="{index}"></a>'

    toc = appendCells(args, nb['cells'], merged, toc)
    merged['metadata'] = nb['metadata']
    return toc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='merge_nb',
        description='Merges a set of jupyter notebooks '
    )
    args = get_merge_args(parser)
    if (args.save_config):
        with open(args.save_config, 'wb') as f:
            args.save_config = None
            pickle.dump(args, f)

    if (args.config_file):
        with open(args.config_file, 'rb') as f:
            args = pickle.load(f)
    
    main(args)
