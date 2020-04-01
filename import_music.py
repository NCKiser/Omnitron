import argparse
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()

print(args.input)
output_file_name = args.input + ".csv"
os.remove(output_file_name)
output_file = open(output_file_name, 'w')
output_csv = csv.writer(output_file)

instrument_map = []
notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']


with open(args.input) as input_file:

    commands = input_file.read().split('|')[-1].split(';')
    for command in commands:
        try:
            items = command.split(' ')
            time = items[0]
            note = items[1].lower().replace('#', 's')
            length = items[2]
            instrument = items[3]
            key = notes.index(note[0])
            output = [time, key, 'piano', note, 2]
            output_csv.writerow(output)
        except IndexError as e:
            print(e)

