import vk_api
from requests import post
import time
import json
import sys
from random import choice

with open('config.json', 'r') as f:
    config = json.load(f)

vk = vk_api.VkApi(token=config['token']).get_api()

name = 'd3adluvv?'

file = {'file1': open('7.jpg', 'rb'),
'file2': open('6.jpg', 'rb'),
'file3': open('5.jpg', 'rb'),
'file4': open('4.jpg', 'rb'),
'file5': open('3.jpg', 'rb'),
'file6': open('2.jpg', 'rb'), }

def upload() -> dict:
    with open('config.json', 'r') as f:
        config = json.load(f)
    url:str = vk.photos.getUploadServer(album_id=config['albumId'])['upload_url']
    r = post(url, files=file).json()
    return r

def newAlbum() -> int:
    
    noFullAlbums = [i['id'] for i in vk.photos.getAlbums()['items'] if i['size'] < 10000]
    if not noFullAlbums:

        albumId = vk.photos.createAlbum(title=name)['id']
        return albumId
    else:
        return choice(noFullAlbums)
try:
    r = upload()
    phlist, hash, server, album = r['photos_list'], r['hash'], r['server'], r['aid']
except vk_api.exceptions.VkApiError as e:
    if "This album is full" in e.error['error_msg']:
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['albumId'] = newAlbum()
        with open('config.json', 'w') as f:
            json.dump(config, f, indent = 4)
        r = upload()
        phlist, hash, server, album = r['photos_list'], r['hash'], r['server'], r['aid']


while True:
    try:
        vk.photos.save(album_id=album, hash=hash, server=server, photos_list = phlist)
        print(time.time(), ' Uploaded. Photo count: ', vk.photos.getAll()['count'])
    except vk_api.exceptions.VkApiError as e:
        if "This album is full" in e.error['error_msg']:
            with open('config.json', 'r') as f:
                config = json.load(f)
            config['albumId'] = newAlbum()
            with open('config.json', 'w') as f:
                json.dump(config, f, indent = 4)
            r = upload()
            phlist, hash, server, album = r['photos_list'], r['hash'], r['server'], r['aid']
        elif 'Unknown error occurred' in e.error['error_msg'] or 'Flood control' in e.error['error_msg']:
            print('sleeping 300s', e.error['error_msg'])
            time.sleep(300)
            continue

