## Animations ##

This directory contains source code for animations.  They are run through the `convert_animation.py` utility to create compressed JSON files for consumption by the status light.

### Design Goals ###

This syntax is designed to try and account for a few different goals:
* Establish a consise syntax for simple animations
* Allow flexibility for different numbers of LEDs, where the same animation may vary across different status lights
* Be fairly concise and low-impact on the status light

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