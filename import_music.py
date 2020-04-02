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
    1: ""
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
            instrument = instrument_map[int(items[3])]
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
