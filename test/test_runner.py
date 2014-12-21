import unittest
import filecmp
import os


class TestBuildPantsTarget(unittest.TestCase):
  @staticmethod
  def _clear_target_file(file_path):
    open(file_path, 'w').close()

  @staticmethod
  def _run_tool(file_path):
    os.system('../build_pants_target.py %s' % file_path)

  def _test_build(self):
    # allows for reuse of testing logic
    self._clear_target_file(self.build_file_to_test)
    self._run_tool(self.file_to_build)
    self.assertTrue(filecmp.cmp(self.build_file_to_test,
                                self.build_file_fixture))

  def test_build_target_for_test_file(self):
    self.file_to_build = './test.py'
    self.build_file_to_test = 'BUILD'
    self.build_file_fixture = 'fixtures/test/BUILD'
    self._test_build()

  def test_build_target_for_test_dir(self):
    self.file_to_build = '.'
    self.build_file_to_test = 'BUILD'
    self.build_file_fixture = 'fixtures/test_dir/BUILD'
    self._test_build()

  def test_build_target_for_sub_dir(self):
    self.file_to_build = 'subdir/'
    self.build_file_to_test = 'subdir/BUILD'
    self.build_file_fixture = 'fixtures/test_sub_dir/BUILD'
    self._test_build()


#
# This should be run from within the test directory
#

if __name__ == '__main__':
  unittest.main()