# Copyright 2025 @tragisch <https://github.com/tragisch>
# SPDX-License-Identifier: MIT
#
# This module provides license reporting functionality inspired by and compatible with
# @rules_license (Apache 2.0) but reimplemented for better integration and visibility.

"""Build file for license management tools."""

load("@rules_license//rules:license.bzl", "license")
load("@rules_python//python:defs.bzl", "py_binary")

package(
    default_applicable_licenses = [":license"],
    default_visibility = ["//visibility:public"],
)

# License declaration for our license management tools
license(
    name = "license",
    package_name = "tools/license",
    license_kinds = ["@rules_license//licenses/spdx:MIT"],
    license_text = "//:LICENSE",  # Reference to root LICENSE file
)

# Export our license management macros
exports_files([
    "license_report.bzl",
    "license_summary_generator.py",
    "sbom_generator.py",
])

# Make Python scripts executable as tools
py_binary(
    name = "license_summary_generator",
    srcs = ["license_summary_generator.py"],
    main = "license_summary_generator.py",
    visibility = ["//visibility:public"],
)

py_binary(
    name = "sbom_generator",
    srcs = ["sbom_generator.py"],
    main = "sbom_generator.py",
    visibility = ["//visibility:public"],
)
