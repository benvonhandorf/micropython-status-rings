import json
import sys
import io
import base64

def color_by_name(name):
  return {"black": [0,0,0],
    "red": [255, 0, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255]}.get(name, None)

def color_from_node(node, base_color = None):
  if node is None:
    return None

  color = color_by_name(node["color"]) or base_color

  if color is None:
    return color

  color[0] = color[0] + int(node.get("r", 0))
  color[1] = color[1] + int(node.get("g", 0))
  color[2] = color[2] + int(node.get("b", 0))

  return color

def convert(filename):
  with open(filename) as uncompressed_file:
    uncompressed_json = json.load(uncompressed_file)

    compressed_frames = []

    led_count = uncompressed_json["leds"]

    for frame in uncompressed_json["frames"]:
      base_color = color_from_node(frame)
      uncompressed_cells = frame.get("cells", [])
      frame_data = bytearray()

      for node_count in range(0, led_count):
        node_color = base_color

        if node_count < len(uncompressed_cells):
          cell_node = uncompressed_cells[node_count]

          node_color = color_from_node(cell_node, base_color)

        if node_color is None or len(node_color) != 3:
          print("Cannot determine color for frame {0} node {1}".format(frame, node_count))
          return

        frame_data.extend(node_color)

      encoded_data = base64.b64encode(frame_data).decode()

      print("{0} bytes in frame data - {1}".format(len(frame_data), encoded_data))

      compressed_frame = {"f": encoded_data}

      print(compressed_frame)

      compressed_frames.append(compressed_frame)

    print(compressed_frames)

    with open(filename + ".compressed", "w") as compressed_file:
      compressed_file.write(json.dumps(compressed_frames))
      print("{0} frames convered for {1} leds".format(len(compressed_frames), led_count) )


if len(sys.argv) != 2:
  print(sys.argv)
  print("Usage: {0} uncompressed_json_file".format(sys.argv[0]))
else:
  convert(sys.argv[1])