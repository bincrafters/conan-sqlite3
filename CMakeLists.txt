cmake_minimum_required(VERSION 3.1.2)
project(sqlite3 C)

include(conanbuildinfo.cmake)
conan_basic_setup()

# Add some options from https://sqlite.org/compile.html
option(ENABLE_JSON1 "Enable JSON SQL functions")

add_library(${PROJECT_NAME} source_subfolder/sqlite3.c
                            source_subfolder/sqlite3.h
                            source_subfolder/sqlite3ext.h)
if (WIN32 AND MSVC AND BUILD_SHARED_LIBS)
    set_target_properties(${PROJECT_NAME} PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif(MSVC AND BUILD_SHARED_LIBS)
if(ENABLE_JSON1)
    target_compile_definitions(${PROJECT_NAME} PRIVATE SQLITE_ENABLE_JSON1)
endif()

install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(DIRECTORY source_subfolder/ DESTINATION include
        FILES_MATCHING PATTERN "*.h")
