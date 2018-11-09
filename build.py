#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import copy

if __name__ == "__main__":

    builder = build_template_default.get_builder()

    # Add build combinations needed for conan-sqlitecpp
    builds = list(builder.items)
    new_builds = copy.deepcopy(builds)
    for build in new_builds:
        build.options['sqlite3:threadsafe'] = 2
        build.options['sqlite3:enable_column_metadata'] = True
    builder.items.extend(new_builds)

    builder.run()
    