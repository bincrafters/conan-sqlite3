#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import copy

if __name__ == "__main__":

    builder = build_template_default.get_builder()

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
