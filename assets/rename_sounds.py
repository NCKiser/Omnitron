import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("instrument")
parser.add_argument("starting_note")
args = parser.parse_args()

# https://onlinesequencer.net/1417680

print(args.instrument, args.starting_note)
input_location = os.path.join(args.instrument,"output")
print(input_location)

names = ['c2', 'cs2', 'd2', 'ds2', 'e2', 'f2', 'fs2', 'g2', 'gs2', 'a2', 'as2', 'b2',
         'c3', 'cs3', 'd3', 'ds3', 'e3', 'f3', 'fs3', 'g3', 'gs3', 'a3', 'as3', 'b3',
         'c4', 'cs4', 'd4', 'ds4', 'e4', 'f4', 'fs4', 'g4', 'gs4', 'a4', 'as4', 'b4',
         'c5', 'cs5', 'd5', 'ds5', 'e5', 'f5', 'fs5', 'g5', 'gs5', 'a5', 'as5', 'b5',
         'c6', 'cs6', 'd6', 'ds6', 'e6', 'f6', 'fs6', 'g6', 'gs6', 'a6', 'as6', 'b6',
         'c7', 'cs7', 'd7', 'ds7', 'e7', 'f7', 'fs7', 'g7', 'gs7', 'a7', 'as7', 'b7',]
name_index = names.index(args.starting_note)
print(name_index)
file_list = os.listdir(os.path.join(args.instrument,"output"))
for name in file_list:
    file_list[file_list.index(name)] = name.split('.')[0]
file_list.sort(key=int)
for filename in file_list:
    source = os.path.join(args.instrument, "output", filename+".wav")
    destination = os.path.join(args.instrument, names[name_index]+".wav")
    print(source+"   "+destination)
    os.rename(source, destination)
    name_index = name_index + 1