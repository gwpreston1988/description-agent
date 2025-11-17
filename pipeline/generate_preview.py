#!/usr/bin/env python3
"""
Preview Generator - Generate sample descriptions for review
"""

import sys
from pathlib import Path

# Import pipeline modules
from config import SEER_DIRS
from sku_parser import SKUParser
from spec_extractor import SpecExtractor
from template_selector import TemplateSelector
from content_generator import ContentGenerator
from html_builder import HTMLBuilder

def generate_preview():
    """Generate preview descriptions"""

    seer_rating = "15.2"
    seer_dir = SEER_DIRS[seer_rating]

    # Use preview SKUS file
    skus_file = seer_dir / "SKUS" / "SKUS_PREVIEW"
    specs_file = seer_dir / "Specs" / f"{seer_rating}_specs.json"
    output_dir = Path(__file__).parent.parent / "Preview Descriptions"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    print(f"{'='*80}")
    print(f"Preview Description Generator - SEER {seer_rating}")
    print(f"{'='*80}\n")

    # Initialize components
    parser = SKUParser()
    extractor = SpecExtractor(str(specs_file))
    selector = TemplateSelector()
    generator = ContentGenerator(extractor)
    builder = HTMLBuilder(generator)

    # Parse preview SKUs
    parsed_skus = parser.parse_skus_file(str(skus_file))

    print(f"Generating {len(parsed_skus)} preview descriptions...\n")

    success_count = 0

    # Process each SKU
    for idx, sku_data in enumerate(parsed_skus, 1):
        models = sku_data['raw_skus']
        component_types = sku_data['component_types']
        system_type = sku_data['system_type']

        print(f"[{idx}/{len(parsed_skus)}] {', '.join(models)}")
        print(f"    System Type: {system_type}")

        # Get specs
        specs = extractor.get_multiple_specs(models)

        # Select template
        template_result = selector.select_template(component_types)
        if not template_result:
            print(f"    ❌ No template found\n")
            continue

        template_name, template_path = template_result
        print(f"    Template: {template_name}")

        # Generate filename
        filename = builder.generate_filename(system_type, specs, models)
        output_path = output_dir / filename

        # Build HTML
        try:
            html = builder.build_html(
                template_path,
                system_type,
                specs,
                float(seer_rating),
                models
            )

            if html:
                builder.save_html(html, output_path)
                success_count += 1
            else:
                print(f"    ❌ HTML generation failed\n")
        except Exception as e:
            print(f"    ❌ Error: {e}\n")

    print(f"\n{'='*80}")
    print(f"✅ Successfully generated {success_count}/{len(parsed_skus)} preview descriptions")
    print(f"📁 Output: {output_dir}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    generate_preview()
