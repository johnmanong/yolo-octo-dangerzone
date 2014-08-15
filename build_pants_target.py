import autopep8
import argparse
import os
import re
from string import Template


PANTS_TARGET_TEMPLATE = Template(
    'python_library(\nname = $name,\nsources = [$sources],\ndependencies=[\n$dependencies\n]\n\n)')


def parse_for_pants(file_path):
    dependencies = []
    sources = []

    file_name_and_ext = os.path.basename(file_path)
    file_name, file_ext = os.path.splitext(file_name_and_ext)

    sources.append(file_name_and_ext)

    with open(file_path) as f:
        content = f.readlines()
        for line in content:
            line = line.strip()
            if not line.startswith('#') and re.match(r'.*\bimport\b.*', line):
                # add comment for now to help resolve
                dependencies.append('# ' + line)

    return {
        'name': file_name,
        'sources': sources,
        'dependencies': dependencies
    }


def is_file_for_pants(file_path):
    file_name_and_ext = os.path.basename(file_path)
    file_name, file_ext = os.path.splitext(file_name_and_ext)

    return file_name_and_ext != __file__ \
        and os.path.isfile(file_path) \
        and file_ext == '.py' \
        and not file_name_and_ext.startswith('__')


def build_pants_target(file_info):
    def _wrap_quotes(str):
        return "'" + str + "'"

    name = _wrap_quotes(file_info['name'])
    sources = ", ".join([_wrap_quotes(source)
                         for source in file_info['sources']])
    dependencies = "\n".join(file_info['dependencies'])

    return autopep8.fix_code(PANTS_TARGET_TEMPLATE.substitute(
        name=name,
        sources=sources,
        dependencies=dependencies
    ))


def process_files_for_pants(rootdir):
    with open(rootdir + '/BUILD', 'a') as build_file:
        file_infos = []

        for file in os.listdir(rootdir):
            file_path = rootdir + '/' + file
            if is_file_for_pants(file_path):
                file_infos.append(parse_for_pants(file_path))
            else:
                print 'skipping: ' + file_path

        for file_info in file_infos:
            build_file.write(build_pants_target(file_info))


# get as arg
parser = argparse.ArgumentParser()
parser.add_argument(
    'target_dir', help='full path to process for pants BUILD', action='append')

for target_dir in parser.parse_args().target_dir:
    process_files_for_pants(target_dir)
