load("@lime_deps//:requirements.bzl", "requirement")
load("//:requirements.bzl", "ALL_PIP_DEPS")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "custom_model",
    srcs = ["custom_model.py"],
    deps = [
        ":errors",
        requirement("flask_sqlalchemy"),
        requirement("sqlalchemy"),
    ],
)

py_library(
    name = "db",
    srcs = ["db.py"],
    deps = [
        ":custom_model",
        requirement("flask_sqlalchemy"),
    ]
)

py_library(
    name = "errors",
    srcs = ["errors.py"],
)

py_library(
    name = "models",
    srcs = ["models.py"],
    deps = [
        ":setting",
        ":tag",
        ":tag_group",
        ":task",
        ":user",
    ]
)

py_library(
    name = "setting",
    srcs = ["setting.py"],
    deps = [
        ":db",
    ]
)

py_test(
    name = "setting_test",
    srcs = ["setting_test.py"],
    deps = [
        ":setting",
        ":user",
        requirement("absl-py"),
    ] + ALL_PIP_DEPS,
    python_version = "PY3",
)

py_library(
    name = "tag",
    srcs = ["tag.py"],
    deps = [
        ":db",
        "//lime/util:api",
    ]
)

py_test(
    name = "tag_test",
    srcs = ["tag_test.py"],
    deps = [
        ":models",
        requirement("absl-py"),
    ] + ALL_PIP_DEPS,
    python_version = "PY3",
)

py_library(
    name = "tag_group",
    srcs = ["tag_group.py"],
    deps = [
        ":db",
        "//lime/util:api",
    ]
)

py_test(
    name = "tag_group_test",
    srcs = ["tag_group_test.py"],
    deps = [
        ":models",
        requirement("absl-py"),
    ] + ALL_PIP_DEPS,
    python_version = "PY3",
)

py_library(
    name = "task",
    srcs = ["task.py"],
    deps = [
        ":db",
        "//lime/util:api",
    ]
)

py_test(
    name = "task_test",
    srcs = ["task_test.py"],
    deps = [
        ":db",
        ":models",
        "//lime/util:testing",
        requirement("absl-py"),
    ] + ALL_PIP_DEPS,
    python_version = "PY3",
)

py_library(
    name = "user",
    srcs = ["user.py"],
    deps = [
        ":db",
        "//lime/util:api",
        "//lime/util:passwords",
        "//lime/util:settings",
        "//lime/util:settings_enums",
    ]
)

py_test(
    name = "user_test",
    srcs = ["user_test.py"],
    deps = [
        ":db",
        ":models",
        "//lime/util:settings_enums",
        "//lime/util:testing",
        requirement("absl-py"),
    ] + ALL_PIP_DEPS,
    python_version = "PY3",
)
