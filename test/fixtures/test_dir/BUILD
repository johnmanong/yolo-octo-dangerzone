
python_library(
    name='middleware',
    sources=['middleware.py'],
    dependencies=[
        # (FAIL: could not find build target for import inspect)
        #import inspect
        # (FAIL: could not find build target for import os)
        #import os
        # (FAIL: could not find build target for import pdb)
        #import pdb
        # (FAIL: could not find build target for import sys)
        #import sys
        # (FAIL: could not find build target for from django.conf import settings)
        #from django.conf import settings
        # (FAIL: could not find build target for from django.core.exceptions import MiddlewareNotUsed)
        #from django.core.exceptions import MiddlewareNotUsed
        # (SUCCESS: match from target mapping) from django_pdb.utils import get_ipdb, has_ipdb
        'test/path/to:target',
        # (FAIL: could not find build target for import important)
        #import important
    ]
)

python_library(
    name='test',
    sources=['test.py'],
    dependencies=[
        # (FAIL: could not find build target for import inspect)
        #import inspect
        # (FAIL: could not find build target for import os)
        #import os
        # (FAIL: could not find build target for import pdb)
        #import pdb
        # (FAIL: could not find build target for import sys)
        #import sys
        # (FAIL: could not find build target for from django.conf import settings)
        #from django.conf import settings
        # (FAIL: could not find build target for from django.core.exceptions import MiddlewareNotUsed)
        #from django.core.exceptions import MiddlewareNotUsed
        # (SUCCESS: match from target mapping) from django_pdb.utils import get_ipdb, has_ipdb
        'test/path/to:target',
        # (FAIL: could not find build target for from middleware import PdbMiddleware)
        #from middleware import PdbMiddleware
        # (SUCCESS: found build target) from test_module.test_module_file import test_module_method
        'test_module/test_module:test_module_file',
        # (SUCCESS: found build target) from some_third_party_module import something
        'third_party/third_party:some_third_party_module',
    ]
)

python_library(
    name='test_runner',
    sources=['test_runner.py'],
    dependencies=[
        # (FAIL: could not find build target for import unittest)
        #import unittest
        # (FAIL: could not find build target for import filecmp)
        #import filecmp
        # (FAIL: could not find build target for import os)
        #import os
    ]
)
