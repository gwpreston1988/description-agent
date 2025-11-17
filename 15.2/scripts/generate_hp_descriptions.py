#!/usr/bin/env python3
"""
Generate product descriptions for Goodman 15.2 SEER2 R-410A Heat Pump units
"""

import json
import os

# Load the JSON data
with open('../15.2_specs.json', 'r') as f:
    specs_data = json.load(f)

# Output directory
output_dir = '../descriptions'

# HTML template function
def generate_hp_description(model_data):
    model_number = model_data['model_number']
    brand = model_data['brand']
    tonnage = model_data['tonnage']
    cooling_capacity = model_data['cooling_capacity_btuh']
    heating_capacity = model_data['heating_capacity_btuh']
    seer2 = model_data['seer2']
    refrigerant = "R-410A"  # Always R-410A for 15.2 SEER2
    compressor = model_data['compressor_type']
    defrost_type = model_data['defrost_type']
    low_ambient = model_data['low_ambient_cooling']
    voltage = model_data['voltage']
    phase = model_data['phase']
    frequency = model_data['frequency_hz']
    mca = model_data['mca']
    mop = model_data['mop']
    charge = model_data['factory_charge_oz']
    liquid_line = model_data['liquid_line_od_in']
    suction_line = model_data['suction_line_od_in']
    sound_level = model_data['sound_level_dba']
    height = model_data['height_in']
    width = model_data['width_in']
    depth = model_data['depth_in']
    weight = model_data['shipping_weight_lb']

    # Format tonnage
    tonnage_str = f"{tonnage}"
    if tonnage == int(tonnage):
        tonnage_str = str(int(tonnage))

    # Format line sizes as fractions
    def format_fraction(decimal):
        if decimal == 0.375:
            return "⅜\""
        elif decimal == 0.75:
            return "¾\""
        elif decimal == 0.875:
            return "⅞\""
        elif decimal == 1.125:
            return "1⅛\""
        else:
            return f"{decimal}\""

    liquid_line_str = format_fraction(liquid_line)
    suction_line_str = format_fraction(suction_line)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Goodman {model_number} {tonnage_str} Ton 15.2 SEER2 Heat Pump</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        #product-container {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #000;
            background: #fff;
        }}

        #product-container h1 {{
            font-size: 2.5em;
            color: #D53938;
            margin-bottom: 10px;
            padding-bottom: 15px;
            border-bottom: 3px solid #D53938;
            font-weight: 700;
        }}

        #product-container h2 {{
            font-size: 1.8em;
            color: #D53938;
            margin: 30px 0 15px 0;
            font-weight: 600;
        }}

        #product-container p {{
            line-height: 1.8;
            margin-bottom: 15px;
            font-size: 1.05em;
            color: #333;
        }}

        .intro-section {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 8px;
            margin: 25px 0;
            border-left: 5px solid #D53938;
        }}

        .specs-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        .specs-table thead {{
            background: linear-gradient(135deg, #D53938 0%, #b32d2c 100%);
            color: white;
        }}

        .specs-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1.1em;
        }}

        .specs-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}

        .specs-table tbody tr {{
            background: #fff;
            transition: all 0.3s ease;
        }}

        .specs-table tbody tr:nth-child(even) {{
            background: #f8f9fa;
        }}

        .specs-table tbody tr:hover {{
            background: linear-gradient(90deg, #D53938 0%, #b32d2c 100%) !important;
            color: white;
            transform: scale(1.01);
            box-shadow: 0 4px 12px rgba(213, 57, 56, 0.3);
        }}

        .specs-table tbody tr:hover td {{
            color: white;
        }}

        .warranty-section {{
            background: linear-gradient(135deg, #F8F9FA 0%, #e9ecef 100%);
            padding: 50px 30px;
            border-radius: 15px;
            margin: 50px 0;
        }}

        .warranty-section h2 {{
            color: #D53938;
            text-align: center;
            margin-bottom: 40px;
            font-size: 28px;
        }}

        .warranty-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            max-width: 800px;
            margin: 0 auto;
        }}

        .warranty-card {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            border: 2px solid rgba(213,57,56,0.3);
            transition: all 0.3s ease;
        }}

        .warranty-card:hover {{
            background: rgba(213,57,56,0.05);
            border-color: #D53938;
            transform: translateY(-5px);
        }}

        .warranty-years {{
            font-size: 48px;
            font-weight: 700;
            color: #D53938;
        }}

        .warranty-label {{
            color: #333;
            font-size: 14px;
            font-weight: 600;
        }}

        .cta-section {{
            background: linear-gradient(135deg, #F8F9FA 0%, #e9ecef 100%);
            padding: 60px 30px;
            border-radius: 15px;
            margin-top: 50px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}

        .cta-content {{
            text-align: center;
            margin-bottom: 40px;
        }}

        .cta-section h2 {{
            color: #D53938;
            margin: 0 0 15px 0;
            font-size: 28px;
            font-weight: 700;
        }}

        .cta-section p {{
            color: #333;
            margin: 0;
            font-size: 16px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }}

        .compliance-badge {{
            background: rgba(213,57,56,0.05);
            border: 2px solid #D53938;
            border-radius: 12px;
            padding: 25px 30px;
            display: flex;
            align-items: center;
            gap: 20px;
            max-width: 700px;
            margin: 0 auto;
            transition: all 0.3s ease;
        }}

        .compliance-badge:hover {{
            background: rgba(87,169,249,0.05);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(213,57,56,0.2);
        }}

        .badge-icon {{
            font-size: 32px;
            color: #D53938;
            font-weight: 700;
            background: rgba(213,57,56,0.2);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .badge-content {{
            text-align: left;
        }}

        .badge-content h3 {{
            color: #D53938;
            margin: 0 0 8px 0;
            font-size: 18px;
            font-weight: 700;
        }}

        .badge-content p {{
            color: #555;
            margin: 0;
            font-size: 14px;
            line-height: 1.5;
        }}

        @media (max-width: 768px) {{
            #product-container {{
                padding: 15px;
            }}

            #product-container h1 {{
                font-size: 1.8em;
            }}

            #product-container h2 {{
                font-size: 1.4em;
            }}

            .specs-table {{
                font-size: 0.9em;
            }}

            .specs-table th,
            .specs-table td {{
                padding: 10px;
            }}

            .cta-section {{
                padding: 40px 20px;
            }}

            .compliance-badge {{
                flex-direction: column;
                text-align: center;
                padding: 20px;
            }}

            .badge-content {{
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div id="product-container">
        <h1>GOODMAN {tonnage_str} Ton 15.2 SEER2 R-410A Heat Pump — {model_number}</h1>

        <div class="intro-section">
            <p>The Goodman {model_number} is a high-efficiency {tonnage_str}-ton heat pump condenser, delivering 15.2 SEER2 cooling performance and reliable heating operation. Featuring a {compressor} compressor, {defrost_type} defrost control, and R-410A refrigerant, this unit provides year-round comfort with consistent heating and cooling efficiency for residential applications.</p>
        </div>

        <h2>Technical Specifications</h2>
        <table class="specs-table">
            <thead>
                <tr>
                    <th>Specification</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Manufacturer</strong></td>
                    <td>{brand}</td>
                </tr>
                <tr>
                    <td><strong>Model Number</strong></td>
                    <td>{model_number}</td>
                </tr>
                <tr>
                    <td><strong>Product Type</strong></td>
                    <td>Heat Pump Condenser</td>
                </tr>
                <tr>
                    <td><strong>Tonnage</strong></td>
                    <td>{tonnage_str} Ton</td>
                </tr>
                <tr>
                    <td><strong>Cooling Capacity</strong></td>
                    <td>{cooling_capacity:,} BTU/h</td>
                </tr>
                <tr>
                    <td><strong>Heating Capacity</strong></td>
                    <td>{heating_capacity:,} BTU/h</td>
                </tr>
                <tr>
                    <td><strong>SEER2 Rating</strong></td>
                    <td>{seer2}</td>
                </tr>
                <tr>
                    <td><strong>Refrigerant Type</strong></td>
                    <td>{refrigerant}</td>
                </tr>
                <tr>
                    <td><strong>Refrigerant Charge</strong></td>
                    <td>{int(charge)} oz</td>
                </tr>
                <tr>
                    <td><strong>Compressor Type</strong></td>
                    <td>{compressor}</td>
                </tr>
                <tr>
                    <td><strong>Defrost Type</strong></td>
                    <td>{defrost_type}</td>
                </tr>
                <tr>
                    <td><strong>Low Ambient Cooling</strong></td>
                    <td>{low_ambient}</td>
                </tr>
                <tr>
                    <td><strong>Voltage/Phase/Frequency</strong></td>
                    <td>{voltage}V-{phase}-{frequency}Hz</td>
                </tr>
                <tr>
                    <td><strong>Min Circuit Ampacity</strong></td>
                    <td>{mca} A</td>
                </tr>
                <tr>
                    <td><strong>Max Overcurrent Protection</strong></td>
                    <td>{int(mop)} A</td>
                </tr>
                <tr>
                    <td><strong>Sound Level</strong></td>
                    <td>{sound_level} dBA</td>
                </tr>
                <tr>
                    <td><strong>Liquid Line Size</strong></td>
                    <td>{liquid_line_str}</td>
                </tr>
                <tr>
                    <td><strong>Suction Line Size</strong></td>
                    <td>{suction_line_str}</td>
                </tr>
                <tr>
                    <td><strong>Dimensions (W×D×H)</strong></td>
                    <td>{int(width)}" × {int(depth)}" × {height}"</td>
                </tr>
                <tr>
                    <td><strong>Shipping Weight</strong></td>
                    <td>{int(weight)} lbs</td>
                </tr>
            </tbody>
        </table>

        <div class="warranty-section">
            <h2>Comprehensive Warranty Protection</h2>
            <div class="warranty-grid">
                <div class="warranty-card">
                    <div class="warranty-years">10</div>
                    <div class="warranty-label">Year Parts Warranty</div>
                </div>
                <div class="warranty-card">
                    <div class="warranty-years">10</div>
                    <div class="warranty-label">Year Compressor Warranty</div>
                </div>
            </div>
        </div>

        <div class="cta-section">
            <div class="cta-content">
                <h2>Professional Installation Required</h2>
                <p>Certified HVAC technician installation ensures optimal performance, safety compliance, and full warranty protection.</p>
            </div>
            <div class="compliance-badge">
                <div class="badge-icon">✓</div>
                <div class="badge-content">
                    <h3>DOE Compliant Nationwide</h3>
                    <p>This 15.2 SEER2 heat pump system meets Department of Energy efficiency requirements for residential HVAC installations across all U.S. climate zones</p>
                </div>
            </div>
            <p style="margin-top: 20px; text-align: center; color: #666; font-size: 0.9em;"><strong>Important:</strong> Check state and local codes and ordinances before purchasing. Product availability and compliance requirements may vary by region.</p>
        </div>
    </div>
</body>
</html>"""

    return html

def format_tonnage(tonnage):
    if tonnage == int(tonnage):
        return str(int(tonnage))
    return str(tonnage)

# Filter for Heat Pump condensers only (GLZS5BA series)
hp_models = {k: v for k, v in specs_data.items() if v['equipment_type'] == 'Heat Pump Condenser' and k.startswith('GLZS5BA')}

# Generate descriptions for each Heat Pump unit
generated_files = []
for model_number, model_data in hp_models.items():
    html_content = generate_hp_description(model_data)

    filename = f"Goodman_R410A_HP_{model_number}.html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as f:
        f.write(html_content)

    generated_files.append(filename)
    tonnage = format_tonnage(model_data['tonnage'])
    print(f"Generated: {tonnage} ton - {model_number}")

print(f"\n✓ Successfully generated {len(generated_files)} Heat Pump unit descriptions")
