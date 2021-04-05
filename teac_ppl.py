#!/usr/bin/env python

__author__ = 'weidongxu'

import os
import os.path
import argparse
import math
from tinytag import TinyTag
from typing import List


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directories', nargs='+', default=os.getcwd())
    parser.add_argument('--playlist', nargs='?', default=None)
    args = parser.parse_args()

    playlist_filename = args.playlist

    file_list = []
    directories = args.directories
    for directory in directories:
        file_list.extend(collect_files_in_directory(directory))

    if not playlist_filename:
        if len(directories) == 1:
            playlist_filename = f'A] {os.path.basename(directories[0])}.ppl'
        else:
            playlist_filename = 'playlist.ppl'

    item_list = []
    for filename in file_list:
        tag = TinyTag.get(filename)
        length = int(math.ceil(tag.duration * 75))

        print(f'file "{filename}", title "{tag.title}", artist "{tag.artist}", length {length}')

        escaped_filename = filename.replace('"', '""')
        escaped_title = tag.title.replace('"', '""')
        escaped_artist = tag.artist.replace('"', '""')

        item = f'"{escaped_filename}",4,"{escaped_title}","{escaped_artist}",{length},0,{length-1}\n'
        item_list.append(item)

    with open(playlist_filename, 'w', encoding='utf-8') as f:
        f.writelines(item_list)


def collect_files_in_directory(directory : str) -> List[str]:
    ext = 'flac'
    ret_file_list = []
    for dir_name, subdir_list, file_list in os.walk(directory):
        for file_name in file_list:
            if file_name.lower().endswith('.' + ext) and not os.path.basename(file_name).startswith('._'):
                ret_file_list.append(os.path.join(dir_name, file_name))
    return ret_file_list


if __name__ == '__main__':
    main()
