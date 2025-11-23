# License Management Tools

Custom license collection and reporting rules compatible with the `@rules_license` framework.

## Overview

This package provides license reporting functionality that is API-compatible with `@rules_license` but offers improved visibility and integration capabilities. The implementation is inspired by the original `@rules_license` but was reimplemented from scratch to address visibility and compatibility issues.

## License Compatibility

- **Our Implementation**: MIT License
- **Original @rules_license**: Apache License 2.0
- **Compatibility**: ✅ Apache 2.0 → MIT is compatible
- **Attribution**: Proper attribution to original source is included

## Features

### Core Functions

- `license_report()` - Collects license information as JSON
- `license_summary()` - Creates human-readable license summaries  
- `license_manifest()` - Generates CSV-style license file listings
- `enhanced_license_report()` - Comprehensive license and metadata reports
- `generate_sbom()` - SPDX 2.3 compliant Software Bill of Materials

### Improvements over @rules_license

1. **Better Visibility**: All components are accessible and modifiable
2. **Enhanced Error Handling**: More robust error reporting
3. **Flexible Output**: Support for multiple output formats
4. **Direct Integration**: No external tool dependencies

## Usage Examples

### Simple License Collection
```starlark
license_report(
    name = "app_licenses",
    deps = [":my_app"],  # Automatically collects ALL transitive deps
)
```

### SBOM Generation
```starlark
generate_sbom(
    name = "app_sbom", 
    deps = [":my_app"],  # Automatically collects ALL transitive deps
    out = "app.spdx",
)
```

### License Manifest
```starlark
license_manifest(
    name = "license_files",
    deps = [":my_app"],  # Automatically collects ALL transitive deps
    warn_on_legacy_licenses = True,
)
```

## API Compatibility

Our implementation maintains full API compatibility with `@rules_license`:

| Original | Our Implementation | Status |
|----------|-------------------|---------|
| `@rules_license//rules_gathering:generate_sbom.bzl` | `generate_sbom()` | ✅ Compatible |
| `@rules_license//rules_gathering:generate_sbom.bzl manifest()` | `license_manifest()` | ✅ Compatible |
| `@rules_license//rules:gather_licenses_info.bzl` | `license_report()` | ✅ Compatible |

## License Information

This package is released under the MIT License. It includes functionality inspired by `@rules_license` (Apache 2.0) but was reimplemented from scratch for compatibility and integration purposes.

See [LICENSE](../../LICENSE) for full license text and attribution information.
