import json
import sys
import io
import base64
from copy import deepcopy

def color_by_name(name):
  return {"black": [0,0,0],
    "red": [255, 0, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255]}.get(name, None)

def color_from_node(node, base_color = None):
  if node is None:
    return None

  color = color_by_name(node.get("color")) or deepcopy(base_color)

  if color is None:
    color = color_by_name("black")

  color[0] = color[0] + int(node.get("r", 0))
  color[1] = color[1] + int(node.get("g", 0))
  color[2] = color[2] + int(node.get("b", 0))

  return color

def buildFileForLeds(led_count, uncompressed_json, base_filename):
  compressed_frames = []

  for frame in uncompressed_json["frames"]:
      base_color = color_from_node(frame)
      uncompressed_cells = frame.get("cells", [])
      frame_data = bytearray()

      for node_count in range(0, led_count):
        node_color = deepcopy(base_color)

        if node_count < len(uncompressed_cells):
          cell_node = uncompressed_cells[node_count]

          node_color = color_from_node(cell_node, base_color)

        if node_color is None or len(node_color) != 3:
          print("Cannot determine color for frame {0} node {1}".format(frame, node_count))
          return

        # print("F: {0}".format(base_color))

        frame_data.extend(node_color)

      encoded_data = base64.b64encode(frame_data).decode()

      # print("{0} bytes in frame data - {1}".format(len(frame_data), encoded_data))

      compressed_frame = {"f": encoded_data}

      compressed_frames.append(compressed_frame)

  marker_location = base_filename.find("#")

  if marker_location == -1:
    marker_location = 0
  else:
    marker_location = marker_location + 1 #Remove the trailing hash

  output_filename = "{0}-{1}.c".format(led_count, base_filename[marker_location:])

  with open(output_filename, "w") as compressed_file:
    compressed_file.write(json.dumps(compressed_frames))
    print("{0} - {1} frames convered for {2} leds".format(output_filename, len(compressed_frames), led_count) )

supported_led_counts = [8, 12, 16, 24]

def convert(filename):
  with open(filename) as uncompressed_file:
    uncompressed_json = json.load(uncompressed_file)

    led_counts = []

    exact_led_count = uncompressed_json.get("leds")

    if exact_led_count is not None:
      led_counts.append(exact_led_count)
    else:
      led_minimum = uncompressed_json.get("ledMin", 8)
      led_maximum = uncompressed_json.get("ledMax", 24)

      led_counts = [x for x in supported_led_counts if x >= led_minimum and x <= led_maximum]

    print("Generating patterns for leds: {0}".format(led_counts))

    for led_count in led_counts:
      buildFileForLeds(led_count, uncompressed_json, filename)

if len(sys.argv) != 2:
  print(sys.argv)
  print("Usage: {0} uncompressed_json_file".format(sys.argv[0]))
else:
  convert(sys.argv[1])