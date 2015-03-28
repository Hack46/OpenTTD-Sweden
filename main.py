# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from glob import iglob
import pandas as pd
import numpy as np
import os
import png


XSCALE = 766
YSCALE = 2048
OUTFILE = 'test_3.png'


def process_map(file_name):
    print('Processing {0}...'.format(file_name))
    return pd.read_csv(file_name, names=['x', 'y', 'z'], sep=' ', decimal=',')


def process_files(base_dir):
    base_glob = os.path.join(base_dir, '*.xyz')
    frames = [process_map(file_name) for file_name in iglob(base_glob)]
    df_f = pd.concat(frames)
    return df_f


if __name__ == '__main__':
    # Download and unzip file from 'http://www.myndighetsdata.se/download/lantmateriet-hdb-50m.zip' and set path below.
    df = process_files('/Users/matthias/Downloads/lantmateriet-hdb-50m')
    df['xcat'] = pd.cut(df.x, XSCALE, labels=range(XSCALE))
    df['ycat'] = pd.cut(df.y, YSCALE, labels=range(YSCALE))
    group = df.groupby(['xcat', 'ycat'])
    df1 = pd.DataFrame(group.z.mean())
    max_z = df1.z.max()
    df1['new_z'] = np.round(df1.z / max_z * 255)
    dz = df1.new_z.unstack().fillna(0).transpose()
    w = png.Writer(XSCALE, YSCALE, greyscale=True)
    with open(OUTFILE, 'wb') as f:
        w.write(f, reversed(dz.values.tolist()))
