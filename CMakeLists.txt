cmake_minimum_required(VERSION 3.1)
project(nlohmann_json LANGUAGES CXX)

add_library(nlohmann_json INTERFACE)
add_library(nlohmann_json::nlohmann_json ALIAS nlohmann_json)
target_include_directories(nlohmann_json
  INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include/nlohmann>
)

if (${CMAKE_VERSION} VERSION_LESS "3.8.0")
  target_compile_features(nlohmann_json INTERFACE cxx_range_for)
else()
  target_compile_features(nlohmann_json INTERFACE cxx_std_11)
endif()

include(GNUInstallDirs)

set(NLOHMANN_JSON_TARGET_NAME               ${PROJECT_NAME})
set(NLOHMANN_JSON_CONFIG_INSTALL_DIR        "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}" CACHE INTERNAL "")
set(NLOHMANN_JSON_INCLUDE_INSTALL_DIR       "${CMAKE_INSTALL_INCLUDEDIR}")
set(NLOHMANN_JSON_TARGETS_EXPORT_NAME       "${PROJECT_NAME}Targets")
set(NLOHMANN_JSON_CMAKE_CONFIG_TEMPLATE     "cmake/config.cmake.in")
set(NLOHMANN_JSON_CMAKE_CONFIG_DIR          "${CMAKE_CURRENT_BINARY_DIR}")
set(NLOHMANN_JSON_CMAKE_VERSION_CONFIG_FILE "${NLOHMANN_JSON_CMAKE_CONFIG_DIR}/${PROJECT_NAME}ConfigVersion.cmake")
set(NLOHMANN_JSON_CMAKE_PROJECT_CONFIG_FILE "${NLOHMANN_JSON_CMAKE_CONFIG_DIR}/${PROJECT_NAME}Config.cmake")
set(NLOHMANN_JSON_CMAKE_PROJECT_TARGETS_FILE "${NLOHMANN_JSON_CMAKE_CONFIG_DIR}/${PROJECT_NAME}Targets.cmake")

##
## INSTALL
## install header files, generate and install cmake config files for find_package()
##
include(CMakePackageConfigHelpers)
# use a custom package version config file instead of
# write_basic_package_version_file to ensure that it's architecture-independent
# https://github.com/nlohmann/json/issues/1697
configure_file(
  "cmake/nlohmann_jsonConfigVersion.cmake.in"
  ${NLOHMANN_JSON_CMAKE_VERSION_CONFIG_FILE}
  @ONLY
)

configure_file(
  ${NLOHMANN_JSON_CMAKE_CONFIG_TEMPLATE}
  ${NLOHMANN_JSON_CMAKE_PROJECT_CONFIG_FILE}
  @ONLY
)

install(
  DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/nlohmann
  DESTINATION ${NLOHMANN_JSON_INCLUDE_INSTALL_DIR}
  FILES_MATCHING PATTERN "*.hpp"
)

install(
  FILES ${NLOHMANN_JSON_CMAKE_PROJECT_CONFIG_FILE} ${NLOHMANN_JSON_CMAKE_VERSION_CONFIG_FILE}
  DESTINATION ${NLOHMANN_JSON_CONFIG_INSTALL_DIR}
)

export(
  TARGETS ${NLOHMANN_JSON_TARGET_NAME}
  NAMESPACE ${PROJECT_NAME}::
  FILE ${NLOHMANN_JSON_CMAKE_PROJECT_TARGETS_FILE}
)

install(
  TARGETS ${NLOHMANN_JSON_TARGET_NAME}
  EXPORT ${NLOHMANN_JSON_TARGETS_EXPORT_NAME}
  INCLUDES DESTINATION ${NLOHMANN_JSON_INCLUDE_INSTALL_DIR}
)

install(
  EXPORT ${NLOHMANN_JSON_TARGETS_EXPORT_NAME}
  NAMESPACE ${PROJECT_NAME}::
  DESTINATION ${NLOHMANN_JSON_CONFIG_INSTALL_DIR}
)
