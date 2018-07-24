cmake_minimum_required(VERSION 2.8)
project(cmake_wrapper)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if (WIN32 AND MSVC AND BUILD_SHARED_LIBS)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif(MSVC AND BUILD_SHARED_LIBS)

add_library(sqlite3 sources/sqlite3.c)

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang" AND ${ANDROID} )
    target_compile_definitions(sqlite3 PRIVATE -DBIONIC_IOCTL_NO_SIGNEDNESS_OVERLOAD)
endif()

# Add some options from https://sqlite.org/compile.html
option(ENABLE_JSON1 "Enable JSON SQL functions")
if(ENABLE_JSON1)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_JSON1)
endif()
