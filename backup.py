import requests
import json
import logging
from urllib.parse import urlencode


class VKAPIClient:
    base_url_API = 'https://api.vk.com/method'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.131'
        }

    def get_profile_photos(self):
        params = self.get_common_params()
        params.update({
            'owner_id': self.user_id, 
            'album_id': 'profile', 
            'rev': '1',
            'extended': '1',
            'count': 5
        })

        response = requests.get(f'{self.base_url_API}/photos.get', params=params)

        return response.json()

    def get_photos_information(self):      
        photos_information = self.get_profile_photos().get('response', {}).get('items', {})
        photos_list_for_save = []

        for photo_info in photos_information:
            photos_list_for_save.append({
                'date': str(photo_info.get('date', 0)),
                'name': str(photo_info.get('likes', {}).get('count')),
                'url': photo_info.get('sizes', [])[-1].get('url'),
                'size': photo_info.get('sizes', [])[-1].get('type')
            })
        
        for id1, photo_content_1 in enumerate(photos_list_for_save):
            for id2, photo_content_2 in enumerate(photos_list_for_save):
                if id1 == id2:
                    continue

                if photo_content_1['name'] == photo_content_2['name']:
                    photo_content_1['name'] += '_' + photo_content_1['date']
                    photo_content_2['name'] += '_' + photo_content_2['date']
        
        photos_information_for_file = []

        for photo_content in photos_list_for_save:
            photos_information_for_file.append({
                "file_name": f"{photo_content['name']}.jpg",
                "size": photo_content['size']          
            })
        
        return {
            'photos_list_for_save': photos_list_for_save,
            'photos_information_for_file': photos_information_for_file
        }

    def saving_local_photos(self):
        photos_information = self.get_photos_information().get('photos_list_for_save')

        for photo in photos_information:
            file_name = f"{photo['name']}.jpg"
            photo_content = requests.get(photo['url'])

            with open(file_name, 'wb') as f:
                f.write(photo_content.content)
        
    def saving_photos_information_file(self):
        dict = {"data": self.get_photos_information().get('photos_information_for_file')}

        with open('photos_information.json', 'w') as f:            
            json.dump(dict, f, indent = 2)


class YADiskAPIClient:
    base_url_ya_disk = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.token = token
    
    def get_headers(self):
        return {'Authorization': self.token}
    
    def creating_folder(self):
        params = {'path': 'Photos_from_VK'}
        requests.put(self.base_url_ya_disk,
                    params=params,
                    headers=self.get_headers())

    def uploading_photos_to_disk(self):
        with open('photos_information.json', encoding='utf-8') as f:
            data_json = json.load(f)
        
        photos_information  = data_json['data']

        self.creating_folder()

        for photo in photos_information:
            params = {'path': f"Photos_from_VK/{photo['file_name']}"}

            response_1 = requests.get(f'{self.base_url_ya_disk}/upload', 
                        params=params,
                        headers=self.get_headers())
        
            url_for_upload = response_1.json().get('href')
            file_name = photo['file_name']

            with open(file_name, 'rb') as file:
                requests.put(url_for_upload, files={'file':file})


logging.basicConfig(level=logging.INFO, filename="backup_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")