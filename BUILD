# Copyright 2025 @tragisch <https://github.com/tragisch>
# SPDX-License-Identifier: MIT

# Root BUILD file for bazel-misc utilities

package(default_visibility = ["//visibility:public"])

# Export key library components for external consumption
exports_files([
    "MODULE.bazel",
    "LICENSE",
])

# Create convenient aliases for external users
alias(
    name = "installer",
    actual = "//lib/installer",
    visibility = ["//visibility:public"],
)

alias(
    name = "installer_bzl",
    actual = "//lib/installer:def.bzl",
    visibility = ["//visibility:public"],
)

alias(
    name = "license_report",
    actual = "//lib/license:license_report.bzl",
    visibility = ["//visibility:public"],
)

# Filegroup for documentation
filegroup(
    name = "docs",
    srcs = glob(
        ["doc/**"],
        allow_empty = True,
    ) + [
        "README.md",
        "//lib/installer:README.md",
        "//lib/license:README.md",
    ],
    visibility = ["//visibility:public"],
)
