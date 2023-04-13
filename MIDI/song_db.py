import pandas as pd
import sqlite3
from traceback import print_exc as pe
import os
import glob
import numpy as np

sqlite3.register_adapter(np.int64, lambda val: int(val))

def Connect():
    conn = sqlite3.connect('midi.db')
    curs = conn.cursor()
    curs.execute("PRAGMA foreign_keys=ON;")
    return conn, curs

