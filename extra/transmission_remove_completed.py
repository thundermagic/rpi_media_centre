# requirement: transmission-clutch
# A sloppy script to delete torrents and data from transmission that are completed and are not seeding anymore
from clutch.core import Client

transmission_host = '192.168.4.4'
client = Client(host=transmission_host)

torrents_list = client.list()

percent_downloaded = client.torrent.percent_done()
finished_torrents = []
for torrent_id, v in percent_downloaded.items():
    if v == 1:  # 1 means its 100% downloaded
        # status of 0 means its stopped, 6: seeding, 4: downloading, 3: download pending
        if torrents_list[torrent_id]['status'] == 0:
            # remove local data
            print('removing torrent: {0}'.format(torrents_list[torrent_id]['name']))
            user_input = input('remove torrent: {0}? Proceed: y/n'.format(torrents_list[torrent_id]['name']))
            if user_input == 'y':
                client.torrent.remove(ids=torrent_id, delete_local_data=True)
                print('torrent: {0} removed'.format(torrents_list[torrent_id]['name']))
            print()
