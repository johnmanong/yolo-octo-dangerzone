#!/usr/bin/env python
import autopep8
import argparse
import os
import re
from string import Template
from target_mapping import PANTS_TARGET_MAPPING


PANTS_TARGET_TEMPLATE = Template(
    '\npython_library(\nname = $name,\nsources = [$sources],\ndependencies=[\n$dependencies\n]\n)\n')


def get_target_for_import(import_statement):
    # split import statement into fragements
    frags = import_statement.split(' ')

    # remove non-module keywords
    frags = [frag for frag in frags if frag not in ['from', 'import']]

    # check config for targets
    mapped_frags = map(lambda x: PANTS_TARGET_MAPPING.get(x), frags)
    return next((item for item in mapped_frags if item is not None), None)


def parse_for_pants(file_path):
    dependencies = []
    sources = []

    file_name_and_ext = os.path.basename(file_path)
    file_name, _ = os.path.splitext(file_name_and_ext)

    sources.append(file_name_and_ext)

    with open(file_path) as file_to_parse:
        content = file_to_parse.readlines()
        for line in content:
            line = line.strip()
            if not line.startswith('#') and re.match(r'.*\bimport\b.*', line):

                # check known targets for match
                target_path = get_target_for_import(line)

                if target_path is not None:
                    # match found, mark as matched and add target path
                    dependencies.append('# (match) %s' % line)
                    dependencies.append("'%s'," % target_path)
                else:
                    # add comment for now to help resolve
                    dependencies.append('# %s' % line)


    return {
        'name': file_name,
        'sources': sources,
        'dependencies': dependencies
    }


def is_file_for_pants(file_path):
    file_name_and_ext = os.path.basename(file_path)
    _, file_ext = os.path.splitext(file_name_and_ext)

    return file_name_and_ext != __file__ \
        and os.path.isfile(file_path) \
        and file_ext == '.py' \
        and not file_name_and_ext.startswith('__')


def build_pants_target(file_info):
    def _wrap_quotes(string):
        return "'" + string + "'"

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

        for file_name in os.listdir(rootdir):
            file_path = rootdir + '/' + file_name
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
