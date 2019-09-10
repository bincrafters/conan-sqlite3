#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import CMake, tools
from conanfile_base import ConanFileBase


class ConanFileDefault(ConanFileBase):
    name = ConanFileBase._base_name
    version = ConanFileBase.version
    settings = "os", "compiler", "arch", "build_type"
    exports_sources = ConanFileBase.exports_sources + ["FindSQLite3.cmake"]
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "threadsafe": [0, 1, 2],
               "enable_column_metadata": [True, False],
               "enable_explain_comments": [True, False],
               "enable_fts3": [True, False],
               "enable_fts4": [True, False],
               "enable_fts5": [True, False],
               "enable_json1": [True, False],
               "enable_rtree": [True, False],
               "omit_load_extension": [True, False]
               }
    default_options = {"shared": False,
                       "fPIC": True,
                       "threadsafe": 1,
                       "enable_column_metadata": False,
                       "enable_explain_comments": False,
                       "enable_fts3": False,
                       "enable_fts4": False,
                       "enable_fts5": False,
                       "enable_json1": False,
                       "enable_rtree": False,
                       "omit_load_extension": False
                       }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["THREADSAFE"] = self.options.threadsafe
        cmake.definitions["ENABLE_COLUMN_METADATA"] = self.options.enable_column_metadata
        cmake.definitions["ENABLE_EXPLAIN_COMMENTS"] = self.options.enable_explain_comments
        cmake.definitions["ENABLE_FTS3"] = self.options.enable_fts3
        cmake.definitions["ENABLE_FTS4"] = self.options.enable_fts4
        cmake.definitions["ENABLE_FTS5"] = self.options.enable_fts5
        cmake.definitions["ENABLE_JSON1"] = self.options.enable_json1
        cmake.definitions["ENABLE_RTREE"] = self.options.enable_rtree
        cmake.definitions["OMIT_LOAD_EXTENSION"] = self.options.omit_load_extension
        cmake.definitions["HAVE_FDATASYNC"] = True
        cmake.definitions["HAVE_GMTIME_R"] = True
        cmake.definitions["HAVE_LOCALTIME_R"] = True
        cmake.definitions["HAVE_POSIX_FALLOCATE"] = True
        cmake.definitions["HAVE_STRERROR_R"] = True
        cmake.definitions["HAVE_USLEEP"] = True
        cmake.definitions["BUILD_SHELL"] = True
        if self.settings.os == "Windows":
            cmake.definitions["HAVE_LOCALTIME_R"] = False
            cmake.definitions["HAVE_POSIX_FALLOCATE"] = False
        if tools.is_apple_os(self.settings.os):
            cmake.definitions["HAVE_POSIX_FALLOCATE"] = False
        if self.settings.os == "Android":
            cmake.definitions["HAVE_POSIX_FALLOCATE"] = False
        cmake.configure()
        return cmake

    def package(self):
        super(ConanFileDefault, self).package()
        self.copy("FindSQLite3.cmake")

    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: %s' % bin_path)
        self.env_info.PATH.append(bin_path)

        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            if self.options.threadsafe:
                self.cpp_info.libs.append("pthread")
            if self.options.omit_load_extension == "False":
                self.cpp_info.libs.append("dl")
