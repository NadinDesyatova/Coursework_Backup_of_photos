import requests
import json
import logging
from urllib.parse import urlencode


class VKAPIClient:
    base_url_API = 'https://api.vk.com/method'

    def __init__(self, token):
        self.token = token

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.131'
        }

    def get_profile_photos(self, user_id):
        params = self.get_common_params()
        params.update({
            'owner_id': user_id, 
            'album_id': 'profile', 
            'rev': '1',
            'extended': '1',
            'count': 5
        })

        response = requests.get(f'{self.base_url_API}/photos.get', params=params)

        return response.json()

    def __get_photos_information(self, user_id):      
        photos_information = self.get_profile_photos(user_id).get('response', {}).get('items', {})
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

    def saving_local_photos(self, user_id):
        photos_information = self.__get_photos_information(user_id).get('photos_list_for_save')

        for photo in photos_information:
            file_name = f"{photo['name']}.jpg"
            photo_content = requests.get(photo['url'])

            with open(file_name, 'wb') as f:
                f.write(photo_content.content)
        
    def saving_photos_information_file(self, file_name, user_id):
        dict = {"data": self.__get_photos_information(user_id).get('photos_information_for_file')}

        json_file_name = f'{file_name}.json'

        with open(json_file_name, 'w') as f:            
            json.dump(dict, f, indent = 2)
        
        return dict['data']


class YADiskAPIClient:
    base_url_ya_disk = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.token = token
    
    def __get_headers(self):
        return {'Authorization': self.token}
    
    def __creating_folder(self, folder_name):
        params = {'path': f'{folder_name}'}
        requests.put(self.base_url_ya_disk,
                    params=params,
                    headers=self.__get_headers())

    def uploading_photos_to_disk(self, folder_name, photos_information):
        self.__creating_folder(folder_name)

        for photo in photos_information:
            params = {'path': f"{folder_name}/{photo['file_name']}"}

            response_1 = requests.get(f'{self.base_url_ya_disk}/upload', 
                        params=params,
                        headers=self.__get_headers())
        
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


if __name__ == '__main__':
    TOKEN_VK = input('Введите токен ВК: ')
    token_ya = input('Введите токен с Полигона Яндекс.Диска.: ')
    current_user_id = input('Введите числовой id пользователя ВК: ')

    vk_client = VKAPIClient(TOKEN_VK)
    vk_client.get_profile_photos(current_user_id)

    vk_client.saving_local_photos(current_user_id)
    data = vk_client.saving_photos_information_file('photos_information', current_user_id)


    ya_client = YADiskAPIClient(token_ya)
    ya_client.uploading_photos_to_disk('Photos_from_VK', data)