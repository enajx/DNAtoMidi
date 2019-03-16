# DNAtoMidi
Convert DNA sequences to Midi sequences
<p align="center"> 
<img src="CodonstoAminoacides.svg" width="600">
</p>

### How to run

You need to have the DNA sequence that you want to use in a txt file, eg. DNA_sequence.txt and the run the command:

```
python3 DNAtomidi.py --sequence_file DNA_sequence.txt
```

To see all the other options:

```
python3 DNAtomidi.py --help
```

### Some theory

The DNA is made of 4 letters A, G, T and C representing the four DNA nucleotides. Three letters together are called [codons](https://en.wikipedia.org/wiki/Codon_(disambiguation)) and can encode one amino acid which are the building blocks of proteins. Although 64 3-letters combination are possible, there are only 20 amino acids found in nature; the same amino-acid may be coded by different condons. The image above shows the 20 amino acids and their encoding codons.

In a simplify model, some codons code the start/stop instructions for the transcription process.


### Further implementations

- [ ] \(Optional) Better notesInKey list
- [ ] \(Optional) Add different mapping modes (current and straight 0->20 notes )
- [ ] \(Optional) Implement start/stop condons
- [ ] \(Optional) Allow fastq as an input format and use quality value to map velocity

