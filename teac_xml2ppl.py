#!/usr/bin/env python

__author__ = 'weidongxu'

import os
import os.path
import argparse
import plistlib
import urllib.parse
import codecs
import unicodedata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='?', default=os.getcwd())
    args = parser.parse_args()

    xml_file_list = collect_files_in_directory(args.directory)
    ppl_file_list = []
    for file_name in xml_file_list:
        print('process xml file: ' + file_name)
        with open(file_name, 'rb') as f:
            content = plistlib.load(f)
            pl = content['Playlists'][0]['Playlist Items']
            tracks = content['Tracks']
            ppl_content = convert_to_ppl(pl, tracks)
            ppl_file_list.append((file_name.replace('.xml', '.ppl'), ppl_content))
    for file_name, content in ppl_file_list:
        print('write ppl file: ' + file_name)
        with codecs.open(file_name, 'w', 'utf-8-sig') as f:
            f.write(content)
#    for file_name in xml_file_list:
#        print('delete xml file: ' + file_name)
#        os.remove(file_name)


def collect_files_in_directory(directory):
    ext = 'xml'
    ret_file_list = []
    for dir_name, subdir_list, file_list in os.walk(directory):
        for file_name in file_list:
            if file_name.lower().endswith('.' + ext) and not os.path.basename(file_name).startswith('._'):
                ret_file_list.append(os.path.join(dir_name, file_name))
    return ret_file_list


def convert_to_ppl(pl, tracks):
    ppl_content = ''
    for p in pl:
        track_id = p['Track ID']
        track = tracks[str(track_id)]

        # convert mac path to windows path
        mac_location = urllib.parse.unquote(track['Location'])[7:]
        mac_dirs = []
        (head, tail) = os.path.split(mac_location)
        while head:
            (head, tail2) = os.path.split(head)
            if tail2 == 'Volumes':
                break
            else:
                mac_dirs.append(tail)
                tail = tail2
        mac_dirs.reverse()
        location = os.path.join('D:', *mac_dirs).replace('/', '\\')
        # NFC (precomposed unicode)
        location = unicodedata.normalize('NFC', location)

        name = track['Name']
        artist = track['Artist']
        duration = track['Optional Duration Time']
        # best guess, duration seems to be in 10millisecond in xml
        ppl_duration = int(duration * 3 / 4)
        # no idea what 4 means
        ppl_line = '"{location}",4,"{name}","{artist}",{num1},0,{num2}'\
            .format(location = location, name = name, artist = artist, num1 = ppl_duration + 1, num2 = ppl_duration)
        ppl_content += ppl_line
        ppl_content += '\n'
    return ppl_content


if __name__ == '__main__':
    main()
