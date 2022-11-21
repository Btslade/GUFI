#!/usr/bin/env @PYTHON_INTERPRETER@
# This file is part of GUFI, which is part of MarFS, which is released
# under the BSD license.
#
#
# Copyright (c) 2017, Los Alamos National Security (LANS), LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# From Los Alamos National Security, LLC:
# LA-CC-15-039
#
# Copyright (c) 2017, Los Alamos National Security, LLC All rights reserved.
# Copyright 2017. Los Alamos National Security, LLC. This software was produced
# under U.S. Government contract DE-AC52-06NA25396 for Los Alamos National
# Laboratory (LANL), which is operated by Los Alamos National Security, LLC for
# the U.S. Department of Energy. The U.S. Government has rights to use,
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR LOS
# ALAMOS NATIONAL SECURITY, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is
# modified to produce derivative works, such modified software should be
# clearly marked, so as not to confuse it with the version available from
# LANL.
#
# THIS SOFTWARE IS PROVIDED BY LOS ALAMOS NATIONAL SECURITY, LLC AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL LOS ALAMOS NATIONAL SECURITY, LLC OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.



'''tests functions in performance_pkg/hashing_functions.py'''
# pylint: disable=import-error, invalid-name, wrong-import-position
import copy
import os
import sys
import unittest

# Add performance package to system path
root = "@CMAKE_BINARY_DIR@" # this will be root when merged with master
root = "/home/braeden/Desktop/work/gufi/my_fork/GUFI"
performance_packages = os.path.join(root, "contrib/performance/")
sys.path.insert(0, performance_packages)

import full_command_hash as fh
import gufi_command_hash as gh
import performance_pkg.hashing_functions as hf
import machine_hash as mh

FULL_HASH = "4d5d6d6df57439fe688c5e2bda38c8ef"
GUFI_COMMAND_HASH = "c66ed7dfb8afe717fba57d56cfb62902"
MACHINE_HASH = "edfad81a97df44c1bbd5ea598c8d4112"

FULL_ARGS = ["--hash_type", "md5",
             "--machine", MACHINE_HASH,
             "--gufi", GUFI_COMMAND_HASH]

GUFI_DICT = {"--hash_type": "md5",
             "--gufi": "gufi_query",
             "-S": "SELECT * FROM summary",
             "-E": "SELECT * FROM pentries",
             "--tree": "tree/Desktop"}

MACHINE_ARGS = ["--hash_type", "md5",
                "--machine", "Machine 1",
                "--cpu", "intel",
                "--cores", "100",
                "--ram", "170GB",
                "--storage", "SSD"]

class TestHashingFunctions(unittest.TestCase):

    def test_hash_machine_config(self):
        # ensure hash value generated is consistent
        machine_args = copy.deepcopy(MACHINE_ARGS)  # wont recognize MACHINE_ARGS without global
        parser = mh.parse_arguments(machine_args)
        self.assertEqual(MACHINE_HASH, hf.hash_machine_config(parser))

        # ensure notes and non-essential arguments don't affect the hash
        machine_args += ["--sd_notes", "SSD with 1TB of free space",
                         "--notes", "These are notes",
                         "--database", "performance.db",
                         "--table", "machine_table"]
        parser = mh.parse_arguments(machine_args)
        self.assertEqual(MACHINE_HASH, hf.hash_machine_config(parser))

        # ensure that small deviations result in a non match
        machine_args[3] = "Machine 1 "  # extra space
        parser = mh.parse_arguments(machine_args)
        self.assertNotEqual(MACHINE_HASH, hf.hash_machine_config(parser))

    def test_hash_gufi_command(self):
        # ensure hash value generated is consistent
        gufi_args = []
        for key, val in GUFI_DICT.items():
            gufi_args.append(key)
            gufi_args.append(val)
        parser = gh.parse_arguments(gufi_args)
        self.assertEqual(GUFI_COMMAND_HASH, hf.hash_gufi_command(parser))

        # ensure notes and non-essential arguments don't affect the hash
        gufi_args += ["--notes", "These are notes",
                      "--database", "performance.db",
                      "--table", "gufi_command"]
        parser = gh.parse_arguments(gufi_args)
        self.assertEqual(GUFI_COMMAND_HASH, hf.hash_gufi_command(parser))

        # ensure that small deviations result in a non match
        gufi_args[3] = "gufi_query "  # extra space
        parser = gh.parse_arguments(gufi_args)
        self.assertNotEqual(GUFI_COMMAND_HASH, hf.hash_gufi_command(parser))

        # ensure providing addditional gufi command flags results in a different hash
        gufi_args[3] = "gufi_query"  # set back to default value from previous test
        gufi_args += ["-a"]
        parser = gh.parse_arguments(gufi_args)
        self.assertNotEqual(GUFI_COMMAND_HASH, hf.hash_gufi_command(parser))

    def test_hash_all_values(self):
        # ensure hash value generated is consistent
        full_args = copy.deepcopy(FULL_ARGS)
        parser = fh.parse_arguments(full_args)
        self.assertEqual(FULL_HASH, hf.hash_all_values(parser))

        # ensure notes and non-essential arguments don't affect the hash
        full_args += ["--notes", "These are notes",
                      "--override", "override.db",
                      "--table", "full"]
        parser = fh.parse_arguments(full_args)
        self.assertEqual(FULL_HASH, hf.hash_all_values(parser))

        # ensure that small deviations result in a non match
        full_args[3] = f"{MACHINE_HASH} "  # Extra Space
        parser = fh.parse_arguments(full_args)
        self.assertNotEqual(FULL_HASH, hf.hash_all_values(parser))

if __name__ == '__main__':
    unittest.main()
