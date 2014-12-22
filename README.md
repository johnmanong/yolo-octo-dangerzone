yolo-octo-dangerzone
====================

[on github](https://github.com/johnmanong/yolo-octo-dangerzone)

Command line tool for generating pants BUILD files. If a BUILD file already exists, it will append script output to the end of the file.

Tool will first look in a static cache (`target_mapping.py`) to revolve import statements into build targets.

If the import statement is not cached, the tool will programatically try to construct the build target path from the import statement. Tool assumes you are running the script from the project root and that module directories are wrapping in a directory of the same name.

If no build target is found using this strategy, it will simply print the import statement in the build file to assist in manual resolution.

There are several configuration options found in `build_pants_target_config.py`.


## Usage:
`$ build_pants_target.py <dir or file path>`

## Structure:

    |-- build_pants_target.py: build script
    |-- target_mapping.py: dict with common mappings between import statements and target paths

## Testing
Run build script with current directory = `test`