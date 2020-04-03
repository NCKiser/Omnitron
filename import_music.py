import argparse
import csv
import os
from math import floor

parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()

print(args.input)
output_file_name = args.input + ".csv"
try:
    os.remove(output_file_name)
except:
    print('output file not overwritten, continuing')
output_file = open(output_file_name, 'w')
output_csv = csv.writer(output_file)

lowest_note = None
highest_note = None

instrument_map = {
    0: "piano",
    8: "grand_piano",
    17: "harpsicord",
    25: "rag_piano",
    26: "music_box",
    19: "xylophone",
    34: "vibraphone",
    21: "steel_drums",
    1: "acoustic_guitar",
    2: "drum_kit",
    31: "electric_drum_kit",
    4: "electric_guitar",
    5: "bass",
    29: "slap_bass",
    32: "jazz_guitar",
    35: "muted_electric_guitar",
    38: "distortion_guitar",
    22: "sitar",
    33: "koto",
    3: "smooth_synth",
    6: "synth_pluck",
    7: "sci-fi",
    13: "sine",
    14: "square",
    15: "sawtooth",
    16: "triangle",
    9: "french_horn",
    10: "trombone",
    11: "violin",
    12: "cello",
    18: "concert harp",
    20: "pizzicato",
    23: "flute",
}
notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
prev_octave = 0
init = True
with open(args.input) as input_file:

    commands = input_file.read().split('|')[-1].split(';')
    for command in commands:
        try:
            items = command.split(' ')
            time = items[0]
            note = items[1].lower().replace('#', 's')
            length = items[2]
            try:
                instrument = instrument_map[int(items[3])]
            except KeyError as e:
                instrument = list(instrument_map.values())[0]
            key = notes.index(note[0])
            octave = int(note[-1])
            output = [time, key, instrument, note, 2]
            output_csv.writerow(output)
            prev_octave = octave
            note_val = octave*10+key
            if note[-1] is 's':
                note_val += .5
            if init or note_val < lowest_note:
                lowest_note = note_val
            if init or note_val > highest_note:
                highest_note = note_val
            init = False
        except IndexError as e:
            pass
print("Import complete")
print(lowest_note, highest_note)
print("Lowest note {}{}".format(notes[floor(lowest_note % 10)], floor(lowest_note/10)))
print("Highest note {}{}".format(notes[floor(highest_note % 10)], floor(highest_note/10)))
