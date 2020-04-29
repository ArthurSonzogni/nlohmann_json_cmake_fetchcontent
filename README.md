# Release-tracking repository for nlohmann/json

This repository is based on:
https://github.com/astoeckel/json

It provides a lightweight repository tracking every releases of
https://github.com/nlohmann/json. You can then depends on it using CMake
[FetchContent](https://cmake.org/cmake/help/v3.11/module/FetchContent.html).

Example:
~~~cmake
include(FetchContent)

FetchContent_Declare(json
  GIT_REPOSITORY
  https://github.com/ArthurSonzogni/nlohmann_json_cmake_fetchcontent
  GIT_TAG v3.7.3)

FetchContent_GetProperties(json)
if(NOT json_POPULATED)
  FetchContent_Populate(json)
  add_subdirectory(${json_SOURCE_DIR} ${json_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()

target_link_libraries(foo PRIVATE nlohmann_json::nlohmann_json)
~~~

Of course, you can use replace the lightweight repository with the official one:
https://github.com/nlohmann/json

The script ./update.py made by @astoeckel automatically download every
nlohmann::json releases and put them into their corresponding git tag.

See:
- [#2073](https://github.com/nlohmann/json/issues/2073),
- [#732](https://github.com/nlohmann/json/issues/732),
- [#620](https://github.com/nlohmann/json/issues/620),
- [#556](https://github.com/nlohmann/json/issues/556),
- [#482](https://github.com/nlohmann/json/issues/482),
- [#96](https://github.com/nlohmann/json/issues/96)
