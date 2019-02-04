load("@lime_deps//:requirements.bzl", "requirement")

ALL_PIP_DEPS = [
    # Bazel doesn't handle transitive dependencies properly; list them all here
    # for now. bpython and deps are omitted; see comment in lime/scripts/BUILD.
    requirement("alembic"),
    requirement("astroid"),
    requirement("bcrypt"),
    requirement("blessings"),
    requirement("certifi"),
    requirement("cffi"),
    requirement("chardet"),
    requirement("click"),
    requirement("flask-migrate"),
    requirement("flask-script"),
    requirement("flask-sqlalchemy"),
    requirement("flask"),
    requirement("greenlet"),
    requirement("idna"),
    requirement("isort"),
    requirement("itsdangerous"),
    requirement("jinja2"),
    requirement("lazy-object-proxy"),
    requirement("mako"),
    requirement("markupsafe"),
    requirement("mccabe"),
    requirement("monkeytype"),
    requirement("newrelic"),
    requirement("passlib"),
    requirement("pip-tools"),
    requirement("pycparser"),
    requirement("pygments"),
    requirement("pygresql"),
    requirement("pyjwt"),
    requirement("pylint"),
    requirement("python-dateutil"),
    requirement("python-editor"),
    requirement("requests"),
    requirement("retype"),
    requirement("six"),
    requirement("sqlalchemy"),
    requirement("typed-ast"),
    requirement("urllib3"),
    requirement("wcwidth"),
    requirement("werkzeug"),
    requirement("wrapt"),
]
