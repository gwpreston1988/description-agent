#!/usr/bin/env python3
"""
Generate 8 missing Solace 14.3 SEER2 system descriptions
Maps AWST30SU/AWST36SU to AWST30LU/AWST36LU specs
"""

import sys
sys.path.insert(0, '/Users/georgepreston/description-agent/pipeline')

from pathlib import Path
from spec_extractor import SpecExtractor
from html_generator import HTMLGenerator

# Initialize
specs_file = '/Users/georgepreston/description-agent/Solace_14.3/Specs/14.3_specs.json'
output_dir = Path('/Users/georgepreston/description-agent/Solace_14.3/Descriptions')

extractor = SpecExtractor(specs_file)
html_gen = HTMLGenerator(14.3, brand="Solace")

# Model number mapping: CSV models -> Specs file models
model_mapping = {
    'S-AWST30SU1308': 'S-AWST30LU1308A',
    'S-AWST30SU1310': 'S-AWST30LU1310A',
    'S-AWST36SU1308': 'S-AWST36LU1308A',
    'S-AWST36SU1310': 'S-AWST36LU1310A',
}

# System combinations to generate
systems = [
    # AC Systems
    ('S-GLXS4BA3010', 'S-AWST30SU1308', 'AC', '2.5Ton'),
    ('S-GLXS4BA3010', 'S-AWST30SU1310', 'AC', '2.5Ton'),
    ('S-GLXS4BA3610', 'S-AWST36SU1308', 'AC', '3Ton'),
    ('S-GLXS4BA3610', 'S-AWST36SU1310', 'AC', '3Ton'),
    # Heat Pump Systems
    ('S-GLZS4BA3010', 'S-AWST30SU1308', 'HP', '2.5Ton'),
    ('S-GLZS4BA3010', 'S-AWST30SU1310', 'HP', '2.5Ton'),
    ('S-GLZS4BA3610', 'S-AWST36SU1308', 'HP', '3Ton'),
    ('S-GLZS4BA3610', 'S-AWST36SU1310', 'HP', '3Ton'),
]

print(f"\nGenerating 8 Solace 14.3 SEER2 system descriptions...\n")

success_count = 0
for condenser_model, ah_model, system_type, tonnage in systems:
    # Map air handler model to specs file model
    ah_spec_model = model_mapping.get(ah_model, ah_model)

    # Get specs
    condenser_spec = extractor.get_spec(condenser_model)
    ah_spec = extractor.get_spec(ah_spec_model)

    if not condenser_spec or not ah_spec:
        print(f"❌ Missing specs for {condenser_model} + {ah_model}")
        continue

    # Update air handler spec to use the correct model number (SU instead of LU, no A suffix)
    ah_spec = ah_spec.copy()
    ah_spec['model_number'] = ah_model

    # Generate HTML
    try:
        if system_type == 'AC':
            html = html_gen.generate_ac_airhandler(condenser_spec, ah_spec)
        else:  # HP
            html = html_gen.generate_hp_airhandler(condenser_spec, ah_spec)

        # Generate filename with exact model numbers from user request
        filename = f"Solace_{tonnage}_R-32_{system_type}_System_{condenser_model}_{ah_model}.html"
        output_path = output_dir / filename

        # Save file
        output_path.write_text(html)
        print(f"✅ {filename}")
        success_count += 1

    except Exception as e:
        print(f"❌ Error generating {condenser_model} + {ah_model}: {e}")

print(f"\n{'='*80}")
print(f"✅ Successfully generated {success_count}/8 descriptions")
print(f"📁 Output: {output_dir}")
print(f"{'='*80}\n")
