load("@lime_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "setup",
    srcs = ["setup.py"],
    deps = [
        "//lime:app",
        "//lime/config",
        "//lime/database:db",
        "//lime/util:api",
        "//lime/views:all_views",
        "//lime/views:testing",
    ],
)
