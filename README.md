This repository is not more useful. Indeed, since v3.11.3, you can use:
```cmake
include(FetchContent)

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz)
FetchContent_MakeAvailable(json)

target_link_libraries(foo PRIVATE nlohmann_json::nlohmann_json)
```

# Release-tracking repository for nlohmann/json

Goal is to provide a lightweight and autonomous repository tracking every
releases of [nlohmann/json](https://github.com/nlohmann/json).

It is meant to be used with CMake
[FetchContent](https://cmake.org/cmake/help/v3.11/module/FetchContent.html).

You can always replace the URL by the official repository:
<https://github.com/nlohmann/json>.
The only differences are:

* The download size: ~500KB vs ~150MB (300× difference)
* Some options are not available. See [the unsupported options section](#Unsupported-options).

## Example

~~~cmake
include(FetchContent)

# Optional: set this to ON if your target publicly links to nlohmann_json and needs to install() 
# set(JSON_Install ON)

FetchContent_Declare(json
  GIT_REPOSITORY https://github.com/ArthurSonzogni/nlohmann_json_cmake_fetchcontent
  GIT_PROGRESS TRUE  GIT_SHALLOW TRUE
  GIT_TAG v3.11.2)

FetchContent_MakeAvailable(json)

target_link_libraries(foo PRIVATE nlohmann_json::nlohmann_json)
~~~

## Unsupported options

The following options are currently not supported. This is done on purpose
because they do not really make sense for a mirror repository, or they have not
been thoroughly tested. Consider using the official repository if you need these
options.

* `JSON_CI`
* `JSON_BuildTests`

## Updates

This repository is fully autonomous. It updates itself every week using github
actions.

### Thanks

This repository is based on: [astoeckel/json](https://github.com/astoeckel/json).

### Addressed `nlohmann/json` issues:

* [#2073](https://github.com/nlohmann/json/issues/2073),
* [#732](https://github.com/nlohmann/json/issues/732),
* [#620](https://github.com/nlohmann/json/issues/620),
* [#556](https://github.com/nlohmann/json/issues/556),
* [#482](https://github.com/nlohmann/json/issues/482),
* [#96](https://github.com/nlohmann/json/issues/96)

