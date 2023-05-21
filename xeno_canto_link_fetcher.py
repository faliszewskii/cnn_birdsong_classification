import requests
import json


if __name__ == '__main__':
    url = 'https://www.xeno-canto.org/api/2/recordings?query=cnt:poland&page=1'
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        num_pages = data['numPages']

        for page in range(1, num_pages+1):
            page_url = f'https://www.xeno-canto.org/api/2/recordings?query=cnt:poland&page={page}'
            page_response = requests.get(page_url)

            if page_response.status_code == 200:
                page_data = json.loads(page_response.text)
                recordings = page_data['recordings']

                for recording in recordings:
                    species = recording['en']
                    if species == "Identity unknown" or species == "Soundscape":
                        continue
                    file_url = recording['file']

                    with open(f'recordings/{species}.txt', 'a') as f:
                        f.write(file_url + '\n')

                print(f'Successfully wrote recordings from page {page} to files.')
            else:
                print(f'Failed to fetch recordings from page {page}.')
    else:
        print('Failed to fetch number of pages.')
