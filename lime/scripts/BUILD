load("@lime_deps//:requirements.bzl", "requirement")
load("//:requirements.bzl", "ALL_PIP_DEPS")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "cron",
    srcs = ["cron.py"],
    deps = [
        "//lime:app",
        requirement("flask_script"),
    ],
)

py_test(
    name = "cron_test",
    srcs = ["cron_test.py"],
    deps = [
        ":cron",
        "//lime:app",
        requirement("absl-py"),
    ] + ALL_PIP_DEPS,
    python_version = "PY3",
)

py_library(
    name = "run_bpython",
    srcs = ["run_bpython.py"],
    deps = [
        "//lime:app",
        "//lime/database:db",
        "//lime/database:models",
        requirement("flask_script"),
        # We should specify bpython as a dep here, but that pulls in curtsies,
        # which pulls in the typing module backport, which is incompatible with
        # Python 3.7. Bazel puts the pip modules in PYTHONPATH, which is
        # prepended to the default sys.path; therefore the version of typing
        # from pip is used instead of the stdlib version.
        # If we don't specify bpython here, it will be loaded from the system
        # (with an ImportError if it's unavailable), and it will work normally.
        # Given bpython is only used for development, this is fine.
    ],
)
