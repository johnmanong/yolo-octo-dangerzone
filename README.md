yolo-octo-dangerzone
====================

Command line tool for generating pants BUILD files. If a BUILD file already exists, it will append script output to the end of the file.

Tool tries to assist with import to target resolution by dropping a comments into the BUILD file. Additionally, if an import statement is found in `target_mapping.py`, it will also add the target path for you.


## Usage:
`$ build_pants_target.py <dir>`

## Structure:
 |-- build_pants_target.py: build script
 |-- target_mapping.py: dict with common mappings between import statements and target paths
