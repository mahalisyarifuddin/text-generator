# text-generator

Test text generator, simplified.

## Introduction

This repository is an enhanced fork of the [Just Another Test Text Generator](http://justanotherfoundry.com/generator). It allows for the creation of natural-looking dummy text for font testing, using trigram analysis from various language corpora.

This version includes a Google Colab port and a standalone web application for ease of use in modern environments.

## Features

1.  **Corpus to Trigrams Conversion**: Convert any text into the trigram TSV format used by the generator.
2.  **Deterministic Text Generation**: Generate text with fixed random seeds for reproducible results.
3.  **Full Feature Parity**: Supports original letter variety, pair variety, and kerning-based probability adjustments.
4.  **Browser-Based Tool**: Includes `generator.html` for instant text generation in the browser using uploaded TSV files.
5.  **Colab Notebook**: Includes `text_generator.ipynb` for easy cloud-based workflows.

## Technical Details

### Trigram Analysis

The generator uses trigram statistics to predict the next character based on the preceding two. Spaces are represented by the underscore character (`_`).

### Adjustment Factors (Tweaks)

*   **Letter Variety**: Balances letter frequencies for a more even character distribution.
*   **Pair Variety**: Balances the frequency of character pairs.
*   **Word Length Biasing**: Adjusts space probabilities to follow the word length distribution found in the original corpus.
*   **Kerning**: Uses data from `kerning.txt` to shift probabilities based on typical kerning pairs.

## How to Use

### Using Google Colab

Open `text_generator.ipynb` in Google Colab to convert your own corpus text or generate text from existing data.

### Using a Web Browser

Open `generator.html` in any modern browser. Upload a trigram TSV file (found in the `languages/` directory) and click "Generate Text".

### Using Python Scripts

Run the original generator script:
```bash
python3 scripts/generator.py -language en -characters all -kern typ -kernlevel 0 -lettervariety 0 -pairvariety 0 -case normal
```

## License

GNU General Public License v2.0. Based on the original code by Tim Ahrens ([Just Another Foundry](http://justanotherfoundry.com/)).
