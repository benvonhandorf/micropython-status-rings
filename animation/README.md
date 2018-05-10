## Animations ##

This directory contains source code for animations.  They are run through the `convert_animation.py` utility to create compressed JSON files for consumption by the status light.

### Design Goals ###

This syntax is designed to try and account for a few different goals:
* Establish a consise syntax for simple animations
* Allow flexibility for different numbers of LEDs, where the same animation may vary across different status lights
* Be fairly concise and low-impact on the status light

#### Animation Selection ####

Animation files all end in `.json.c`.

Animations will be selected by the device based on the following process:
* If there is a file that begins with the number of LEDs in the ring and followed by the animation name desired, it will be used.  For example, if the status light has 8 LEDs and is trying to load animation `foo`, `8-foo.json.c` will be checked first.
* If there is a file that matches the animation name, it will be used.  For example, a status ring with any number of LEDs will look for a `foo.json.c` if it cannot find a more applicable file.

### Basic syntax ###

#### Frames ####
Animations are defined in JSON files, containing arrays of frames.
```
{
  "frames": [
  	...
  ]
}
```

Each individual frame can specify the color for all LEDs in the ring, like so:
```
{
  "color": "black"
},
```

or like so:
```
{
  "r": 0,
  "g": 0,
  "b": 0
},
```

#### Cells ####

The frame of animation can also specify the color of individual cells in the animation frame.  It need not specify all cells, particularly if the Frame has already specified a color and only needs to override some of the cells.

Thus the following frame fills the entire ring with red and then overrides the first two cells with green:
```
{
  "color": "red",
  "cells": [
    {
      "color": "green"
    },
    {
      "color": "green"
    }
  ]
}
```

### Supported Color names ###

The following colors are supported by name:

* "black": [0,0,0]
* "red": [255, 0, 0]
* "green": [0, 255, 0]
* "blue": [0, 0, 255]

### LED Counts ###

To help match the animation selection process above, uncompressed JSON file names are parsed to produce multiple files for different LED counts.  

For example, an uncompressed file named which contains a `leds` member set to 8 will result in a compressed animation file of `8-foo.json.c`.  However, a file that contains both an `ledMin` of 8 and `ledMax` of 12 will create both an `8-foo.json.c` and a `12-foo.json.c`, since it claims to contain support for both 8 and 12 led rings.

The LED counts supported are defined in `convert_animation.py` and are currently 8, 12, 16 and 24 LED.  Anything within the `ledMin` - `ledMax` range will be generated, so a file with an `ledMin` of 8 and an `ledMax` of 24 will generate 4 files.