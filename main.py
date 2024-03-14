#!/usr/bin/env python3
"""
combine all file contents from a directory into one giant file
"""
import os
import sys
import pyperclip

DIR_EXCLUDE_LIST = [
  "venv",
  "node_modules"
]

FILE_INCLUDE_LIST = [
  "py",
  "js",
  "jsx",
  "ts",
  "txt"
]

def main(dir_path: str) -> None:
  """
  start
  """
  files = walk_directory(dir_path)
  combine_files(files, dir_path)
  # combine_files_to_new_file(files, "combined.txt", dir_path)


def walk_directory(dir_path: str) -> list[str]:
  """
  walk the directory and return list of files
  """
  all_files = []
  for root, dirs, files in os.walk(dir_path):
    dirs[:] = [d for d in dirs if d not in DIR_EXCLUDE_LIST]
    for file in files:
      file_extension = file.split(".")[-1]
      if file_extension in FILE_INCLUDE_LIST:
        all_files.append(os.path.join(root, file))
  return all_files


def combine_files(files: list[str], dir_path: str) -> str:
  """
  combine contents of all files into one giant string
  """
  root_dir_idx = dir_path.rfind("/")
  combined_content = ""
  for file in files:
    combined_content += "-" * 20 + "\n"
    combined_content += f"file name: {file[root_dir_idx + 1:]}" + "\n\n"
    with open(file, "r") as f:
      for line in f:
        combined_content += line
      combined_content += "\n"
  pyperclip.copy(combined_content)
  print(f"copied contents from {len(files)} files to clipboard")
  return combined_content


def combine_files_to_new_file(files: list[str], output_file: str, dir_path: str) -> None:
  """
  combine contents of all files into one giant file
  """
  if os.path.exists(output_file):
    os.remove(output_file)
  line_count = 0
  root_dir_idx = dir_path.rfind("/")
  with open(output_file, "a") as out_file:
    for file in files:
      out_file.write("-" * 20 + "\n")
      out_file.write(f"file name: {file[root_dir_idx + 1:]}" + "\n\n")
      with open(file, "r") as in_file:
        for line in in_file:
          out_file.write(line)
          line_count += 1
      out_file.write("\n\n")
      out_file.write("-" * 20 + "\n")
      line_count += 3
  print(f"combined {len(files)} files into {output_file} with {line_count} lines")


if __name__ == "__main__":
  if len(sys.argv) > 1:
    directory = sys.argv[1]
    if directory == ".":
      directory = os.getcwd()
    print(f"copying contents from directory {directory}")
    main(directory)
  else:
    print("specify the project path")

