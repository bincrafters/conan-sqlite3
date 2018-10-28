cmake_minimum_required(VERSION 2.8)
project(cmake_wrapper)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if (WIN32 AND MSVC AND BUILD_SHARED_LIBS)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif(MSVC AND BUILD_SHARED_LIBS)

add_library(sqlite3 sources/sqlite3.c)

if (${ANDROID})
    if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
        target_compile_definitions(sqlite3 PRIVATE -DBIONIC_IOCTL_NO_SIGNEDNESS_OVERLOAD)
    endif()
endif()

# Add some options from https://sqlite.org/compile.html
option(ENABLE_JSON1 "Enable JSON SQL functions")
if(ENABLE_JSON1)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_JSON1)
endif()

option(ENABLE_COLUMN_METADATA "Enable additional APIs that provide convenient access to meta-data about tables and queries")
if(ENABLE_COLUMN_METADATA)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_COLUMN_METADATA)
endif()

option(ENABLE_EXPLAIN_COMMENTS "Enable SQLite to insert comment text into the output of EXPLAIN")
if(ENABLE_EXPLAIN_COMMENTS)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_EXPLAIN_COMMENTS)
endif()

option(ENABLE_FTS3 "Enable version 3 of the full-text search engine")
if(ENABLE_FTS3)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_FTS3)
endif()

option(ENABLE_FTS4 "Enable version 3 and 4 of the full-text search engine")
if(ENABLE_FTS4)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_FTS4)
endif()

option(ENABLE_FTS5 "Enable version 5 of the full-text search engine")
if(ENABLE_FTS5)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_FTS5)
endif()

option(ENABLE_RTREE "Enable support for the R*Tree index extension")
if(ENABLE_RTREE)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_RTREE)
endif()

option(OMIT_LOAD_EXTENSION "Omits the entire extension loading mechanism from SQLite")
if(OMIT_LOAD_EXTENSION)
    target_compile_definitions(sqlite3 PRIVATE SQLITE_OMIT_LOAD_EXTENSION)
endif()

option(HAVE_FDATASYNC "Use fdatasync() instead of fsync() on unix systems")
if(HAVE_FDATASYNC)
    target_compile_definitions(sqlite3 PRIVATE HAVE_FDATASYNC)
endif()

option(HAVE_GMTIME_R "Use the threadsafe gmtime_r()")
if(HAVE_GMTIME_R)
    target_compile_definitions(sqlite3 PRIVATE HAVE_GMTIME_R)
endif()

option(HAVE_LOCALTIME_R "Use the threadsafe localtime_r()")
if(HAVE_LOCALTIME_R)
    target_compile_definitions(sqlite3 PRIVATE HAVE_LOCALTIME_R)
endif()

option(HAVE_POSIX_FALLOCATE "Use posix_fallocate()")
if(HAVE_POSIX_FALLOCATE)
    target_compile_definitions(sqlite3 PRIVATE HAVE_POSIX_FALLOCATE)
endif()

option(HAVE_STRERROR_R "Use strerror_r()")
if(HAVE_STRERROR_R)
    target_compile_definitions(sqlite3 PRIVATE HAVE_STRERROR_R)
endif()

option(HAVE_USLEEP "Use usleep() system call to implement the xSleep method")
if(HAVE_USLEEP)
    target_compile_definitions(sqlite3 PRIVATE HAVE_USLEEP)
endif()

target_compile_definitions(sqlite3 PRIVATE SQLITE_THREADSAFE=${THREADSAFE})
