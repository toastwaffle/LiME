load("@lime_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "api",
    srcs = ["api.py"],
    deps = [
        ":crossdomain",
        ":errors",
        requirement("flask"),
    ],
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

py_library(
    name = "crossdomain",
    srcs = ["crossdomain.py"],
    deps = [
        requirement("flask"),
    ],
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
