from fastai.basics import *
from .numpy_encode import *
from .music_transformer import transform
from typing import Collection

BOS = 'xxbos' #Beginning of sequence
PAD = 'xxpad' # padding
EOS = 'xxeos' # End of sequence
MASK = 'xxmask' # Used for BERT masked language modeling. 
CSEQ = 'xxcseq' # Used for Seq2Seq translation - denotes start of chord sequence
MSEQ = 'xxmseq' # Used for Seq2Seq translation - denotes start of melody sequence

# Deprecated tokens. Kept for compatibility 
S2SCLS = 'xxs2scls' # deprecated
NSCLS = 'xxnscls' # deprecated

SEP = 'xxsep' # Used to denote end of timestep (required for polyphony). separator idx = -1 (part of notes)

SPECIAL_TOKS = [BOS, PAD, EOS, S2SCLS, MASK, CSEQ, MSEQ, NSCLS, SEP] # Important: SEP token must be last

NOTE_TOKS = [f'n{i}' for i in range(NOTE_SIZE)] 
# NOTE_SIZE is imported from numpy_encode
DUR_TOKS = [f'd{i}' for i in range(DUR_SIZE)]
# DUR_SIZE is imported from numpy_encode
NOTE_START, NOTE_END = NOTE_TOKS[0], NOTE_TOKS[-1]
DUR_START, DUR_END = DUR_TOKS[0], DUR_TOKS[-1]

MTEMPO_SIZE = 10
MTEMPO_OFF = 'mt0'
MTEMPO_TOKS = [f'mt{i}' for i in range(MTEMPO_SIZE)]

# Vocab - token to index mapping
class MusicVocab():
    "Contain the correspondence between numbers and tokens and numericalize."
    def __init__(self, itos:Collection[str]):
        self.itos = itos
        self.stoi = {v:k for k,v in enumerate(self.itos)}

    def numericalize(self, t:Collection[str]) -> List[int]:
        "Convert a list of tokens `t` to their ids."
        return [self.stoi[w] for w in t]

    def textify(self, nums:Collection[int], sep=' ') -> List[str]:
        "Convert a list of `nums` to their tokens."
        items = [self.itos[i] for i in nums]
        return sep.join(items) if sep is not None else items
    
    def to_music_item(self, idxenc):
        return transform.MusicItem(idxenc, self)
    
    # Note: property decorator creates a "getter" method for these tokens,
    # We can also create a "setter" method with @property_name.setter
    # This means that instead of calling: 
    # MusicVocab.mask_idx() to retrieve our value
    # We can call:
    # MusicVocab.mask_idx instead
    # it allows a level of abstraction, so the user does not have to directly access the private values, which may cause an error
    @property 
    def mask_idx(self): return self.stoi[MASK]
    @property 
    def pad_idx(self): return self.stoi[PAD]
    @property
    def bos_idx(self): return self.stoi[BOS]
    @property
    def sep_idx(self): return self.stoi[SEP]
    @property
    def npenc_range(self): return (self.stoi[SEP], self.stoi[DUR_END]+1)
    @property
    def note_range(self): return self.stoi[NOTE_START], self.stoi[NOTE_END]+1
    @property
    def dur_range(self): return self.stoi[DUR_START], self.stoi[DUR_END]+1

    def is_duration(self, idx): 
        return idx >= self.dur_range[0] and idx < self.dur_range[1]
    def is_duration_or_pad(self, idx):
        return idx == self.pad_idx or self.is_duration(idx)
        
    def __getstate__(self):
        return {'itos':self.itos}

    def __setstate__(self, state:dict):
        self.itos = state['itos']
        self.stoi = {v:k for k,v in enumerate(self.itos)}
        
    def __len__(self): return len(self.itos)

    def save(self, path):
        "Save `self.itos` in `path`"
        pickle.dump(self.itos, open(path, 'wb'))

    @classmethod
    # Note about @classmethod, 
    # This passes a "cls" this isn't "self", this is the class itself, so this will need to be called with a class object
    def create(cls) -> 'Vocab':
        "Create a vocabulary from a set of `tokens`."
        itos = SPECIAL_TOKS + NOTE_TOKS + DUR_TOKS + MTEMPO_TOKS
        # Create a list of index tokens for a new class
        if len(itos)%8 != 0:
            itos = itos + [f'dummy{i}' for i in range(len(itos)%8)]
        # This will create a new object of the class MusicVocab, passing itos, into the class - see __init__
        # This will also result in the creation of a string-to-index dictionary in the class construction as well.
        return cls(itos) 
    
    # Essentially, a classmethod is a method that can instatiate a class object, it allows us to encapsulate a portion of the intial setup, whether that be parsing a string, into the construction of the class
    @classmethod
    def load(cls, path):
        "Load the `Vocab` contained in `path`"
        itos = pickle.load(open(path, 'rb'))
        return cls(itos)