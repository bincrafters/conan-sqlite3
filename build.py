#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default, build_template_installer, build_shared
import copy
import os

if __name__ == "__main__":
    docker_entry_script = ".ci/entry.sh"

    if "CONAN_CONANFILE" in os.environ and os.environ["CONAN_CONANFILE"] == "conanfile_installer.py":
        arch = os.environ["ARCH"]
        builder = build_template_installer.get_builder(docker_entry_script=docker_entry_script)
        builder.add({"os": build_shared.get_os(), "arch_build": arch, "arch": arch}, {}, {}, {})
        builder.run()
    else:
        builder = build_template_default.get_builder(docker_entry_script=docker_entry_script)

        # Add build combinations needed for conan-sqlitecpp
        builds = list(builder.items)

        new_builds_1 = copy.deepcopy(builds)
        new_builds_2 = copy.deepcopy(builds)

        for build in new_builds_1:
            build.options['sqlite3:threadsafe'] = 2
            build.options['sqlite3:enable_column_metadata'] = True
        for build in new_builds_2:
            build.options['sqlite3:threadsafe'] = 1
            build.options['sqlite3:enable_column_metadata'] = True

        builder.items.extend(new_builds_1)
        builder.items.extend(new_builds_2)

        builder.run()
