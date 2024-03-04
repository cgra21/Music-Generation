from torch.utils.data import Dataset
import numpy as np
import utils
import music21 as ms
import torch

class MIDIDataset(Dataset):

    def __init__(self, midi_files, vocab, transform = None):
        """
        Arguments:
            midi_files(list): List of paths to MIDI files
            transform: transformation for data
        """
        self.midi_files = midi_files
        self.transform = transform
        self.tokenizer = utils
        self.vocab = vocab

    def _tokens_to_indices(self, tokens):
        return [self.vocab[token] if token in self.vocab else self.vocab["<unk>"] for token in tokens]

    def __len__(self):
        return len(self.midi_files)

    def __getitem__(self, idx):
        midi_path = self.midi_files[idx]
        # Load and tokenize the MIDI file
        score = ms.converter.parse(midi_path)
        tokens = self.tokenizer.tokenize(score).split()
        tokens = self._tokens_to_indices(tokens)
        if self.transform:
            tokens = self.transform(tokens)
        input_sequence = tokens[:-1]
        target_sequence = tokens[1:]
        return torch.tensor(input_sequence, dtype=torch.long), torch.tensor(target_sequence, dtype=torch.long)