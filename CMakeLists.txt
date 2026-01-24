cmake_minimum_required(VERSION 3.10)
project(RZP)

set(CMAKE_CXX_STANDARD 20)

include_directories(include)

file(GLOB SOURCES "src/*.cpp")

add_executable(RZP ${SOURCES})

# Uncomment and edit if using SFML or SDL2
# find_package(SFML 2.5 COMPONENTS graphics window system REQUIRED)
# target_link_libraries(RZP sfml-graphics sfml-window sfml-system)
