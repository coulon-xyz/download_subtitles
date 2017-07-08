#!/usr/local/bin/python
#-*- coding: utf-8 -*

import hashlib
import os
import requests
import click

@click.group()
@click.option('--debug', '-d', is_flag=True, help="Display debug logs to console")
def cli(debug):
    pass


@click.command()
@click.option('--input', '-i', required=True, help="input file")
@click.option('--language', '-l', default="en", help="Display dataframes to screen using matplotlib")
def download(input, language):
    """
    download subs
    """
    subs = get_subs(input)
    if subs:
        sub_file_name = input[:-3] + "srt"
        sub_file = open(sub_file_name, "w")
        sub_file.write(subs)
        sub_file.close()


def get_hash(file_name):
    # this hash function receives the name of the file and returns the hash code
    readsize = 64 * 1024
    with open(file_name, 'rb') as f:
        size = os.path.getsize(file_name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def get_subs(file_name):
    file_hash = get_hash(file_name)
    api_url = "http://api.thesubdb.com/"
    url = api_url + "?action=download&hash=" + file_hash + "&language=en"
    headers = {'user-agent': "SubDB/1.0 (Pyrrot/0.1; http://github.com/jrhames/pyrrot-cli)"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.content
    raise Exception("status_code :" + str(r.status_code))

cli.add_command(download)

if __name__ == "__main__":
    cli()
