# Notebook Converter

Scripts for merging and converting jupyter notebooks to html/pdf and generating table of contents

## Getting Started

### Prerequisites

* Python 3 (Tested with 3.11)

### Building the Scripts

1. Install dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```

2. Install [playwright](https://playwright.dev/) dependency:
    * In Powershell (Windows):
        ```powershell
        $env:PLAYWRIGHT_BROWSERS_PATH="0"
        playwright install chromium
        ```

    * In Bash (Unix):
        ```bash
        PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium
        ```

3. Run [pyinstaller](https://pyinstaller.org/) to generate executables
    ```bash
    pyinstaller notebook_converter.spec
    ```

4. Executables (`merge_nb` and `nb2pdf`) can now be found in the `dist/notebook_converter` folder. Run them with the `--help` flag for usage

