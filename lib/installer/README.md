# Bazel Installer Tool

This tool provides a convenient way to install Bazel-built binaries to your system.

## Overview

The installer tool generates installation scripts that can copy your built binaries to system directories like `/usr/local/bin` or custom locations.

## Usage

### 1. Define an installer target in your BUILD file

```bazel
load("//tools/installer:def.bzl", "installer")

installer(
    name = "install_my_tool",
    data = [":my_binary"],
    target_subdir = "bin",  # Optional: subdirectory within install prefix
)
```

### 2. Run the installer

```bash
# Install to a custom directory
bazel run //path/to:install_my_tool -- /usr/local/bin

# Install with sudo (use -s flag)
bazel run //path/to:install_my_tool -- -s /usr/local/bin

# Install to home directory
bazel run //path/to:install_my_tool -- ~/bin
```

## Example

For a binary target like this:

```bazel
cc_binary(
    name = "my_tool",
    srcs = ["main.cpp"],
)

installer(
    name = "install_my_tool", 
    data = [":my_tool"],
)
```

You can install it with:

```bash
bazel run //:install_my_tool -- /usr/local/bin
```

This will copy the `my_tool` binary to `/usr/local/bin/my_tool`.

## Features

- Supports single files and directories
- Optional sudo installation with `-s` flag
- Customizable target subdirectories
- Cross-platform compatibility (macOS, Linux)
- Automatic license collection and installation
- Debug mode via `INSTALLER_DEBUG=true` environment variable
- Improved error handling with descriptive messages
- Smart file type detection (binaries → bin/, libraries → lib/, headers → include/)

## Advanced Usage

### Debug Mode
Enable detailed debugging output:
```bash
INSTALLER_DEBUG=true bazel run //path/to:install_my_tool -- /usr/local/bin
```

### System Integration
Create symlinks in standard system directories:
```bash
installer(
    name = "install_my_tool",
    data = [":my_tool"],
    system_integration = True,  # Creates symlinks in /usr/local/*
)
```

## Files

- `def.bzl`: Contains the `installer()` rule definition
- `installer.bash.template`: Bash script