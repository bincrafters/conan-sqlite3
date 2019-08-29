#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class TestPackageConan(ConanFile):
    settings = "os", "arch"

    def test(self):
        self.run("sqlite3 --version", run_environment=True)
