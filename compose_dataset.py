import csv
import os


def compose_dataset(root_dir, target_train_file, target_test_file, train_to_test_ratio, target_classes_file):
    # traverse the directory structure and count the files
    total_files = sum(len(files) for _, _, files in os.walk(root_dir))
    processed_files = 0

    with (
        open(target_train_file, 'w', newline='') as train_csv,
        open(target_test_file, 'w', newline='') as test_csv,
        open(target_classes_file, 'w', newline='') as classes_csv
    ):
        fieldnames = ['path', 'species']
        classes_fieldnames = ['class']
        train_writer = csv.DictWriter(train_csv, fieldnames=fieldnames)
        test_writer = csv.DictWriter(test_csv, fieldnames=fieldnames)
        classes_writer = csv.DictWriter(classes_csv, fieldnames=classes_fieldnames)
        train_writer.writeheader()
        test_writer.writeheader()
        classes_writer.writeheader()

        processed_species = 0
        bird_species = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
        for species in bird_species:
            classes_writer.writerow({"class":species})
            spectrograms = [f for f in os.listdir(os.path.join(root_dir, species)) if os.path.isfile(os.path.join(root_dir, species, f))]
            processed_count = 0
            for spectrogram in spectrograms:
                current_writer = train_writer
                if processed_count / len(spectrograms) > train_to_test_ratio:
                    current_writer = test_writer
                current_writer.writerow(
                    {
                        "path": os.path.join(species, spectrogram),
                        "species": processed_species
                    }
                )
                print(f"Progress: {processed_files}/{total_files}")
                processed_count += 1
                processed_files += 1
            processed_species += 1


if __name__ == "__main__":
    root_dir = "spectrograms"
    target_train_file = "train_data.csv"
    target_test_file = "test_data.csv"
    target_classes_file = "classes.csv"
    train_to_test_ratio = 0.8
    compose_dataset(root_dir, target_train_file, target_test_file, train_to_test_ratio, target_classes_file)
