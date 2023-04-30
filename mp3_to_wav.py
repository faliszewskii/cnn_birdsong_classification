import os
from pydub import AudioSegment


if __name__ == '__main__':
    # define the input and output directories
    input_dir = "downloads"
    output_dir = "converted"

    # traverse the directory structure and identify audio files
    total_files = sum(len(files) for _, _, files in os.walk(input_dir))
    processed_files = 0

    # traverse the directory structure and identify audio files
    for subdir, dirs, files in os.walk(input_dir):
        # create the corresponding output subdirectory
        subdir_output = os.path.join(output_dir, os.path.relpath(subdir, input_dir))
        if not os.path.exists(subdir_output):
            os.makedirs(subdir_output)
        for file in files:
            filepath = os.path.join(subdir, file)
            filepath_wav = os.path.join(subdir_output, file[:-3] + "wav")
            if os.path.exists(filepath_wav):
                continue
            if filepath.endswith(".mp3") or filepath.endswith(".wav"):
                # convert mp3 files to wav format
                if filepath.endswith(".mp3"):
                    try:
                        audio = AudioSegment.from_mp3(filepath)
                        audio.export(filepath_wav, format="wav")
                    except Exception as exc:
                        print(f"Exception has occured for {file}")
                        print(type(exc).__name__)
                # copy wav files as is
                else:
                    filepath_copy = os.path.join(subdir_output, file)
                    os.system("cp \"{}\" \"{}\"".format(filepath, filepath_copy))
                # print progress message
                processed_files += 1
                print("Processed file {}/{}: {}".format(processed_files, total_files, filepath))
