#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import CMake, tools
from conanfile_base import ConanFileBase


class ConanFileDefault(ConanFileBase):
    name = ConanFileBase._base_name + "_installer"
    version = ConanFileBase.version
    settings = "os_build", "compiler", "arch_build"

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["THREADSAFE"] = 1
        cmake.definitions["ENABLE_COLUMN_METADATA"] = False
        cmake.definitions["ENABLE_EXPLAIN_COMMENTS"] = False
        cmake.definitions["ENABLE_FTS3"] = False
        cmake.definitions["ENABLE_FTS4"] = False
        cmake.definitions["ENABLE_FTS5"] = False
        cmake.definitions["ENABLE_JSON1"] = False
        cmake.definitions["ENABLE_RTREE"] = False
        cmake.definitions["OMIT_LOAD_EXTENSION"] = False
        cmake.definitions["HAVE_FDATASYNC"] = True
        cmake.definitions["HAVE_GMTIME_R"] = True
        cmake.definitions["HAVE_LOCALTIME_R"] = True
        cmake.definitions["HAVE_POSIX_FALLOCATE"] = True
        cmake.definitions["HAVE_STRERROR_R"] = True
        cmake.definitions["HAVE_USLEEP"] = True
        cmake.definitions["BUILD_SHELL"] = True
        if self.settings.os_build == "Windows":
            cmake.definitions["HAVE_LOCALTIME_R"] = False
        if self.settings.os_build != "Linux":
            cmake.definitions["HAVE_POSIX_FALLOCATE"] = False
        cmake.configure()
        return cmake

    def package(self):
        super(ConanFileDefault, self).package()
        tools.rmdir(os.path.join(self.package_folder, "lib"))
        tools.rmdir(os.path.join(self.package_folder, "include"))

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: %s' % bin_path)
        self.env_info.PATH.append(bin_path)
