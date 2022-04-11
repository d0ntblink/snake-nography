# snake-nography User Manual
## Gary. K
### 4/11/2022

[Github Link](https://github.com/d0ntblink/snake-nography)

## Setup

### Required Python Libraries

*  opencv-python
*  math **included**
*  logging **included**
*  numpy
*  argparse **included**
  
to install all the required libraries
`pip install numpy opencv-python`

### Required Programs

* somesort of a shell
* python3

## Notes

***This program will only work lossless image fromats as the cover image such as bitmap.***

***the output format needs to match the orginal secret image format.***

***the cover image needs to be at least 8 times bigger in pixel count in both the height and width***

## Help
```
usage: snake-nography.py [-h] [-x <key>] [-d] (-c <secret image> <cover image> <output> | -r <target file> <output>)

This program hides images into other images in lossless format.

options:
  -h, --help            show this help message and exit
  -x <key>, --xcrypt <key>
                        Decrypts or encrypts image using a XOR formula
  -d, --debug           Enables debug mode
  -c <secret image> <cover image> <output>, --cloak <secret image> <cover image> <output>
                        Cloaks an image in another image
  -r <target file> <output>, --reveal <target file> <output>
                        Reveals an image hidden by this program
PS C:\Users\d0ntblink\OneDrive\Projects\snake-nography> 

```

## Examples

```
python3 snake-nography.py -c luna.bmp view.png output.png
python3 snake-nography.py -c luna.bmp view.png output.png -x "secretpassword"
python3 snake-nography.py -r output.png showmethemoney.bmp -x "secretpassword"
```