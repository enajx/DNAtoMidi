#!/usr/bin/env python
import csv
from midiutil import MIDIFile
import random
import sys
import argparse
from time import time

def formatDNAFile(rawFile):

    with open(rawFile) as myfile:
        data=myfile.read().replace('\n', '')

    split_sequence = [data[i:i+3] for i in range(0, len(data)-1, 3)]

    return split_sequence


def textToPitches(dnaText, startingPitch):
    degrees = []
    speeds = []
    # notesInKey = [0,2,4,5,7,9,11,12,14,16,17,19,21,23,24,26]
    # notesInKey = [0,2,4,5,7,9,10,19,12,14,17,8,21,16,11,24] #increased key pattern
    notesInKey = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]


    start_codon =      ['ATG']
    # start_codons =      ['ATG', 'GTG', 'TTG']
    stop_codons =       ['TAA', 'TAG', 'TGA']

    condonsList = [['ATT', 'ATC', 'ATA',],
    ['CTT', 'CTC', 'CTA', 'CTG', 'TTA', 'TTG',],
    ['GTT', 'GTC', 'GTA', 'GTG',],
    ['TTT', 'TTC',],
    ['ATG',],
    ['TGT', 'TGC',],
    ['GCT', 'GCC', 'GCA', 'GCG',],
    ['GGT', 'GGC', 'GGA', 'GGG',],
    ['CCT', 'CCC', 'CCA', 'CCG',],
    ['ACT', 'ACC', 'ACA', 'ACG',],
    ['TCT', 'TCC', 'TCA', 'TCG','AGT', 'AGC',],
    ['TAT', 'CCC', 'CCA', 'CCG',],
    ['CCT', 'TAC',],
    ['TGG',],
    ['CAA', 'CAG',],
    ['AAT', 'AAC',],
    ['CAT', 'CAC',],
    ['GAA', 'GAG',],
    ['GAT', 'GAC',],
    ['AAA', 'AAG',],
    ['CGT', 'CGC', 'CGA', 'AGA', 'AGG']]

    possibleNumAcidCombos = int(len(condonsList))

    counter = 0
    for codon_read in dnaText:
        for i in range(0, 20):
                for codon in condonsList[i]:
                    if codon_read == codon:
                        counter += 1
                        pitch = startingPitch + notesInKey[i]


        duration = random.choice([0.5, 1, 1.5, 2])
        # to-do: parametrise the duration depending on the quality of the read in case the input format is fastq

        degrees.append(pitch)
        speeds.append(duration)

    print("\nInput sequence contains", len(dnaText), "codons""\n")
    print(counter, "enconding codons have been found in the input sequence\n")

    return degrees, speeds

def randomTriples(startingPitch): #determines which triples to be used after some half notes
    notes = random.choice([[0,2,0], [0,7,0],
                  [0,4,7], [4,0,4],
                  [0,2,0]])
    x = []
    for i in range(len(notes)):
        x.append([notes[i]+startingPitch, (1/3)])
    return x

def connectNotes(pitch1, difference):
     #stored as [pitch, length]
     x = []
     blank = []
     ###NINTHS###
     ninth1 = [[pitch1+12, .25], [pitch1+7, .25], [pitch1+4, .25], [pitch1, .25]]
     ninth2 = [[pitch1+16, (1/3)], [pitch1+12, (1/3)], [pitch1+7, (1/3)]]
     ninth3 = [[pitch1+12, (1/3)], [pitch1+19, (1/3)], [pitch1+5, (1/3)]]
     ninth4 = [[pitch1+10, (1/3)], [pitch1+9, (1/3)], [pitch1+2, (1/3)]]

     invertNinth1 = [[pitch1-12, .25], [pitch1-7, .25], [pitch1-4, .25], [pitch1, .25]]
     invertNinth2 = [[pitch1-16, (1/3)], [pitch1-12, (1/3)], [pitch1-7, (1/3)]]
     invertNinth3 = [[pitch1-12, (1/3)], [pitch1-19, (1/3)], [pitch1-5, (1/3)]]
     invertNinth4 = [[pitch1-10, (1/3)], [pitch1-9, (1/3)], [pitch1-2, (1/3)]]

     #up a ninth
     if difference == 14:
         x = random.choice([ninth1, ninth2, ninth3, ninth4, blank])

     #down a ninth
     if difference == -14:
         x = random.choice([invertNinth1, invertNinth2, invertNinth3, invertNinth4, blank])

     ###TENTHS###
     tenth1 = [[pitch1+14, (1/3)], [pitch1+10, (1/3)], [pitch1+7, (1/3)]]
     tenth2 = [[pitch1+17, .25], [pitch1+14, .25], [pitch1+12, .25], [pitch1+7, .25]]
     tenth3 = [[pitch1+5, (1/3)], [pitch1+9, (1/3)], [pitch1, (1/3)]]
     tenth4 = [[pitch1+11, .25], [pitch1+12, .25], [pitch1+14, .25], [pitch1+16, .25],
               [pitch1+17, .25], [pitch1+14, .25], [pitch1+12, .25], [pitch1+7, .25]]

     invertTenth1 = [[pitch1-14, (1/3)], [pitch1-10, (1/3)], [pitch1-7, (1/3)]]
     invertTenth2 = [[pitch1-17, .25], [pitch1-14, .25], [pitch1-12, .25], [pitch1-7, .25]]
     invertTenth3 = [[pitch1-5, (1/3)], [pitch1-9, (1/3)], [pitch1, (1/3)]]
     invertTenth4 = [[pitch1-11, .25], [pitch1-12, .25], [pitch1-14, .25], [pitch1-16, .25],
                     [pitch1-17, .25], [pitch1-14, .25], [pitch1-12, .25], [pitch1-7, .25]]
     #up a tenth
     if difference == 16:
         x = random.choice([tenth1, tenth2, tenth3, tenth4, blank])

     #down a tenth
     if difference == -16:
         x = random.choice([invertTenth1, invertTenth2, invertTenth3, invertTenth4, blank])

     ###ELEVENTHS###
     eleventh1 = [[pitch1+12, (1/3)], [pitch1+10, (1/3)], [pitch1+5, (1/3)]]
     eleventh2 = [[pitch1+16, .25], [pitch1+12, .25], [pitch1+9, .25], [pitch1+5, .25]]
     eleventh3 = [[pitch1+15, (1/3)], [pitch1+9, (1/3)], [pitch1+3, (1/3)]]

     invertEleventh1 = [[pitch1-12, (1/3)], [pitch1-10, (1/3)], [pitch1-5, (1/3)]]
     invertEleventh2 = [[pitch1-16, .25], [pitch1-12, .25], [pitch1-9, .25], [pitch1-5, .25]]
     invertEleventh3 = [[pitch1-15, (1/3)], [pitch1-9, (1/3)], [pitch1-3, (1/3)]]

     #up an eleventh
     if difference == 17:
         x = random.choice([eleventh1, eleventh2, eleventh3, blank])

     #down an eleventh
     if difference == -17:
         x = random.choice([invertEleventh1, invertEleventh2, invertEleventh3, blank])

     ###TWELVES###
     twelves1 = [[pitch1+19, (1/3)], [pitch1+19, (1/3)], [pitch1+19, (1/3)]]
     twelves2 = [[pitch1+24, (1/3)], [pitch1+16, (1/3)], [pitch1+7, (1/3)]]
     twelves3 = [[pitch1+17, .25], [pitch1+14, .25], [pitch1+10, .25], [pitch1+7, .25]]

     invertTwelves1 = [[pitch1-19, (1/3)], [pitch1-19, (1/3)], [pitch1-19, (1/3)]]
     invertTwelves2 = [[pitch1-24, (1/3)], [pitch1-16, (1/3)], [pitch1-7, (1/3)]]
     invertTwelves3 = [[pitch1-17, .25], [pitch1-14, .25], [pitch1-10, .25], [pitch1-7, .25]]

     #up a twelth
     if difference == 19:
         x = random.choice([twelves1, twelves2, twelves3, blank])

     #down a twelth
     if difference == -19:
         x = random.choice([invertTwelves1, invertTwelves2, invertTwelves3, blank])

     ###THIRTEENS###
     thirt1 = [[pitch1+16, (1/3)], [pitch1+13, (1/3)], [pitch1+9, (1/3)]]
     thirt2 = [[pitch1+17, .25], [pitch1+16, .25], [pitch1+12, .25], [pitch1+5, .25]]
     thirt3 = [[pitch1+22, (1/3)], [pitch1+17, (1/3)], [pitch1+10, (1/3)]]

     invertThirt1 = [[pitch1-16, (1/3)], [pitch1-13, (1/3)], [pitch1-9, (1/3)]]
     invertThirt2 = [[pitch1-17, .25], [pitch1-16, .25], [pitch1-12, .25], [pitch1-5, .25]]
     invertThirt3 = [[pitch1-22, (1/3)], [pitch1-17, (1/3)], [pitch1-10, (1/3)]]

     #up a thirteenth
     if difference == 21:
         x = random.choice([thirt1, thirt2, thirt3, blank])

     #down a thirteenth
     if difference == -21:
         x = random.choice([invertThirt1, invertThirt2, invertThirt3, blank])

     ###FOURTEENTHS###
     fourt1 = [[pitch1+21, (1/3)], [pitch1+16, (1/3)], [pitch1+12, (1/3)]]
     fourt2 = [[pitch1+17, .25], [pitch1+12, .25], [pitch1+5, .25], [pitch1+12, .25]]

     invertFourt1 = [[pitch1-21, (1/3)], [pitch1-16, (1/3)], [pitch1-12, (1/3)]]
     invertFourt2 = [[pitch1-17, .25], [pitch1-12, .25], [pitch1-5, .25], [pitch1-12, .25]]

     #up a fourteenth
     if difference == 23:
         x = random.choice([fourt1, fourt2, blank])

     #down a fourteenth
     if difference == -23:
         x = random.choice([invertFourt1, invertFourt2, blank])


     ##fifteen, double octave

     return x

##still needs a lot of work
##should append the new ones in the right spots
def findDifference(pitches, speeds, startingPitch):
    lastPitch = 0
    for i, pitch in enumerate(pitches):
        differenceInPitch = pitch - lastPitch
        newNotes = connectNotes(pitch-differenceInPitch, differenceInPitch)
        if len(newNotes) != 0:
            newNotePitches, newNoteLengths = zip(*newNotes)
            for x in range(len(newNotePitches)):
                pitches.insert(i, newNotePitches[x])
                speeds.insert(i, newNoteLengths[x])
        lastPitch = pitch
    return pitches, speeds

def sixthTurnaround(pitches, speeds, startingPitch):
    newPitches = pitches[:]
    newSpeeds = speeds[:]

    for i in range(len(pitches)):
        if (pitches[i] - startingPitch == 8) and (speeds[i] != (1/3)):
            newPitches.insert(i+1, pitches[i]-4)
            newSpeeds.insert(i, 1)
            newPitches.insert(i+1, pitches[i]-1)
            newSpeeds.insert(i, .5)
    return newPitches, newSpeeds

def afterSomeHalfs(pitches, speeds, startingPitch):
    lastNoteLength = 0
    for i in range(len(pitches)):
        if speeds[i] == 2 and (pitches[i] - startingPitch in [0, 7, 12, 19]) and (lastNoteLength != (1/3)):
            x = randomTriples(startingPitch)
            newNotePitches, newNoteLengths = zip(*x)
            for a in range(len(newNotePitches)):
                pitches.insert(i+1, newNotePitches[a])
                speeds.insert(i+1, newNoteLengths[a])
        lastNoteLength = speeds[i]
    return pitches, speeds

def start():

    startingPitch = args.startingnote
    track    = args.track
    channel  = args.channel
    tempo    = args.tempo
    volume   = args.velocity
    time     = args.time
    duration = args.duration


    formattedForInsert = formatDNAFile(args.sequence_file)
    myDegrees, mySpeeds = textToPitches(formattedForInsert, startingPitch)
    myDegrees, mySpeeds = findDifference(myDegrees, mySpeeds, startingPitch)
    myDegrees, mySpeeds = sixthTurnaround(myDegrees, mySpeeds, startingPitch)
    myDegrees, mySpeeds = afterSomeHalfs(myDegrees, mySpeeds, startingPitch)

    MyMIDI = MIDIFile(1, adjust_origin = True)  # One track
    MyMIDI.addTempo(track, time, tempo)
    currentTime = time
    for i, pitch in enumerate(myDegrees):
        MyMIDI.addNote(track, channel, pitch, currentTime, mySpeeds[i], volume)
        currentTime = currentTime+mySpeeds[i]

    with open("DNAmusic_" + timestamp + ".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
    description='''Example of run: python --sequence_File my_dna.txt . ''',
    epilog="""That's all.""")

    # Parse input options
    parser.add_argument('--sequence_file', type=str,
                        help='the dna sequence in a txt file, ie. my_dna.txt')

    parser.add_argument('--format', type=str,
                        default='txt',
                        help='the encoding of the data file: txt or fastq')

    parser.add_argument('--tempo', type=int,
                        default=120,
                        help='the tempo of the midi file (BPM), default value 120')

    parser.add_argument('--track', type=int,
                        default=0,
                        help='midi track, default value 0')

    parser.add_argument('--channel', type=int,
                        default=0,
                        help='midi channel, default value 0')

    parser.add_argument('--velocity', type=int,
                        default=100,
                        help='velocity of the notes (0-127), default value 100')

    parser.add_argument('--startingnote', type=int,
                        default=60,
                        help='Starting note ( 5 -> 127 or F-2 -> G8 ), default value 60 (C4 or middle C)')

    parser.add_argument('--time', type=int,
                        default=0,
                        help='?   # In beats')

    parser.add_argument('--duration', type=int,
                        default=0,
                        help='?   # In beats')


    args = parser.parse_args()

    timestamp = str(int(time()))

    start()
