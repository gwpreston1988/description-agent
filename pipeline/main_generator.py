#!/usr/bin/env python3
"""
Main Generator - Master orchestration script for HVAC description generation
Unified pipeline for generating HTML descriptions from SKUs and specs

Usage:
    python main_generator.py --seer 15.2 [options]
    python main_generator.py --seer 15.2 --dry-run
    python main_generator.py --seer 15.2 --validate-only
"""

import argparse
import sys
from pathlib import Path

# Import pipeline modules
from config import SEER_DIRS, validate_config
from sku_parser import SKUParser
from spec_extractor import SpecExtractor
from template_selector import TemplateSelector
from content_generator import ContentGenerator
from html_builder import HTMLBuilder


class DescriptionGenerator:
    """Main orchestration class for generating HVAC descriptions"""

    def __init__(self, seer_rating: str, dry_run: bool = False):
        """
        Initialize generator for a specific SEER rating

        Args:
            seer_rating: SEER rating (e.g., "15.2")
            dry_run: If True, don't write files
        """
        self.seer_rating = seer_rating
        self.dry_run = dry_run

        # Get directories
        if seer_rating not in SEER_DIRS:
            raise ValueError(f"Unknown SEER rating: {seer_rating}. Available: {list(SEER_DIRS.keys())}")

        self.seer_dir = SEER_DIRS[seer_rating]
        self.skus_file = self.seer_dir / "SKUS" / "SKUS"
        self.specs_file = self.seer_dir / "Specs" / f"{seer_rating}_specs.json"
        self.output_dir = self.seer_dir / "Generated_Descriptions"

        # Validate paths
        self._validate_paths()

        # Initialize pipeline components
        print(f"\n{'='*80}")
        print(f"HVAC Description Generator - SEER {seer_rating}")
        print(f"{'='*80}\n")

        self.parser = SKUParser()
        self.extractor = SpecExtractor(str(self.specs_file))
        self.selector = TemplateSelector()
        self.generator = ContentGenerator(self.extractor)
        self.builder = HTMLBuilder(self.generator)

        # Statistics
        self.stats = {
            'total_skus': 0,
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0
        }

    def _validate_paths(self):
        """Validate that required paths exist"""
        if not self.seer_dir.exists():
            raise FileNotFoundError(f"SEER directory not found: {self.seer_dir}")

        if not self.skus_file.exists():
            raise FileNotFoundError(f"SKUS file not found: {self.skus_file}")

        if not self.specs_file.exists():
            raise FileNotFoundError(f"Specs file not found: {self.specs_file}")

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def validate_only(self):
        """
        Validate SKUs and specs without generating anything

        Returns:
            True if all valid, False otherwise
        """
        print("🔍 Validation Mode")
        print("-" * 80)

        # Parse SKUs
        parsed_skus = self.parser.parse_skus_file(str(self.skus_file))
        print(f"✅ Parsed {len(parsed_skus)} SKU entries from {self.skus_file.name}")

        all_valid = True
        missing_specs = set()

        # Check each SKU
        for idx, sku_data in enumerate(parsed_skus, 1):
            models = sku_data['raw_skus']

            # Validate specs exist
            is_valid, missing = self.extractor.validate_specs(models)

            if not is_valid:
                all_valid = False
                missing_specs.update(missing)
                print(f"  ⚠️  Line {sku_data['line_number']}: Missing specs for {', '.join(missing)}")

        if all_valid:
            print(f"\n✅ All {len(parsed_skus)} SKU entries have valid specs!")
            return True
        else:
            print(f"\n❌ Validation failed!")
            print(f"  Missing specs for {len(missing_specs)} models: {', '.join(sorted(missing_specs))}")
            return False

    def generate_all(self):
        """Generate all descriptions from SKUS file"""
        print("🚀 Starting generation process...")
        print("-" * 80)

        # Parse SKUs
        parsed_skus = self.parser.parse_skus_file(str(self.skus_file))
        self.stats['total_skus'] = len(parsed_skus)

        if not parsed_skus:
            print("❌ No valid SKUs found in SKUS file")
            return

        print(f"Found {len(parsed_skus)} SKU entries to process\n")

        # Process each SKU
        for idx, sku_data in enumerate(parsed_skus, 1):
            self._process_sku(idx, sku_data)

        # Print summary
        self._print_summary()

    def _process_sku(self, idx: int, sku_data: dict):
        """
        Process a single SKU entry

        Args:
            idx: Entry number (for display)
            sku_data: Parsed SKU data dictionary
        """
        self.stats['processed'] += 1

        models = sku_data['raw_skus']
        component_types = sku_data['component_types']
        system_type = sku_data['system_type']

        print(f"[{idx}/{self.stats['total_skus']}] Processing: {', '.join(models)}")
        print(f"    System: {system_type}")

        # Validate specs
        is_valid, missing = self.extractor.validate_specs(models)
        if not is_valid:
            print(f"    ❌ Missing specs for: {', '.join(missing)}")
            self.stats['failed'] += 1
            return

        # Get specs
        specs = self.extractor.get_multiple_specs(models)

        # Select template
        template_result = self.selector.select_template(component_types)
        if not template_result:
            print(f"    ❌ No suitable template found")
            self.stats['failed'] += 1
            return

        template_name, template_path = template_result
        print(f"    Template: {template_name}")

        # Generate filename
        filename = self.builder.generate_filename(system_type, specs, models)
        output_path = self.output_dir / filename

        # Build HTML
        try:
            html = self.builder.build_html(
                template_path,
                system_type,
                specs,
                float(self.seer_rating),
                models
            )

            if not html:
                print(f"    ❌ HTML generation failed")
                self.stats['failed'] += 1
                return

            # Save file (unless dry run)
            if self.dry_run:
                print(f"    🔍 DRY RUN: Would save to {filename}")
                self.stats['successful'] += 1
            else:
                success = self.builder.save_html(html, output_path)
                if success:
                    self.stats['successful'] += 1
                else:
                    self.stats['failed'] += 1

        except Exception as e:
            print(f"    ❌ Error: {e}")
            self.stats['failed'] += 1

        print()  # Blank line between entries

    def _print_summary(self):
        """Print generation summary statistics"""
        print("=" * 80)
        print("GENERATION SUMMARY")
        print("=" * 80)
        print(f"Total SKU Entries:  {self.stats['total_skus']}")
        print(f"Processed:          {self.stats['processed']}")
        print(f"✅ Successful:      {self.stats['successful']}")
        print(f"❌ Failed:          {self.stats['failed']}")
        print(f"⏭️  Skipped:         {self.stats['skipped']}")
        print()

        if self.dry_run:
            print("🔍 DRY RUN MODE - No files were actually written")
        else:
            print(f"📁 Output directory: {self.output_dir}")

        print("=" * 80)


def main():
    """Main entry point with CLI argument parsing"""
    parser = argparse.ArgumentParser(
        description='HVAC Description Generator - Unified Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all descriptions for SEER 15.2
  python main_generator.py --seer 15.2

  # Dry run (don't write files)
  python main_generator.py --seer 15.2 --dry-run

  # Validate only (check SKUs and specs)
  python main_generator.py --seer 15.2 --validate-only

  # Test configuration
  python main_generator.py --test-config
        """
    )

    parser.add_argument('--seer', type=str, help='SEER rating (e.g., 15.2, 14.3)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing files')
    parser.add_argument('--validate-only', action='store_true', help='Only validate SKUs and specs')
    parser.add_argument('--test-config', action='store_true', help='Test configuration')

    args = parser.parse_args()

    # Test config
    if args.test_config:
        print("Testing configuration...")
        errors = validate_config()
        if errors:
            print("❌ Configuration errors found:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print("✅ Configuration validated successfully!")
            print(f"Available SEER ratings: {', '.join(SEER_DIRS.keys())}")
            sys.exit(0)

    # Require --seer for other operations
    if not args.seer:
        parser.print_help()
        print("\n❌ Error: --seer argument is required")
        sys.exit(1)

    try:
        # Initialize generator
        gen = DescriptionGenerator(args.seer, dry_run=args.dry_run)

        # Run validation only or full generation
        if args.validate_only:
            is_valid = gen.validate_only()
            sys.exit(0 if is_valid else 1)
        else:
            gen.generate_all()

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
