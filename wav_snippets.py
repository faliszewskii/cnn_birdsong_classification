import math
import os
import wave
from concurrent.futures import ThreadPoolExecutor


def cut_file(filepath, file_no):
    with wave.open(filepath, 'rb') as wav_file:
        # Get the total number of frames in the file
        num_frames = wav_file.getnframes()
        # Get the frame rate of the file
        frame_rate = wav_file.getframerate()
        # Calculate the total duration of the file in seconds
        duration = num_frames / float(frame_rate)
        # Calculate the number of clips that will be created
        num_clips = int(math.floor(duration / clip_length))
        # Loop through each clip and extract it from the input file
        for i in range(num_clips):
            clip_filename = os.path.join(subdir_output, f"{os.path.splitext(file)[0]}.{i + 1}.wav")
            if os.path.exists(clip_filename):
                continue
            # Calculate the start and end frames for the clip
            start_frame = int(i * clip_length * frame_rate)
            end_frame = min(int((i + 1) * clip_length * frame_rate), num_frames)
            # Read the data for the clip
            wav_file.setpos(start_frame)
            clip_data = wav_file.readframes(end_frame - start_frame)
            # Create a new WAV file for the clip
            with wave.open(clip_filename, 'wb') as clip_file:
                clip_file.setparams(wav_file.getparams())
                clip_file.writeframes(clip_data)
        print("Processed file {}/{}: {}".format(file_no, total_files, subdir))


if __name__ == '__main__':
    # define the input and output directories
    input_dir = "converted"
    output_dir = "snippets"
    # Define the desired clip length in seconds
    clip_length = 3

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
            with ThreadPoolExecutor() as executor:
                executor.submit(cut_file, filepath, processed_files)
                processed_files += 1
