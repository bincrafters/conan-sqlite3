#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools


class ConanFileBase(ConanFile):
    _base_name = "sqlite3"
    version = "3.29.0"
    description = "Self-contained, serverless, in-process SQL database engine."
    url = "http://github.com/bincrafters/conan-sqlite3"
    homepage = "https://www.sqlite.org"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = ("conan", "sqlite", "database", "sql", "serverless")
    license = "Public Domain"
    generators = "cmake"
    exports = ["LICENSE.md", "conanfile_base.py"]
    exports_sources = ["CMakeLists.txt"]

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        sha256 = "48253d8f1616f213422e4374cff39050488d2497812d9bbb8609524127d45732"
        download_url = "{}/2019".format(self.homepage)
        major, minor, patch = self.version.split(".")
        archive_name = "sqlite-amalgamation-" + major + minor.rjust(2, "0") + patch.rjust(2, "0") + "00"
        tools.get("{}/{}.zip".format(download_url, archive_name), sha256=sha256)
        os.rename(archive_name, self._source_subfolder)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        header = tools.load(os.path.join(self._source_subfolder, "sqlite3.h"))
        license_content = header[3:header.find("***", 1)]
        tools.save("LICENSE", license_content)
        self.copy("LICENSE", dst="licenses")

        cmake = self._configure_cmake()
        cmake.install()
