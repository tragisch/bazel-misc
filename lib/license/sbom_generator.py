#!/usr/bin/env python3
# Copyright 2025 @tragisch <https://github.com/tragisch>
# SPDX-License-Identifier: MIT

"""
SPDX SBOM Generator

Generates SPDX 2.3 compliant Software Bills of Materials from rules_license metadata.
Mimics the functionality of @rules_license//tools:write_sbom.
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Set


def generate_sbom(licenses_info_file: str, output_file: str) -> None:
    """Generate SPDX-style SBOM from license metadata.
    
    Args:
        licenses_info_file: Path to input JSON file with license metadata
        output_file: Path to output SPDX JSON file
    """
    try:
        with open(licenses_info_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Create SPDX-style SBOM structure
        sbom = {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": "Project License SBOM",
            "documentNamespace": "https://github.com/tragisch/monorepo",
            "creationInfo": {
                "created": datetime.utcnow().isoformat() + "Z",
                "creators": ["Tool: custom-bazel-sbom-generator"],
                "licenseListVersion": "3.21"
            },
            "packages": [],
            "relationships": []
        }
        
        package_refs: Dict[str, bool] = {}
        
        # Process each top-level target
        for item in metadata:
            if "licenses" in item:
                for license_entry in item["licenses"]:
                    package_name = license_entry.get("package_name", "unknown")
                    package_ref = f"SPDXRef-Package-{package_name}"
                    
                    if package_ref not in package_refs:
                        # Extract license information
                        license_info: List[str] = []
                        if "license_kinds" in license_entry:
                            for kind in license_entry["license_kinds"]:
                                license_name = kind.get("name", "NOASSERTION")
                                if license_name not in license_info:
                                    license_info.append(license_name)
                        
                        license_concluded = " AND ".join(license_info) if license_info else "NOASSERTION"
                        
                        # Create package entry
                        package = {
                            "SPDXID": package_ref,
                            "name": package_name,
                            "downloadLocation": "NOASSERTION",
                            "filesAnalyzed": False,
                            "licenseConcluded": license_concluded,
                            "licenseDeclared": license_concluded,
                            "copyrightText": license_entry.get("copyright_notice", "NOASSERTION") or "NOASSERTION"
                        }
                        
                        # Add license text reference if available
                        if "license_text" in license_entry and license_entry["license_text"]:
                            package["licenseInfoFromFiles"] = license_info if license_info else ["NOASSERTION"]
                        
                        # Add package version if available
                        if "package_version" in license_entry and license_entry["package_version"]:
                            package["versionInfo"] = license_entry["package_version"]
                        
                        # Add package URL if available
                        if "package_url" in license_entry and license_entry["package_url"]:
                            package["homepage"] = license_entry["package_url"]
                        
                        sbom["packages"].append(package)
                        package_refs[package_ref] = True
                        
                        # Add relationship
                        sbom["relationships"].append({
                            "spdxElementId": "SPDXRef-DOCUMENT",
                            "relatedSpdxElement": package_ref,
                            "relationshipType": "DESCRIBES"
                        })
        
        # Sort packages by name for consistent output
        sbom["packages"].sort(key=lambda x: x["name"])
        sbom["relationships"].sort(key=lambda x: x["relatedSpdxElement"])
        
        # Write SBOM
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sbom, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        # Create error SBOM
        error_sbom = {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": "Error SBOM",
            "documentNamespace": "https://github.com/tragisch/monorepo",
            "creationInfo": {
                "created": datetime.utcnow().isoformat() + "Z",
                "creators": ["Tool: custom-bazel-sbom-generator"],
            },
            "packages": [],
            "relationships": [],
            "errors": [str(e)]
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(error_sbom, f, indent=2, ensure_ascii=False)


def main() -> None:
    """Main entry point.
    
    Supports both the original @rules_license argument style and our simple style.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate SPDX SBOM from license metadata')
    parser.add_argument('--licenses_info', help='Path to input licenses JSON file')
    parser.add_argument('--out', help='Path to output SPDX JSON file')
    
    # Support both argument styles for compatibility
    parser.add_argument('licenses_info_file', nargs='?', help='Input file (positional argument)')
    parser.add_argument('output_file', nargs='?', help='Output file (positional argument)')
    
    args = parser.parse_args()
    
    # Determine input and output files (support both argument styles)
    if args.licenses_info and args.out:
        # Original @rules_license style: --licenses_info --out
        licenses_info_file = args.licenses_info
        output_file = args.out
    elif args.licenses_info_file and args.output_file:
        # Our simple style: positional arguments
        licenses_info_file = args.licenses_info_file
        output_file = args.output_file
    else:
        parser.error("Must provide either --licenses_info and --out, or two positional arguments")
    
    generate_sbom(licenses_info_file, output_file)


if __name__ == "__main__":
    main()
