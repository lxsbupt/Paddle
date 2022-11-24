# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
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

import unittest
import subprocess
import sys, os
<<<<<<< HEAD
import json
import shutil
=======
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
import tempfile

import random

from os import listdir
from os.path import isfile, join

pyname = 'train.py'
colpyfile = '''# train.py for unitest
import os
env = os.environ.copy()
assert "PADDLE_MASTER" in env
assert "PADDLE_GLOBAL_SIZE" in env
assert "PADDLE_LOCAL_SIZE" in env
assert "PADDLE_GLOBAL_RANK" in env
assert "PADDLE_LOCAL_RANK" in env
'''

pspyfile = '''# train.py for unitest
import os
env = os.environ.copy()
assert "PADDLE_PSERVERS_IP_PORT_LIST" in env
assert "PADDLE_TRAINER_ENDPOINTS" in env
assert "PADDLE_ROLE" in env
#assert "PADDLE_RANK" in env
'''


def write_file(name, ct):
    with open(name, "w") as f:
        f.write(ct)


def get_files(pth, prefix):
    return [
<<<<<<< HEAD
        f for f in listdir(pth) if isfile(join(pth, f)) and f.startswith(prefix)
        and f != f"{prefix}.gpu.log"
=======
        f
        for f in listdir(pth)
        if isfile(join(pth, f)) and not f.endswith('gpu.log')
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
    ]


class Collective_Test(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.temp_dir.name, pyname)
        write_file(self.path, colpyfile)

    def tearDown(self):
        self.temp_dir.cleanup()

    def pdrun(self, args, env=None):
        cmd = [sys.executable.split('/')[-1], "-m", "paddle.distributed.launch"]
        if args:
            cmd.extend(args.split(" "))
        cmd.extend([self.path])
        env = os.environ.copy()
        # virtual devies for testing
        env.update({'CUDA_VISIBLE_DEVICES': '0,1,2,3,4,5,6,7'})
        proc = subprocess.Popen(cmd, env=env)
        return proc

    def test_collective_1(self):
        log_dir = tempfile.TemporaryDirectory()
        args = "--job_id test1 --log_dir {}".format(log_dir.name)
        p = self.pdrun(args)
        p.wait()
        self.assertTrue(p.poll() == 0)
        log_dir.cleanup()

    def test_collective_2(self):
        log_dir = tempfile.TemporaryDirectory()
        args = "--job_id test2 --devices 0,1,2 --log_dir {}".format(
<<<<<<< HEAD
            log_dir.name)
=======
            log_dir.name
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        p = self.pdrun(args)
        p.wait()
        self.assertTrue(p.poll() == 0)

        c = get_files(log_dir.name, 'test2')
        self.assertTrue(len(c) == 4)
        log_dir.cleanup()

    def test_collective_3(self):
        log_dir = tempfile.TemporaryDirectory()
        port = random.randrange(6000, 8000)
<<<<<<< HEAD
        args = "--job_id test3 --devices 0,1 --log_dir {} --master 127.0.0.1:{} --nnodes 2".format(
            log_dir.name, port)
        p1 = self.pdrun(args)
        p2 = self.pdrun(args)
=======
        args = "--job_id test3 --devices 0,1 --log_dir {} --master 127.0.0.1:{} --nnodes 2"
        p1 = self.pdrun(args.format(log_dir.name + "/1", port))
        p2 = self.pdrun(args.format(log_dir.name + "/2", port))
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        p1.wait()
        p2.wait()
        self.assertTrue(p1.poll() == 0)
        self.assertTrue(p2.poll() == 0)

<<<<<<< HEAD
        c = get_files(log_dir.name, 'test3')
        self.assertTrue(len(c) == 6)
=======
        c1 = get_files(log_dir.name + "/1", 'test3')
        c2 = get_files(log_dir.name + "/2", 'test3')
        print(c1)
        self.assertTrue(len(c1) == 3)
        self.assertTrue(len(c2) == 3)
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        log_dir.cleanup()


class PS_Test(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.temp_dir.name, pyname)
        write_file(self.path, pspyfile)

    def tearDown(self):
        self.temp_dir.cleanup()

    def pdrun(self, args, env=None):
        cmd = [sys.executable.split('/')[-1], "-m", "paddle.distributed.launch"]
        if args:
            cmd.extend(args.split(" "))
        cmd.extend([self.path])
        proc = subprocess.Popen(cmd, env)
        return proc

    def test_ps_1(self):
        log_dir = tempfile.TemporaryDirectory()
        args = "--run_mode ps --log_dir {}".format(log_dir.name)
        p = self.pdrun(args)
        p.wait()
        self.assertTrue(p.poll() == 0)
        log_dir.cleanup()

    def test_ps_2(self):
        log_dir = tempfile.TemporaryDirectory()
<<<<<<< HEAD
        args = "--job_id ps2 --server_num=2 --trainer_num=2 --log_dir {}".format(
            log_dir.name)
=======
        args = (
            "--job_id ps2 --server_num=2 --trainer_num=2 --log_dir {}".format(
                log_dir.name
            )
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        p = self.pdrun(args)
        p.wait()
        self.assertTrue(p.poll() == 0)

        c = get_files(log_dir.name, 'ps2')
        self.assertTrue(len(c) == 5)
        log_dir.cleanup()

    def test_ps_3(self):
        log_dir = tempfile.TemporaryDirectory()
        port = random.randrange(6000, 8000)
<<<<<<< HEAD
        args = "--job_id ps3 --log_dir {} --master 127.0.0.1:{} --nnodes 2 --server_num=1 --trainer_num=1".format(
            log_dir.name, port)
        p1 = self.pdrun(args)
        p2 = self.pdrun(args)
=======
        args = "--job_id ps3 --log_dir {} --master 127.0.0.1:{} --nnodes 2 --server_num=1 --trainer_num=1"
        p1 = self.pdrun(args.format(log_dir.name + "/1", port))
        p2 = self.pdrun(args.format(log_dir.name + "/2", port))
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        p1.wait()
        p2.wait()
        self.assertTrue(p1.poll() == 0)
        self.assertTrue(p2.poll() == 0)

<<<<<<< HEAD
        c = get_files(log_dir.name, 'ps3')
        self.assertTrue(len(c) == 6)
=======
        c1 = get_files(log_dir.name + "/1", 'ps3')
        c2 = get_files(log_dir.name + "/2", 'ps3')
        print(c1)
        self.assertTrue(len(c1) == 3)
        self.assertTrue(len(c2) == 3)
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        log_dir.cleanup()

    def test_ps_4(self):
        log_dir = tempfile.TemporaryDirectory()
        args = "--job_id ps4 --log_dir {} --servers 127.0.0.1:8900,127.0.0.1:8901 --trainers 127.0.0.1:8902,127.0.0.1:8903".format(
<<<<<<< HEAD
            log_dir.name)
=======
            log_dir.name
        )
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        p1 = self.pdrun(args)
        p1.wait()
        self.assertTrue(p1.poll() == 0)

        c = get_files(log_dir.name, 'ps4')
<<<<<<< HEAD
=======
        print(c)
>>>>>>> 43b92b633f5d2db98f45d4b9597e5389f6f9712f
        self.assertTrue(len(c) == 5)
        log_dir.cleanup()


if __name__ == '__main__':
    unittest.main()
