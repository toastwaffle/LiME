load("//:requirements.bzl", "ALL_PIP_DEPS")

py_binary(
    name = "command",
    srcs = ["command.py"],
    deps = [
        "//lime:app",
        "//lime/database:db",
        "//lime/database:models",
        "//lime/scripts:cron",
        "//lime/scripts:run_bpython",
        "//lime/system:setup",
    ] + ALL_PIP_DEPS,
    data = glob(["migrations/**/*"]),
    python_version = "PY3",
)
