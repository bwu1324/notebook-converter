# Notebook Converter

Scripts for merging and converting jupyter notebooks to html/pdf and generating table of contents

## Getting Started

### Prerequisites

* Python 3 (Tested with 3.11)

### Building the Scripts

1. Install dependencies by running:
    ```shell
    pip install -r requirements.txt
    ```

2. Run [pyinstaller](https://pyinstaller.org/) to generate executables
    ```shell
    pyinstaller ./merge_nb.py --onefile
    ```
    ```shell
    pyinstaller ./nb2pdf.py --onefile
    ```

3. Executables can now be found in the `dist` folder. Run with the `--help` flag for usage

