from __future__ import division, print_function, unicode_literals

__author__ = 'setten'

import os

from pymatgen.util.testing import PymatgenTest
from pymatgen.io.abinitio.tasks import TaskManager

test_dir = os.path.join(os.path.dirname(__file__), "..", "..", 'test_files')

from pymatgen.io.abinitio.flows import Flow


class GWSpecTest(PymatgenTest):
    def test_fixes(self):
        flow = Flow(workdir=test_dir, manager=TaskManager.from_file(os.path.join(test_dir, "taskmanager.yml")))
        inp = {}
        flow.register_task(input=inp)
        flow.allocate()



