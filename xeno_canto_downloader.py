import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import httpx
from tqdm import tqdm

def download_file(url, i, dirname):
    metadata = httpx.head(url).headers['Content-Type']
    ext = 'wav' if metadata == 'audio/wav' else 'mp3'
    filename1 = f"{dirname}.{i}.{ext}"
    if os.path.exists(os.path.join(downloads_dir, dirname, filename1)):
        print(f"Skipping {filename1}")
        return
    # Download the file from the URL
    response = urllib.request.urlopen(url)
    # Save the downloaded file to the directory with the unique filename
    with open(os.path.join(downloads_dir, dirname, filename1), 'wb') as outfile:
        outfile.write(response.read())


if __name__ == '__main__':
    # Set the path to the recordings directory
    recordings_dir = './recordings/'
    # Set the path to the downloads directory
    downloads_dir = './downloads/'
    # Lines number lower threshold
    file_count = 150

    # Loop through all the files in the recordings directory
    progressEnumerable = tqdm(os.listdir(recordings_dir), unit="file")
    for filename in progressEnumerable:
        progressEnumerable.set_description("Downloading %s" % filename)
        # Check if the file is a regular file (i.e., not a directory)
        if os.path.isfile(os.path.join(recordings_dir, filename)):
            # Open the file and read all the lines into a list
            with open(os.path.join(recordings_dir, filename), 'r') as f:
                lines = f.readlines()
            # Check if the file has at least file_count lines
            if len(lines) >= file_count:
                # Loop through each line in the file
                i = 0
                # Create the directory with the same name as the file (without the extension)
                dirname = os.path.splitext(filename)[0]
                os.makedirs(os.path.join(downloads_dir, dirname), exist_ok=True)
                with ThreadPoolExecutor() as executor:
                    # Submit a download task for each URL in the file
                    for line in lines:
                        if i == file_count:
                            break
                        # Strip any whitespace from the line
                        url = line.strip()
                        executor.submit(download_file, url, i, dirname)
                        i += 1
            else:
                print(f"Skipping {filename} because it has less than {file_count} lines")
