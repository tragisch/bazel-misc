#!/usr/bin/env python3
# Copyright 2025 @tragisch <https://github.com/tragisch>
# SPDX-License-Identifier: MIT

"""
License Summary Generator

Creates human-readable license summaries from rules_license JSON reports.
"""

import json
import sys
from typing import Dict, List


def create_summary(json_file: str, output_file: str) -> None:
    """Create a human-readable license summary from JSON report.
    
    Args:
        json_file: Path to the input JSON file containing license data
        output_file: Path to the output text file for the summary
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            licenses_data = json.load(f)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("LICENSE SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            if not licenses_data:
                f.write("No license information found.\n")
                return
            
            # Group by license type
            license_groups: Dict[str, List[str]] = {}
            
            for item in licenses_data:
                # Process licenses from the main structure
                if "licenses" in item:
                    for license_entry in item["licenses"]:
                        # Get package name 
                        package_name = license_entry.get("package_name", "Unknown")
                        
                        # Get license type from license_kinds
                        license_type = "Unknown"
                        if "license_kinds" in license_entry:
                            for kind in license_entry["license_kinds"]:
                                if "name" in kind:
                                    license_type = kind["name"]
                                    break
                        
                        if license_type not in license_groups:
                            license_groups[license_type] = []
                        license_groups[license_type].append(package_name)
            
            # Write summary by license type
            total_packages = 0
            for license_type, packages in sorted(license_groups.items()):
                unique_packages = sorted(set(packages))  # Remove duplicates
                total_packages += len(unique_packages)
                f.write(f"{license_type} ({len(unique_packages)} packages):\n")
                for package in unique_packages:
                    f.write(f"  - {package}\n")
                f.write("\n")
            
            f.write(f"Total packages with license info: {total_packages}\n")
            
    except Exception as e:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Error creating license summary: {e}\n")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) != 3:
        print("Usage: license_summary_generator.py <input.json> <output.txt>")
        sys.exit(1)
    
    create_summary(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
