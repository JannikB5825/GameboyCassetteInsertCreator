<h1 align="center">Gameboy Cassette Insert Creator</h1>
<p align="center">Creates an J-Card inserts for Gameboy Games</p>

![Demo](/docs/demo.gif)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Usage

### Image insertion

The programm can insert images onto the Template. All images that are imported have to be given horizontal aligned, since the programm automaticly flips the spine and backcover. While the programm tries to fit the background color of the insert, by finding the edge color of the cover image

### Dimensions

The program automaticly makes the images fit to the smallest dimension of the section. As Example: If a cover with a higher resulution than the template is, is inserted the program automaticly scales the image down to fit the width of the cover without changing its proportions. Following are the different dimensions of the template parts if you want to design your cover images yourself:

- Cover: 650x837
- Spine: 127x749
- Backcover: 253x1030

### Presets

The program comes preloaded with the the diffrent style of Gameboy System Box: Gameboy, Gameboy Color, Gameboy Advance. When changing these presets with the dropdown menu the banner on the cover and the spine will change to the system selected. Also the publisher on the bottom of the spine can be changed with dropdown menu next to it. By Selecting "Select File" a costom file can be used and fill be fitted to the needed dimensions.

### Output

The program can output either PNGs or PDFs. The PDFs are formattet for A4 paper and formated ready for printing, which means that the insert is inserted into the PDF at the right dimension.