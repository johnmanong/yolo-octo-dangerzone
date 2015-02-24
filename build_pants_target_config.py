from string import Template


"""
  This object should hold static mappings from import statements to pants target paths.
  Sadly this is a manual process. :(

"""
PANTS_TARGET_MAPPING = {
    'django_pdb.utils': 'test/path/to:target',
}


"""
  Template used to generate build targets
"""
PANTS_TARGET_TEMPLATE = Template(
    '\npython_library(\nname = $name,\nsources = [$sources],\ndependencies=[\n$dependencies\n]\n)\n')


"""
  True if all python modules are wrapped in a directory of the same name (not working atm)
"""
DOUBLE_DIR_STRUCTURE = True


"""
  Additional paths to search for targets in build files when reconciling import statements
"""
TARGET_SOURCE_ROOTS = [
    'third_party/third_party'
]
