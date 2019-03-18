load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "io_bazel_rules_python",
    # TODO: switch back to bazelbuild repository once
    # https://github.com/bazelbuild/rules_python/pull/158 is merged.
    remote = "https://github.com/cs-world/rules_python.git",
    commit = "e5b4a6d",
)

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

load("@io_bazel_rules_python//python:pip.bzl", "pip_import")

pip_import(
   name = "lime_deps",
   requirements = "//:requirements.txt",
   python_interpreter = "python3",
)

load("@lime_deps//:requirements.bzl", "pip_install")

pip_install()
