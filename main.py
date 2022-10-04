import csv
acceptable_modes = ["Analog/analog", "Analog", "DMR", "DMR/analog"]

schema = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
"""


def placemark(name, desc, coords):
    return f"""
    <Placemark>
      <name>{name}</name>
      <description>{desc}</description>
      <Point>
        <coordinates>{coords}</coordinates>
      </Point>
    </Placemark>"""
    

def gen_name(line):
  call = line["\ufeffCall"]
  mode = line["Mode"]
  if mode in acceptable_modes[:2]:
    band = " 70cm"
    if float(line["Output Freq"]) < 440:
      band = "2m"
    return f"{call} {band}"
  elif mode in acceptable_modes[2:]:
    mode = "DMR"

  return f"{call} {mode}"


def gen_desc(line):
    output = line["Output Freq"]
    input = line["Input Freq"]
    uplink_tone = line["Uplink Tone"]
    downlink_tone = line["Downlink Tone"]
    mode = line["Mode"]
    last_update = line["Last Update"]

    return f"rx: {output}, tx: {input}, ^{uplink_tone}Hz, {mode}, {last_update}"


def gen_coords(line):
  return f"{line['Long']}, {line['Lat']}, 0"


with open("Georgia Repeaters All.csv", 'r') as file:
    repeaters = csv.DictReader(file)

    for line in repeaters:
        if line["Mode"] not in acceptable_modes:
          continue

        name = gen_name(line)
        
        desc = gen_desc(line) 

        coords = gen_coords(line)

        schema += placemark(name, desc, coords)
        

schema += """
  </Document>
</kml>
"""
print(schema)
