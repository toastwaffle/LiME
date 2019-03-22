load("@lime_deps//:requirements.bzl", "requirement")
load("//:requirements.bzl", "ALL_PIP_DEPS")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "api",
    srcs = ["api.py"],
    deps = [
        ":crossdomain",
        ":errors",
        requirement("absl-py"),
        requirement("flask"),
    ],
)

py_test(
    name = "api_test",
    srcs = ["api_test.py"],
    deps = [
        ":api",
        ":errors",
        ":testing",
        "//lime:app",
        "//lime/system:setup",
        requirement("absl-py"),
    ] + ALL_PIP_DEPS,
    python_version = "PY3",
)

py_library(
    name = "auth",
    srcs = ["auth.py"],
    deps = [
        ":api",
        ":errors",
        "//lime:app",
        "//lime/database:errors",
        "//lime/database:models",
        requirement("pyjwt"),
    ],
)

py_test(
    name = "auth_test",
    srcs = ["auth_test.py"],
    deps = [
        ":auth",
        ":errors",
        ":testing",
        "//lime:app",
        "//lime/database:db",
        "//lime/database:models",
        requirement("absl-py"),
    ] + ALL_PIP_DEPS,
    python_version = "PY3",
)

py_library(
    name = "crossdomain",
    srcs = ["crossdomain.py"],
    deps = [
        requirement("flask"),
    ],
)

py_test(
    name = "crossdomain_test",
    srcs = ["crossdomain_test.py"],
    deps = [
        ":crossdomain",
        "//lime:app",
        requirement("absl-py"),
    ] + ALL_PIP_DEPS,
    python_version = "PY3",
)

py_library(
    name = "errors",
    srcs = ["errors.py"],
)

py_library(
    name = "passwords",
    srcs = ["passwords.py"],
    deps = [
        "//lime:app",
        "//lime/database:db",
    ],
)

py_library(
    name = "settings",
    srcs = ["settings.py"],
    deps = [
        ":errors",
        "//lime/database:db",
        "//lime/database:setting",
    ],
)

py_library(
    name = "settings_enums",
    srcs = ["settings_enums.py"],
)

py_library(
    name = "testing",
    srcs = ["testing.py"],
    deps = [
        ":api",
        ":auth",
        "//lime:app",
        "//lime/database:db",
        "//lime/database:models",
        "//lime/system:setup",
    ],
    testonly = 1,
)

py_library(
    name = "typevars",
    srcs = ["typevars.py"],
    deps = [
        "//lime/database:models",
    ],
)
