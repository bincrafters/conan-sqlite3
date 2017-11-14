project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_library(sqlite3 sources/sqlite3.c)