import music21 as ms
from music21 import note, pitch, chord
from torchtext.vocab import vocab
from collections import Counter, OrderedDict
import os
from pathlib import Path

class MusicManager:
    '''Class built to help manage music objects and turn them into tokens for processing
    
        Needs to be able to handle and create vocab for multiple music objects'''
    
    def __init__(self):
        self.scores = {} # List containing music21.Score objects for each inputted song
        self.vocab = None # Vocabulary object created from scores

    @staticmethod
    def configure():
        "configure MuseScore to show music"
        ms.configure.run()
        return

    # This method will be used for adding texts to a score list
    def add_song(self, score_path, name = None) -> str:
        '''Input: music21 Score
        Output: a string representation

        Usage: This function will convert a music21 Score object into a string of text, where each note is represented as :
        n[MIDI_PITCH] d[DURATION]

        When notes are played at the same offset, they will be one after another. If notes are played at different offset  
        values they will be seperated by a "xxsep" token. This is represented as:
        xxsep d[ELEMENT_OFFSET - LAST_OFFSET]'''
        
        score = ms.converter.parse(score_path)
        
        output = []
        last_offset = 0
        last_duration = 0
        # in order to get duration for xxsep token, we need to get offset between currently played note and prev
        for element in score.recurse().stream().notesAndRests:
            if isinstance(element, (note.Note, chord.Chord, note.Rest)):
                if element.offset != last_offset:
                    output.append(f'xxsep d{element.offset - last_offset}')
                    
                if isinstance(element, chord.Chord):
                    # For chords, handle each note in the chord
                    for n in element.notes:
                        midi_pitch = n.pitch.midi
                        dur = n.duration.quarterLength
                        output.append(f'n{midi_pitch} d{dur}')
                        
                elif isinstance(element, note.Note):
                    midi_pitch = element.pitch.midi
                    dur = element.duration.quarterLength * 4
                    output.append(f'n{midi_pitch} d{dur}')
                else:
                    # For rests, just update the duration
                    dur = element.duration.quarterLength * 4
                    output.append(f'n0 d{dur}')
                    
                # Update the last note's offset and duration
                last_offset = element.offset
                last_duration = dur
        
        output.append('xxeos')
        # Join the sequence into a single string
        output_text = ' '.join(output)

        # Check if user inputted name, if so use it
        if name is not None:
            if name not in self.scores:
                self.scores[name] = {'score': score,
                                     'string': output_text}
            else:
                raise ValueError(f'{name} already exists in the scores')
        # if no user inputted name, use filename        
        else:
            name = Path(score_path).stem
            if name not in self.scores:
                self.scores[name] = {'score': score,
                                     'string': output_text}
            else:
                raise ValueError(f'{name} already exists in the scores')
        return 

    def tokenize(self) -> list[str]:
        '''Input: music21 Score
        Output: a list of "tokens"

        Usage: This function will convert a music21 Score object into a string of text, where each note is represented as :
        n[MIDI_PITCH] d[DURATION]

        When notes are played at the same offset, they will be one after another. If notes are played at different offset  
        values they will be seperated by a "xxsep" token. This is represented as:
        xxsep d[ELEMENT_OFFSET - LAST_OFFSET]

        This is just a version of textify, but with split
        '''
        return 


    def musicify(self, tokens):
        '''Convert a set of tokens into a music21.Score

        This will be created after passing in our sequence to our transformer model. The basic output is a set of probability based on a list of vocab. The next token in the sequence being the highest probability. The conversion from probability to tokens will be handled by pytorch itself, however we will handle tokens to music.

        Our generated tokens should take the form 
        n[PITCH_VALUE] d[DURATION] 
        but it is possible they don't, so we need to handle the chance they don't occur in that order.

        Usage:

        Input:
            A list of tokens

        Output:
            A music21 Score object
        '''
        pass

    def create_vocab(self):
        pass

