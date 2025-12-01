#!/usr/bin/env python3
"""
Universal Description Generator - Works for all SEER ratings and system types
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

from config import SEER_DIRS
from sku_parser import SKUParser
from spec_extractor import SpecExtractor
from html_generator import HTMLGenerator


class UniversalGenerator:
    """Universal generator for all HVAC system descriptions"""

    def __init__(self, seer_rating: str):
        """
        Initialize generator for specific SEER rating

        Args:
            seer_rating: SEER rating as string (e.g., "15.2", "13.4")
        """
        self.seer_rating = seer_rating
        self.seer_float = float(seer_rating) if "_" not in seer_rating else float(seer_rating.split("_")[1])
        self.seer_dir = SEER_DIRS[seer_rating]

        # Detect brand (Solace or Goodman)
        self.brand = "Solace" if "Solace" in seer_rating else "Goodman"

        # Initialize components
        specs_file = self.seer_dir / "Specs" / f"{seer_rating.split('_')[-1]}_specs.json"
        self.parser = SKUParser()
        self.extractor = SpecExtractor(str(specs_file))
        self.html_gen = HTMLGenerator(self.seer_float, brand=self.brand)

        print(f"\n{'='*80}")
        print(f"Universal Description Generator - SEER {seer_rating}")
        print(f"{'='*80}\n")

    def generate_filename(self, system_type: str, models: List[str], specs: Dict[str, Dict]) -> str:
        """
        Generate standardized filename based on system type

        Args:
            system_type: System type from parser (e.g., 'AC_AirHandler', 'AC_80Furnace_Upflow')
            models: List of model numbers
            specs: Dictionary of specs for each model

        Returns:
            Filename string
        """
        # Get tonnage from first condenser/HP
        tonnage = None
        for model, spec in specs.items():
            if spec and 'tonnage' in spec:
                tonnage = HTMLGenerator.format_tonnage(spec['tonnage'])
                break

        if len(models) == 1:
            # Single component
            return f"{self.brand}_R-32_{models[0]}.html"

        elif len(models) == 2:
            # 2-component system
            if 'AC' in system_type and 'AirHandler' in system_type:
                return f"{self.brand}_{tonnage}Ton_R-32_AC_System_{'_'.join(models)}.html"
            elif 'HP' in system_type and 'AirHandler' in system_type:
                return f"{self.brand}_{tonnage}Ton_R-32_HP_System_{'_'.join(models)}.html"
            else:
                return f"{self.brand}_R-32_System_{'_'.join(models)}.html"

        else:
            # 3-component system (Condenser/HP + Furnace + Coil)
            afue = None
            orientation = None

            # Detect AFUE from system_type
            if '80' in system_type:
                afue = '80AFUE'
            elif '92' in system_type:
                afue = '92AFUE'
            elif '96' in system_type:
                afue = '96AFUE'

            # Detect orientation
            if 'Upflow' in system_type:
                orientation = 'Upflow'
            elif 'Horizontal' in system_type:
                orientation = 'Horizontal'

            if 'DualFuel' in system_type or 'HP' in system_type:
                # Dual fuel (HP + Furnace + Coil)
                return f"{self.brand}_R-32_DualFuel_{afue}_{orientation}_System_{'_'.join(models)}.html"
            else:
                # AC + Furnace + Coil
                return f"{self.brand}_R-32_AC_{afue}_{orientation}_System_{'_'.join(models)}.html"

    def generate_description(self, sku_data: Dict, output_dir: Path) -> bool:
        """
        Generate HTML description for a single SKU/system

        Args:
            sku_data: Parsed SKU data from parser
            output_dir: Output directory for HTML files

        Returns:
            True if successful, False otherwise
        """
        models = sku_data['raw_skus']
        system_type = sku_data['system_type']
        component_count = sku_data['component_count']

        # Get specs for all models
        specs = self.extractor.get_multiple_specs(models)

        # Check if all specs found
        if len(specs) != len(models):
            missing = set(models) - set(specs.keys())
            print(f"    ⚠️  Missing specs for: {', '.join(missing)}")
            return False

        # Generate HTML based on system type
        html = None
        try:
            if component_count == 1:
                # Single component
                spec = specs[models[0]]
                component_type = sku_data['component_types'][0]

                if 'AC_Condenser' in component_type:
                    html = self.html_gen.generate_ac_condenser_only(spec)
                elif 'HP_Condenser' in component_type:
                    html = self.html_gen.generate_hp_condenser_only(spec)
                elif 'AirHandler' in component_type:
                    html = self.html_gen.generate_air_handler_only(spec)
                elif 'Coil' in component_type:
                    # Enrich coil spec to ensure orientation and other fields
                    spec = self.extractor.enrich_coil_spec(spec)
                    html = self.html_gen.generate_coil_only(spec)
                elif 'Furnace' in component_type:
                    # Enrich furnace spec
                    spec = self.extractor.enrich_furnace_spec(spec)
                    html = self.html_gen.generate_furnace_only(spec)

            elif component_count == 2:
                if 'AC_AirHandler' in system_type:
                    # AC + Air Handler
                    ac_spec = specs[models[0]]
                    ah_spec = specs[models[1]]
                    html = self.html_gen.generate_ac_airhandler(ac_spec, ah_spec)

                elif 'HP_AirHandler' in system_type:
                    # Heat Pump + Air Handler
                    hp_spec = specs[models[0]]
                    ah_spec = specs[models[1]]
                    html = self.html_gen.generate_hp_airhandler(hp_spec, ah_spec)

            elif component_count == 3:
                # AC/HP + Furnace + Coil - need to sort components properly
                component_types = sku_data['component_types']

                # Find each component by type
                condenser_idx = None
                furnace_idx = None
                coil_idx = None

                for i, comp_type in enumerate(component_types):
                    if 'AC_Condenser' in comp_type or 'HP_Condenser' in comp_type:
                        condenser_idx = i
                    elif 'Furnace' in comp_type:
                        furnace_idx = i
                    elif 'Coil' in comp_type:
                        coil_idx = i

                if condenser_idx is not None and furnace_idx is not None and coil_idx is not None:
                    if 'AC' in system_type:
                        ac_spec = specs[models[condenser_idx]]
                        furnace_spec = self.extractor.enrich_furnace_spec(specs[models[furnace_idx]])
                        coil_spec = self.extractor.enrich_coil_spec(specs[models[coil_idx]])
                        html = self.html_gen.generate_ac_furnace_coil(ac_spec, furnace_spec, coil_spec)

                    elif 'HP' in system_type or 'DualFuel' in system_type:
                        # HP + Furnace + Coil (Dual Fuel)
                        hp_spec = specs[models[condenser_idx]]
                        furnace_spec = self.extractor.enrich_furnace_spec(specs[models[furnace_idx]])
                        coil_spec = self.extractor.enrich_coil_spec(specs[models[coil_idx]])
                        html = self.html_gen.generate_hp_furnace_coil(hp_spec, furnace_spec, coil_spec)

            if not html:
                print(f"    ❌ No generator found for system type: {system_type}")
                return False

            # Generate filename and save
            filename = self.generate_filename(system_type, models, specs)
            output_path = output_dir / filename

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html)

            print(f"    ✅ {filename}")
            return True

        except Exception as e:
            print(f"    ❌ Error: {e}")
            return False

    def generate_all(self, skus_file: Path, output_dir: Path) -> Dict[str, int]:
        """
        Generate all descriptions from a SKUS file

        Args:
            skus_file: Path to SKUS file
            output_dir: Output directory

        Returns:
            Dictionary with statistics
        """
        # Parse all SKUs
        parsed_skus = self.parser.parse_skus_file(str(skus_file))

        print(f"Processing {len(parsed_skus)} systems from {skus_file.name}...\n")

        stats = {
            'total': len(parsed_skus),
            'success': 0,
            'failed': 0
        }

        for idx, sku_data in enumerate(parsed_skus, 1):
            models = sku_data['raw_skus']
            system_type = sku_data['system_type']

            print(f"[{idx}/{stats['total']}] {', '.join(models)}")
            print(f"    System Type: {system_type}")

            if self.generate_description(sku_data, output_dir):
                stats['success'] += 1
            else:
                stats['failed'] += 1

            print()

        return stats


def main():
    """Main entry point"""
    # Get SEER rating from command line argument
    if len(sys.argv) < 2:
        print("Usage: python universal_generator.py <seer_rating>")
        print("Available SEER ratings: 13.4, 14.3, 15.2, 16.2, 17.2, 17.5")
        sys.exit(1)

    seer_rating = sys.argv[1]

    if seer_rating not in SEER_DIRS:
        print(f"❌ Invalid SEER rating: {seer_rating}")
        print(f"Available: {', '.join(SEER_DIRS.keys())}")
        sys.exit(1)

    generator = UniversalGenerator(seer_rating)

    # Use SKUS file (default to SKUS if SKUS_PREVIEW doesn't exist)
    skus_file = SEER_DIRS[seer_rating] / "SKUS" / "SKUS"
    skus_preview = SEER_DIRS[seer_rating] / "SKUS" / "SKUS_PREVIEW"

    if skus_preview.exists():
        skus_file = skus_preview

    output_dir = SEER_DIRS[seer_rating] / "Descriptions"

    if not skus_file.exists():
        print(f"❌ SKUS file not found: {skus_file}")
        sys.exit(1)

    # Generate all
    stats = generator.generate_all(skus_file, output_dir)

    # Print summary
    print(f"{'='*80}")
    print(f"✅ Successfully generated {stats['success']}/{stats['total']} descriptions")
    if stats['failed'] > 0:
        print(f"❌ Failed: {stats['failed']}")
    print(f"📁 Output: {output_dir}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
