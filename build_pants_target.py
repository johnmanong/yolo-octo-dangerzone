#!/usr/bin/env python
import autopep8
import argparse
import logging
import os
import re
from string import Template
from target_mapping import PANTS_TARGET_MAPPING

logger = logging.getLevelName(__name__)


PANTS_TARGET_TEMPLATE = Template(
    '\npython_library(\nname = $name,\nsources = [$sources],\ndependencies=[\n$dependencies\n]\n)\n')


def get_target_for_import(import_statement):
    # split import statement into fragements
    frags = import_statement.split(' ')

    # remove non-module keywords
    frags = [frag for frag in frags if frag not in ['from', 'import']]

    # check config for targets
    matches = [PANTS_TARGET_MAPPING.get(frag) for frag in frags if frag in PANTS_TARGET_MAPPING]

    # return if matches found
    return matches[0] if matches else None


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
        return "'%s'" % string

    name = _wrap_quotes(file_info['name'])
    sources = ", ".join([_wrap_quotes(source)
                         for source in file_info['sources']])
    dependencies = "\n".join(file_info['dependencies'])

    return autopep8.fix_code(PANTS_TARGET_TEMPLATE.substitute(
        name=name,
        sources=sources,
        dependencies=dependencies
    ))


def process_dir_for_pants(target_dir, files=None):
    files = files or os.listdir(target_dir)

    with open(target_dir + '/BUILD', 'a') as build_file:
        file_infos = []

        for file_name in files:
            file_path = target_dir + '/' + file_name
            if is_file_for_pants(file_path):
                file_infos.append(parse_for_pants(file_path))
            else:
                print 'skipping: ' + file_path

        for file_info in file_infos:
            build_file.write(build_pants_target(file_info))


def process_files_for_pants(file_target):
    if os.path.isfile(file_target):
        dir = os.path.dirname(file_target)
        files = [os.path.basename(file_target)]
        process_dir_for_pants(target_dir=dir, files=files)
    elif os.path.isdir(file_target):
        process_dir_for_pants(file_target)
    else:
        logger('Cannot process argument %s', file_target)





# get as arg
parser = argparse.ArgumentParser()
parser.add_argument(
    'files_to_build', help='full path to process for pants BUILD', action='append')

for files_to_build in parser.parse_args().files_to_build:
    process_files_for_pants(files_to_build)
