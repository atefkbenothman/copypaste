#!/usr/bin/env python3
"""
Combine all file contents from a directory into one giant file
"""
import os
import sys
import pyperclip

DIR_EXCLUDE_LIST = [
  "venv",
  "node_modules",
  ".git"
]

FILE_INCLUDE_LIST = [
  "py",
  "js",
  "jsx",
  "ts",
  "txt"
]

def main(dir_path: str) -> None:
  file_paths: list[str] = walk_directory(dir_path)
  combined_content: str = combine_files(file_paths, dir_path)
  pyperclip.copy(combined_content)
  print(f"Copied contents from {len(file_paths)} files to clipboard")


def walk_directory(dir_path: str) -> list[str]:
  """
  Walk the directory and return list of files
  """
  file_paths = []
  for root, dirs, files in os.walk(dir_path):
    dirs[:] = [d for d in dirs if d not in DIR_EXCLUDE_LIST]
    for file in files:
      file_extension = file.split(".")[-1]
      if file_extension in FILE_INCLUDE_LIST:
        file_paths.append(os.path.join(root, file))
  return file_paths


def combine_files(files: list[str], dir_path: str) -> str:
  """
  Combine contents of all files into one giant string
  """
  combined_content = ""
  root_dir_idx = dir_path.rfind("/")
  for file in files:
    with open(file, "r") as f:
      combined_content += "-" * 20 + "\n"
      combined_content += f"file name: {file[root_dir_idx + 1:]}" + "\n\n"
      combined_content += f.read()
      combined_content += "\n"
  return combined_content


def combine_files_to_new_file(files: list[str], output_file: str, dir_path: str) -> None:
  """
  Combine contents of all files into one giant file
  """
  if os.path.exists(output_file):
    os.remove(output_file)
  root_dir_idx = dir_path.rfind("/")
  with open(output_file, "a") as out_file:
    for file in files:
      with open(file, "r") as in_file:
        out_file.write("-" * 20 + "\n")
        out_file.write(f"file name: {file[root_dir_idx + 1:]}" + "\n\n")
        out_file.write(in_file.read())
        out_file.write("\n\n")
  print(f"combined {len(files)} files into {output_file}")


if __name__ == "__main__":
  if len(sys.argv) > 1:
    directory = sys.argv[1]
    if directory == ".":
      directory = os.getcwd()
    print(f"copying contents from directory {directory}")
    main(directory)
  else:
    print("specify the project path")

