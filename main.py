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
    

def description(line):
    output = line["Output Freq"]
    input = line["Input Freq"]
    uplink_tone = line["Uplink Tone"]
    downlink_tone = line["Downlink Tone"]
    mode = line["Mode"]
    last_update = line["Last Update"]

    return f"rx: {output}, tx: {input}, ^{uplink_tone}Hz, {mode}, {last_update}"


with open("Georgia Repeaters All.csv", 'r') as file:
    repeaters = csv.DictReader(file)

    for line in repeaters:
        band = " 70cm"
        if float(line["Output Freq"]) < 440:
            band = " 2m"
        name = line["\ufeffCall"] + band
        if line["Mode"] not in acceptable_modes:
          continue

        name = gen_name(line)
        
        desc = description(line) 

        coords = line['Long'] +", "+ line['Lat'] + ', 0'

        schema += placemark(name, desc, coords)
        

schema += """
  </Document>
</kml>
"""
print(schema)
