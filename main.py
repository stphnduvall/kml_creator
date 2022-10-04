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
  mode = get_mode(line)
  if mode == "Analog":
    band = "70cm"
    if float(line["Output Freq"]) < 440:
      band = "2m"
    return f"{call} {band}"

  return f"{call} {mode}"


def get_mode(line):
  mode = "Analog"
  if line["Mode"] in acceptable_modes[2:]:
    mode = "DMR"
  return mode


def gen_desc(line):
    output = line["Output Freq"]
    input = line["Input Freq"]
    last_update = line["Last Update"]

    mode = get_mode(line)
    if mode == "DMR":
      color_code = line["Digital Access"]
      access_protection = f"cc: {color_code}"
    else:
      uplink_tone = line["Uplink Tone"]
      access_protection = f"^{uplink_tone}Hz"
    
    return f"rx: {output}, tx: {input}, {access_protection}, {mode}, {last_update}"


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
