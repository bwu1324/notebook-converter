import os
import time
import nbformat as nbf
from nbconvert import HTMLExporter
from playwright.sync_api import sync_playwright
from yaspin import yaspin


class nb2pdf_args:
    def __init__(
        self,
        notebook: os.PathLike,
        save_html=False,
        no_save_pdf=False
    ):
        self.notebook = notebook
        self.save_html = save_html
        self.no_save_pdf = no_save_pdf
    notebook: os.PathLike
    save_html: bool
    no_save_pdf: bool


def nb2pdf(args: nb2pdf_args):
    directory = os.path.dirname(os.path.abspath(args.notebook))
    filename, _ = os.path.splitext(os.path.basename(args.notebook))
    if (args.save_html):
        html_output = os.path.join(directory, filename + '.html')
    else:
        html_output = os.path.join(directory, 'TEMP-' + filename + '.html')
    pdf_output = os.path.join(directory, filename + '.pdf')

    # Read notebook
    nb = nbf.read(args.notebook, as_version=4)

    # Create HTML
    if (args.save_html):
        print('Generating HTML')

    exporter = HTMLExporter()
    html_data, _ = exporter.from_notebook_node(nb)
    html_data = html_data.replace('<head>', '''
<head>
<style>
    .jp-InputPrompt {
        display: none !important;
    }

    .jp-Notebook-cell {
        break-inside: avoid !important;
    }
</style>
<script type="text/x-mathjax-config">
    MathJax.Hub.Queue(function () {
        document.getElementById('mathjax-loading-indicator').style.display = 'none';
    });
</script>
''')
    html_data = html_data.replace('<main>', '''
<main>
<div style="width: 100%; background-color: red; color: white; font-size: 12px; padding: 5px;" id="mathjax-loading-indicator">MathJax Is Loading...</div>
''')

    with open(html_output, "w") as f:
        f.write(html_data)
    if (args.save_html):
        print(f'HTML File saved at {html_output}')

    # Create PDF
    if (not args.no_save_pdf):
        with yaspin(text='Generating PDF') as spinner:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f'file://{html_output}')
                page.wait_for_selector('id=mathjax-loading-indicator', state="hidden")
                page.emulate_media(media="screen")
                page.pdf(path=pdf_output)
                browser.close()
        print(f'PDF saved at {pdf_output}')

    # Remove temporary html file
    if (not args.save_html):
        os.unlink(html_output)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='nb2pdf',
        description='Converts jupyter notebooks to html/pdf'
    )
    parser.add_argument('notebook')
    parser.add_argument(
        '--save_html', '--html',
        help='Save HTML version of notebook',
        action='store_true',
    )
    parser.add_argument(
        '--no_save_pdf',  '--no_pdf',
        help='Save pdf version of notebook',
        action='store_true',
    )
    args = parser.parse_args()
    nb2pdf(args)
