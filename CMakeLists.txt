project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_library(sqlite3 sources/sqlite3.c)

# Add some options from https://sqlite.org/compile.html
option(ENABLE_JSON1 "Enable JSON SQL functions")
if(ENABLE_JSON1)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_JSON1)
endif()