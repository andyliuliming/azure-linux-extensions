#!/usr/bin/env python
#
#CustomScript extension
#
# Copyright 2014 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Requires Python 2.6+
#

import unittest
import env
import handle
import os
import tempfile
import nohup

class MockUtil():
    def __init__(self, test):
        self.test = test

    def get_log_dir(self):
        return "/tmp"
    def do_status_report(self, operation, status, status_code, message):
        self.test.assertNotEqual(None, message)

    def do_exit(self,exit_code,operation,status,code,message):
        self.test.assertNotEqual(None, message)
        if "Script returned an error" in message:
            raise Exception()

class TestCommandExecution(unittest.TestCase):
    def test_parse_cmd(self):
        cmd = u'sh foo.bar.sh -af bar --foo=bar | more \u6211'
        args = handle.parse_args(cmd)
        self.assertNotEquals(None, args)
        args.insert(0, 'install/nohup.py')
    
    def test_tail(self):
        with open("/tmp/testtail", "w+") as F:
            F.write(u"abcdefghijklmnopqrstu\u6211vwxyz".encode("utf-8"))
        tail = nohup.tail("/tmp/testtail", 2)
        self.assertEquals("yz", tail)

        tail = nohup.tail("/tmp/testtail")
        self.assertEquals("abcdefghijklmnopqrstuvwxyz", tail)

    def test_start_task(self):
        hutil = MockUtil(self)
        test_script = os.path.join(env.root, "test", "mock.sh")
        nohup.start_task(hutil, [test_script, "0"], 0.1)

        with self.assertRaises(Exception):
            nohup.start_task(hutil, [test_script, "1"], 0.1)

if __name__ == '__main__':
    unittest.main()