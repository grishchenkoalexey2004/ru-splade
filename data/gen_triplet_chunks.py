from datasets import load_dataset
import os
import gzip
import shutil


def gzip_file(input_file):
    # Create gzipped version of the file
    output_file = input_file + '.gz'

    if os.path.exists(output_file):
        print(f"Gzipped file already exists at {os.path.abspath(output_file)}")
        return
    else:
        with open(input_file, 'rb') as f_in:
            with gzip.open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    print(f"Created gzipped file at {os.path.abspath(output_file)}")

def concat_tsv_files(input_files,chunk_number):
    # Concatenate all TSV files into one and gzip
    output_file = f"msmarco-ru/triplets/train/chunk_{chunk_number}.tsv"

    if os.path.exists(output_file):
        print(f"Concatenated TSV file already exists at {os.path.abspath(output_file)}")
        return
    else:
        with open(output_file, "w", encoding="utf-8") as outfile:
            for tsv_file in input_files:
                with open(tsv_file, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())

            os.remove(tsv_file)
            
    print(f"Combined {len(input_files)} TSV files into {os.path.abspath(output_file)}")

    print("Gzipping concatenated TSV file")
    gzip_file(output_file)


if __name__ == "__main__":
    print("Введите номера начального и конечного файлов и chunk_number")
    start_file,end_file,chunk_number = list(map(int,input().split()))

    converted_files = []
    for i in range(start_file,end_file+1):
        if len(str(i)) == 1:
            pyarrow_file_name = f"msmarco-ru/triplets/train/data-0000{i}-of-00113.arrow"

        elif len(str(i)) == 2:
            pyarrow_file_name = f"msmarco-ru/triplets/train/data-000{i}-of-00113.arrow"

        elif len(str(i)) == 3:
            pyarrow_file_name = f"msmarco-ru/triplets/train/data-00{i}-of-00113.arrow"

        output_tsv_file = pyarrow_file_name.replace(".arrow",".tsv")

        # Check if output TSV file already exists
        if os.path.exists(output_tsv_file):
            print(f"TSV file already exists at {os.path.abspath(output_tsv_file)}")
            converted_files.append(output_tsv_file)

        else:
            # если tsv файл не существует, то конвертируем arrow файл в tsv
            dataset = load_dataset("arrow", data_files=pyarrow_file_name)["train"]

            with open(output_tsv_file, "w", encoding="utf-8") as f:
                
                # Write data rows
                for row in dataset:
                    values = [str(row[col]) for col in dataset.column_names]
                    f.write("\t".join(values) + "\n")

            print(f"Converted arrow file to TSV at {os.path.abspath(output_tsv_file)}")
            converted_files.append(output_tsv_file)

    concat_tsv_files(converted_files,chunk_number)


    print("Removing individual TSV files after concatenation")
    # Remove individual TSV files after concatenation
    for tsv_file in converted_files:
        os.remove(tsv_file)
        print(f"Removed {os.path.abspath(tsv_file)}")
    print("Done")

    print("Removing concatenated tsv file")
    os.remove(f"msmarco-ru/triplets/train/chunk_{chunk_number}.tsv")
    print("Done")

