#!/usr/bin/env python3
"""
15.2 SEER2 Spec Extractor
Extracts outdoor unit specs (heat pumps + AC condensers) from PDFs,
then combines with indoor equipment from 13-4-specs.json.
"""

import json
import re
import sys
import pdfplumber
from pathlib import Path
from typing import Dict, List, Optional

sys.stdout = sys.stdout
sys.stderr = sys.stderr

# Model lists
HEAT_PUMPS = ['GLZS5BA1810', 'GLZS5BA2410', 'GLZS5BA3010', 'GLZS5BA3610',
              'GLZS5BA4210', 'GLZS5BA4810', 'GLZS5BA6010']
AC_CONDENSERS = ['GLXS5BA1810', 'GLXS5BA2410', 'GLXS5BA3010', 'GLXS5BA3610',
                 'GLXS5BA4210', 'GLXS5BA4810', 'GLXS5BA6010']

# File paths
HP_PDF = Path('./GLZS5B.pdf')
AC_PDF = Path('./GLXS5B.pdf')
INDOOR_SPECS = Path('../13-4-specs.json')
OUTPUT_FILE = Path('./15.2_SEER.json')


def clean_number(value: str) -> Optional[float]:
    """Clean and convert string to number."""
    if not value or value == '—' or value == '-':
        return None
    cleaned = re.sub(r'[,\s]', '', value)
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_fraction(value: str) -> Optional[float]:
    """Parse fractional dimensions like '35½' or '41⅝'."""
    if not value:
        return None

    value = value.replace('\n', '').replace('"', '').replace("'", '').strip()

    # Unicode fraction map
    fraction_map = {
        '½': 0.5, '¼': 0.25, '¾': 0.75, '⅛': 0.125, '⅜': 0.375,
        '⅝': 0.625, '⅞': 0.875, '⅓': 0.333, '⅔': 0.667
    }

    # Handle mixed fractions like "35½"
    for frac_char, frac_value in fraction_map.items():
        if frac_char in value:
            parts = value.split(frac_char)
            whole = float(parts[0]) if parts[0] else 0
            return whole + frac_value

    # Handle standard fractions
    if '/' in value:
        try:
            if ' ' in value:
                parts = value.split()
                whole = float(parts[0])
                frac = parts[1].split('/')
                return whole + (float(frac[0]) / float(frac[1]))
            else:
                parts = value.split('/')
                return float(parts[0]) / float(parts[1])
        except:
            return None

    try:
        return float(value)
    except:
        return None


def parse_ac_condenser(pdf_path: Path, model_number: str) -> Dict:
    """Parse AC condenser specs from GLXS5B.pdf."""
    print(f"Processing {model_number} (AC Condenser)...")

    spec = {
        'model_number': model_number,
        'brand': 'Goodman',
        'equipment_type': 'Air Conditioner Condenser',
        'tonnage': None,
        'cooling_capacity_btuh': None,
        'seer2': 15.2,
        'eer2': None,
        'voltage': None,
        'phase': 1,
        'frequency_hz': 60,
        'mca': None,
        'mop': None,
        'refrigerant_type': 'R-410A',
        'factory_charge_oz': None,
        'liquid_line_od_in': None,
        'suction_line_od_in': None,
        'compressor_type': None,
        'sound_level_dba': None,
        'height_in': None,
        'width_in': None,
        'depth_in': None,
        'shipping_weight_lb': None,
    }

    with pdfplumber.open(pdf_path) as pdf:
        # Page 3 - Specifications table
        if len(pdf.pages) > 2:
            spec_page = pdf.pages[2]
            tables = spec_page.extract_tables()

            if tables and len(tables) > 0:
                table = tables[0]

                # Find model column - search for model number in header
                col_idx = None
                header_row = table[0]
                for idx, cell in enumerate(header_row):
                    if cell and model_number[:12] in cell.replace('\n', '').replace(' ', ''):
                        col_idx = idx
                        break

                if col_idx:
                    # Row 1: Capacities (BTU/h line 0, dBA line 1)
                    if len(table) > 1:
                        row = table[1]
                        values = row[col_idx].split('\n') if row[col_idx] else []
                        if len(values) >= 2:
                            spec['cooling_capacity_btuh'] = int(clean_number(values[0]) or 0)
                            spec['tonnage'] = round(spec['cooling_capacity_btuh'] / 12000, 1)
                            spec['sound_level_dba'] = clean_number(values[1])

                    # Row 2: Compressor (Type is last line)
                    if len(table) > 2:
                        row = table[2]
                        values = row[col_idx].split('\n') if row[col_idx] else []
                        if len(values) >= 4:
                            spec['compressor_type'] = values[-1]  # Last line is type

                    # Row 4: Refrigeration System
                    if len(table) > 4:
                        row = table[4]
                        values = row[col_idx].split('\n') if row[col_idx] else []
                        if len(values) >= 6:
                            # Lines: liquid, suction, liquid(repeat), suction(repeat), connection type, charge
                            spec['liquid_line_od_in'] = parse_fraction(values[0])
                            spec['suction_line_od_in'] = parse_fraction(values[1])
                            spec['factory_charge_oz'] = clean_number(values[-1])

                    # Row 5: Electrical Data
                    if len(table) > 5:
                        row = table[5]
                        values = row[col_idx].split('\n') if row[col_idx] else []
                        if len(values) >= 3:
                            voltage_match = re.search(r'(\d+/\d+)', values[0])
                            if voltage_match:
                                spec['voltage'] = voltage_match.group(1)
                            spec['mca'] = clean_number(values[1])
                            spec['mop'] = clean_number(values[2])

                    # Row 6: Equipment Weight
                    if len(table) > 6:
                        row = table[6]
                        values = row[col_idx].split('\n') if row[col_idx] else []
                        if len(values) >= 1:
                            spec['shipping_weight_lb'] = clean_number(values[0])

        # Page 19 - Dimensions
        if len(pdf.pages) > 18:
            dim_page = pdf.pages[18]
            dim_text = dim_page.extract_text()

            # Parse dimensions from text
            for line in dim_text.split('\n'):
                if model_number[:12] in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        # Format: Model W D H
                        spec['width_in'] = parse_fraction(parts[1])
                        spec['depth_in'] = parse_fraction(parts[2])
                        spec['height_in'] = parse_fraction(parts[3])
                    break

    return spec


def parse_heat_pump(pdf_path: Path, model_number: str) -> Dict:
    """Parse heat pump specs from GLZS5B.pdf."""
    print(f"Processing {model_number} (Heat Pump)...")

    spec = {
        'model_number': model_number,
        'brand': 'Goodman',
        'equipment_type': 'Heat Pump Condenser',
        'tonnage': None,
        'cooling_capacity_btuh': None,
        'heating_capacity_btuh': None,
        'seer2': 15.2,
        'eer2': None,
        'hspf2': None,
        'low_ambient_cooling': None,
        'voltage': None,
        'phase': 1,
        'frequency_hz': 60,
        'mca': None,
        'mop': None,
        'refrigerant_type': 'R-410A',
        'factory_charge_oz': None,
        'liquid_line_od_in': None,
        'suction_line_od_in': None,
        'compressor_type': None,
        'defrost_type': None,
        'sound_level_dba': None,
        'height_in': None,
        'width_in': None,
        'depth_in': None,
        'shipping_weight_lb': None,
    }

    with pdfplumber.open(pdf_path) as pdf:
        # Page 3 - Specifications table
        if len(pdf.pages) > 2:
            spec_page = pdf.pages[2]
            tables = spec_page.extract_tables()

            if tables and len(tables) > 0:
                table = tables[0]

                # Find model column
                col_idx = None
                header_row = table[0]
                for idx, cell in enumerate(header_row):
                    if cell and model_number[:11] in cell.replace('\n', '').replace(' ', ''):
                        col_idx = idx
                        break

                if col_idx:
                    # Extract from table rows
                    for row_idx, row in enumerate(table):
                        if not row or not row[0]:
                            continue

                        cell_text = row[0].lower()

                        # Nominal Capacities row
                        if 'cooling' in cell_text and 'btu' in cell_text:
                            values = row[col_idx].split('\n') if row[col_idx] else []
                            if len(values) >= 2:
                                spec['cooling_capacity_btuh'] = int(clean_number(values[0]) or 0)
                                spec['heating_capacity_btuh'] = int(clean_number(values[1]) or 0)
                                spec['tonnage'] = round(spec['cooling_capacity_btuh'] / 12000, 1)
                            # Line 3 is dBA
                            if len(values) >= 4:
                                spec['sound_level_dba'] = clean_number(values[3])

                        # SEER2 and dBA row
                        elif 'seer2' in cell_text or 'decibel' in cell_text:
                            values = row[col_idx].split('\n') if row[col_idx] else []
                            for val in values:
                                num = clean_number(val)
                                if num:
                                    if num > 60:  # dBA value
                                        spec['sound_level_dba'] = num

                        # HSPF2 row
                        elif 'hspf2' in cell_text:
                            value = row[col_idx]
                            spec['hspf2'] = clean_number(value)

                        # Compressor row
                        elif 'compressor' in cell_text:
                            values = row[col_idx].split('\n') if row[col_idx] else []
                            if values:
                                spec['compressor_type'] = values[-1]

                        # Refrigeration System
                        elif 'refrigeration' in cell_text or 'line size' in cell_text:
                            values = row[col_idx].split('\n') if row[col_idx] else []
                            if len(values) >= 6:
                                spec['liquid_line_od_in'] = parse_fraction(values[0])
                                spec['suction_line_od_in'] = parse_fraction(values[1])
                                spec['factory_charge_oz'] = clean_number(values[-1])

                        # Electrical Data
                        elif 'electrical' in cell_text:
                            values = row[col_idx].split('\n') if row[col_idx] else []
                            if len(values) >= 3:
                                voltage_match = re.search(r'(\d+/\d+)', values[0])
                                if voltage_match:
                                    spec['voltage'] = voltage_match.group(1)
                                spec['mca'] = clean_number(values[1])
                                spec['mop'] = clean_number(values[2])

                        # Equipment Weight
                        elif 'weight' in cell_text:
                            values = row[col_idx].split('\n') if row[col_idx] else []
                            # Shipping weight is typically the second value
                            if len(values) >= 2:
                                spec['shipping_weight_lb'] = clean_number(values[1])
                            elif len(values) >= 1:
                                spec['shipping_weight_lb'] = clean_number(values[0])

        # Page 21 - Dimensions (heat pumps are on page 21, not 19)
        if len(pdf.pages) > 20:
            dim_page = pdf.pages[20]
            dim_text = dim_page.extract_text()

            for line in dim_text.split('\n'):
                # Handle edge cases: PDF typos and extra chars (F, numbers)
                # Look for model number allowing for typos (GLZ5S5BA vs GLZS5BA)
                if model_number[:9] in line or model_number.replace('GLZS5', 'GLZ5S5') in line:
                    parts = line.split()
                    # Find the model number in parts and take next 3 values
                    for i, part in enumerate(parts):
                        if 'A*' in part and ('GLZS5BA' in part or 'GLZ5S5BA' in part):
                            # Dimensions are the next 3 parts after model number
                            if i + 3 < len(parts):
                                spec['width_in'] = parse_fraction(parts[i+1])
                                spec['depth_in'] = parse_fraction(parts[i+2])
                                spec['height_in'] = parse_fraction(parts[i+3])
                            elif i + 2 < len(parts):
                                # Handle line 7 case: parts are [numbers, model, dim1, dim2, dim3, numbers]
                                # Need to filter out non-dimension values
                                vals = []
                                for j in range(i+1, len(parts)):
                                    val = parse_fraction(parts[j])
                                    if val and 20 < val < 50:  # Reasonable dimension range
                                        vals.append(val)
                                    if len(vals) == 3:
                                        break
                                if len(vals) >= 3:
                                    spec['width_in'] = vals[0]
                                    spec['depth_in'] = vals[1]
                                    spec['height_in'] = vals[2]
                            break
                    break

    # Typical heat pump features
    spec['defrost_type'] = 'Demand'
    spec['low_ambient_cooling'] = '0°F'

    return spec


def main():
    """Main execution function."""
    print("=" * 70)
    print("15.2 SEER2 Spec Extraction")
    print("=" * 70)
    print("\nStep 1: Extracting outdoor units from PDFs...")
    print("-" * 70)

    all_specs = {}

    # Extract heat pumps
    print("\nExtracting Heat Pumps from GLZS5B.pdf...")
    for model in HEAT_PUMPS:
        try:
            spec = parse_heat_pump(HP_PDF, model)
            all_specs[model] = spec
            print(f"  ✓ {model}")
        except Exception as e:
            print(f"  ✗ ERROR: {model}: {e}")
            import traceback
            traceback.print_exc()

    # Extract AC condensers
    print("\nExtracting AC Condensers from GLXS5B.pdf...")
    for model in AC_CONDENSERS:
        try:
            spec = parse_ac_condenser(AC_PDF, model)
            all_specs[model] = spec
            print(f"  ✓ {model}")
        except Exception as e:
            print(f"  ✗ ERROR: {model}: {e}")
            import traceback
            traceback.print_exc()

    # Load and copy indoor equipment from 13-4-specs.json
    print("\n" + "-" * 70)
    print("Step 2: Copying indoor equipment from 13-4-specs.json...")
    print("-" * 70)

    try:
        with open(INDOOR_SPECS, 'r') as f:
            indoor_specs = json.load(f)

        indoor_count = 0
        for model, spec in indoor_specs.items():
            all_specs[model] = spec
            indoor_count += 1

        print(f"✓ Copied {indoor_count} indoor equipment specs")
    except Exception as e:
        print(f"✗ ERROR loading indoor specs: {e}")
        import traceback
        traceback.print_exc()

    # Write output
    print("\n" + "-" * 70)
    print(f"Step 3: Writing combined specs to {OUTPUT_FILE}...")
    print("-" * 70)

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_specs, f, indent=2)

    print(f"✓ Complete! Output written to {OUTPUT_FILE}")
    print(f"\nTotal equipment specs: {len(all_specs)}")
    print(f"  - Outdoor units (extracted): {len(HEAT_PUMPS) + len(AC_CONDENSERS)}")
    print(f"  - Indoor units (copied): {len(all_specs) - len(HEAT_PUMPS) - len(AC_CONDENSERS)}")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
