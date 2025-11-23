# bazel-misc

Collection of useful Bazel rules and utilities for project automation.

## Libraries

### Installer Rules (`//lib/installer`)
Starlark rules for creating installers that can deploy Bazel-built artifacts to target systems.

### License Tools (`//lib/license`)
Comprehensive license reporting and SBOM generation tools with API compatibility to `@rules_license`.

## Requirements

- Bazel 8.0+ (uses bzlmod)

## Examples

### Using Installer Rules
```starlark
load("@bazel_misc//lib/installer:def.bzl", "installer")

installer(
    name = "install_my_app",
    data = [":my_binary"],
    target_subdir = "bin",
)
```

### Using License Tools
```starlark
load("@bazel_misc//lib/license:license_report.bzl", "license_report", "generate_sbom")

license_report(
    name = "project_licenses",
    deps = [":my_app"],
)

generate_sbom(
    name = "project_sbom",
    deps = [":my_app"],
)
```
