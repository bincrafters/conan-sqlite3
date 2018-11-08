#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class ConanSqlite3(ConanFile):
    name = "sqlite3"
    version = "3.25.3"
    description = "Self-contained, serverless, in-process SQL database engine."
    url = "http://github.com/bincrafters/conan-sqlite3"
    homepage = "https://www.sqlite.org"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = ("conan", "sqlite", "database", "sql", "serverless")
    license = "Public Domain"
    generators = "cmake"
    settings = "os", "compiler", "arch", "build_type"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "FindSQLite3.cmake"]
    options = {"shared": [True, False], "enable_json1": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "enable_json1": False, "fPIC": True}
    _source_subfolder = "source_subfolder"

    def source(self):
        sha256 = "2ad5379f3b665b60599492cc8a13ac480ea6d819f91b1ef32ed0e1ad152fafef"
        download_url = "{}/2018".format(self.homepage)
        archive_name = "sqlite-amalgamation-3250300"
        tools.get("{}/{}.zip".format(download_url, archive_name), sha256=sha256)
        os.rename(archive_name, self._source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_JSON1"] = self.options.enable_json1
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        header = tools.load(os.path.join(self._source_subfolder, "sqlite3.h"))
        license_content = header[3:header.find("***", 1)]
        tools.save("LICENSE", license_content)

        self.copy("LICENSE", dst="licenses")
        self.copy("FindSQLite3.cmake")

        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
            self.cpp_info.libs.append("dl")
