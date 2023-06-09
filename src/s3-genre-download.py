#!/usr/bin/env python3

import os
import boto3
import re
import mimetypes

from boto3.s3.transfer import TransferConfig
s3 = boto3.resource('s3')
config = TransferConfig(multipart_threshold=64 * 1024 * 1024)

scratchfile = '/tmp/scratchfile'

srcname = 'licenselounge-audiolab'
src = s3.Bucket(srcname)

def key_exists(key, section):
    results = s3.meta.client.list_objects_v2(Bucket=section, Prefix=key)
    return 'Contents' in results

files = [ ".*.mp3" ]
pats = {}

for f in files:
    pats[f] = re.compile(f'jake/blues/{f}')

for o in src.objects.all():
    for f in files:
        m = pats[f].match(o.key)
        if m is not None:
            print(f'*Found: {o.key}')
            filename = scratchfile + "/" + o.key
            os.makedirs(os.path.split(scratchfile + "/" + o.key)[0], exist_ok=True)
            s3.Object(srcname, o.key).download_file(filename, Config=config)
