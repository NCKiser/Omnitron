import argparse
import csv
import os

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

instrument_map = {
    0: "piano",
    1: ""
}
notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
prev_octave = 0

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
            if int(prev_octave) < int(note[-1]):
                key += 7
                key = key % 8
            output = [time, key, instrument, note, 2]
            output_csv.writerow(output)
            prev_octave = note[-1]
            print(prev_octave)
        except IndexError as e:
            pass
