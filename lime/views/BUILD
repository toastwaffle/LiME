load("@lime_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "all_views",
    srcs = ["all_views.py"],
    deps = [
        ":auth",
        ":settings",
        ":tags",
        ":tasks",
    ],
)

py_library(
    name = "auth",
    srcs = ["auth.py"],
    deps = [
        "//lime/database:db",
        "//lime/database:errors",
        "//lime/database:models",
        "//lime/util:api",
        "//lime/util:auth",
        "//lime/util:errors",
        requirement("sqlalchemy"),
    ],
)

py_library(
    name = "settings",
    srcs = ["settings.py"],
    deps = [
        "//lime/util:api",
        "//lime/util:errors",
    ],
)

py_library(
    name = "tags",
    srcs = ["tags.py"],
    deps = [
        "//lime/database:db",
        "//lime/database:errors",
        "//lime/database:models",
        "//lime/util:api",
        "//lime/util:auth",
    ],
)

py_library(
    name = "tasks",
    srcs = ["tasks.py"],
    deps = [
        "//lime/database:db",
        "//lime/database:errors",
        "//lime/database:models",
        "//lime/util:api",
        "//lime/util:auth",
        "//lime/util:errors",
    ],
)

py_library(
    name = "testing",
    srcs = ["testing.py"],
    deps = [
        "//lime:app",
        requirement("flask"),
    ],
)
