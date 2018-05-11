import json, io, math

led_count = 12
frames = 20
color_offset = (2 * math.pi) / 3
led_offset = (2 * math.pi) / led_count
half_value = 128

def normalize(value):
  return min(max(int((value * half_value) + half_value), 0), 255)

def red_value(radians, led):
  return normalize(math.sin(radians + (led * led_offset)))
def green_value(radians, led):
  return normalize(math.sin(radians + color_offset + (led * led_offset)))
def blue_value(radians, led):
  return normalize(math.sin(radians + (color_offset * 2) + (led * led_offset)))

frameset = []

for frame in range(0, frames):
  radians =  ( frame / frames ) * 2 * math.pi

  cell_data = []

  for led in range(0, led_count):
    r = red_value(radians, led)
    g = green_value(radians, led)
    b = blue_value(radians, led)

    cell = {'r': r, 'g': g, 'b': b}
    cell_data.append(cell)

  frame_data = {'color':"black", 'cells': cell_data}

  frameset.append(frame_data)

root = {'frames': frameset, 'leds': led_count}

output_filename = "{0}#{1}.json".format(led_count, "rgb_chase")

with open(output_filename, "w") as file:
  file.write(json.dumps(root))