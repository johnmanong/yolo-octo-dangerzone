"""
  This object should hold static mappings from import statements to pants target paths.
  Sadly this is a manual process. :(

"""

PANTS_TARGET_MAPPING = {
  'django_pdb.utils': 'test/path/to:target',
}