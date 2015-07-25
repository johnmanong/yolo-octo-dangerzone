#!/usr/bin/env python
import argparse
import os
import re
import string


TAB = ' ' * 4

PANTS_TARGET_TEMPLATE = string.Template(
    'python_library(\n'
    + TAB + 'name=$name,\n'
    + TAB + 'sources=[$sources],\n'
    + TAB + 'dependencies=[\n'
    + TAB + TAB + '$dependencies\n'
    + TAB + ']\n'
    + ')\n\n'
)


PANTS_TARGET_TEMPLATE_MAP = {
    'lib': PANTS_TARGET_TEMPLATE,
    'bin': None,
    'tests': None,
}


def target_exists_in_build_file(build_file_path, target_name):
    """
    Determine if build file contains target.
    """
    if not os.path.isfile(build_file_path):
        print 'build_file_path=%r does not point to valid BUILD file' % build_file_path
        return False

    return "name='%s'" % target_name in open(build_file_path, 'r').read()


def pants_info_from_file(file_path):
    dependencies = []
    sources = []

    file_name_and_ext = os.path.basename(file_path)
    file_name, _ = os.path.splitext(file_name_and_ext)

    sources.append(file_name_and_ext)

    return {
        'name': file_name,
        'sources': sources,
        'dependencies': [],
    }


def is_file_for_pants(file_path):
    """
    Determine whether pants should build a target for this file.
    """
    file_name_and_ext = os.path.basename(file_path)
    _, file_ext = os.path.splitext(file_name_and_ext)

    return file_name_and_ext != __file__ \
        and os.path.isfile(file_path) \
        and file_ext == '.py' \
        and not file_name_and_ext.startswith('__')


def build_pants_target(file_info):
    """
    Convert a file_info object into pants target string.
    Not support for dependencies in this tool.
    """
    def _wrap_quotes(string):
        return "'%s'" % string

    name = _wrap_quotes(file_info['name'])
    sources = ', '.join([_wrap_quotes(source)
                         for source in file_info['sources']])

    return PANTS_TARGET_TEMPLATE.substitute(
        name=name,
        sources=sources,
        dependencies=''
    )

def process_dir_for_pants(target_dir, files=None):
    files = files or os.listdir(target_dir)

    with open(target_dir + '/BUILD', 'a') as build_file:
        file_infos = []

        for file_name in files:
            file_path = target_dir + file_name

            # some files, like __init__.py files, can be ignored.
            if not is_file_for_pants(file_path):
                print 'cannot build target for %r' % file_path
                continue

            # parse file into info obj with target info
            file_info_obj = pants_info_from_file(file_path)

            # check for file in build file
            if target_exists_in_build_file(build_file_path=build_file.name,
                    target_name=file_info_obj['name']):
                print 'target name %r found in BUILD' % file_info_obj['name']
            else:
                file_infos.append(file_info_obj)

        for file_info in file_infos:
            build_file.write(build_pants_target(file_info))

def process_files_for_pants(file_target):
    if os.path.isfile(file_target):
        # only process single file
        dirname = os.path.dirname(file_target) + '/'
        files = [os.path.basename(file_target)]
        process_dir_for_pants(target_dir=dirname, files=files)
    elif os.path.isdir(file_target):
        # process all files in directory
        process_dir_for_pants(file_target)
    else:
        print('Cannot process argument %s', file_target)

# get as arg
parser = argparse.ArgumentParser()
parser.add_argument(
    'files_to_build', help='full path to process for pants BUILD', action='append')

for files_to_build in parser.parse_args().files_to_build:
    process_files_for_pants(files_to_build)
