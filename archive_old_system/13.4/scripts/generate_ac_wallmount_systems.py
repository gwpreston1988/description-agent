#!/usr/bin/env python3
"""
Generate AC + Wall-Mounted Air Handler System descriptions for Goodman R-32 systems
"""

import json
import os

# Load the JSON data
with open('../13.4_specs.json', 'r') as f:
    specs_data = json.load(f)

# Output directory
output_dir = '../descriptions'

# System combinations (AC + Wall-Mounted Air Handler)
# Note: JSON has 'A' suffix on wall-mount models
systems = [
    ('GLXS3BN1810', 'AWST18SU1305A'),  # 1.5 ton, 5kW heat
    ('GLXS3BN2410', 'AWST24SU1305A'),  # 2.0 ton, 5kW heat
    ('GLXS3BN3010', 'AWST30LU1308A'),  # 2.5 ton, 8kW heat
    ('GLXS3BN3010', 'AWST30LU1310A'),  # 2.5 ton, 10kW heat
    ('GLXS3BN3610', 'AWST36LU1308A'),  # 3.0 ton, 8kW heat
    ('GLXS3BN3610', 'AWST36LU1310A'),  # 3.0 ton, 10kW heat
]

def format_fraction(decimal):
    """Convert decimal to fraction string"""
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

def format_tonnage(tonnage):
    """Format tonnage for display"""
    if tonnage == int(tonnage):
        return str(int(tonnage))
    return str(tonnage)

def generate_wallmount_system_description(ac_data, ah_data):
    """Generate complete wall-mount system description HTML"""

    # AC specs
    ac_model = ac_data['model_number']
    ac_tonnage = format_tonnage(ac_data['tonnage'])
    ac_cooling = ac_data['cooling_capacity_btuh']
    ac_seer2 = ac_data['seer2']
    ac_compressor = ac_data['compressor_type']
    ac_voltage = ac_data['voltage']
    ac_phase = ac_data['phase']
    ac_freq = ac_data['frequency_hz']
    ac_mca = ac_data['mca']
    ac_mop = ac_data['mop']
    ac_charge = ac_data['factory_charge_oz']
    ac_liquid = format_fraction(ac_data['liquid_line_od_in'])
    ac_suction = format_fraction(ac_data['suction_line_od_in'])
    ac_sound = ac_data['sound_level_dba']
    ac_height = ac_data['height_in']
    ac_width = ac_data['width_in']
    ac_depth = ac_data['depth_in']
    ac_weight = ac_data['shipping_weight_lb']

    # Air Handler specs
    ah_model = ah_data['model_number']
    ah_tonnage = format_tonnage(ah_data['tonnage'])
    ah_motor = ah_data['blower_motor_type']
    ah_voltage = ah_data['voltage']
    ah_phase = ah_data['phase']
    ah_freq = ah_data['frequency_hz']
    ah_mca = ah_data['mca']
    ah_mop = ah_data['mop']
    ah_height = ah_data['height_in']
    ah_width = ah_data['width_in']
    ah_depth = ah_data['depth_in']
    ah_weight = ah_data['shipping_weight_lb']
    ah_heat_kw = ah_data['included_heat_kit_kw']
    ah_heat_btuh = ah_data['included_heat_kit_btuh']

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GOODMAN {ac_tonnage} Ton 13.4 SEER2 R-32 Air Conditioning System with Wall-Hung Air Handler</title>
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

        #product-container h3 {{
            font-size: 1.4em;
            color: #57A9F9;
            margin: 25px 0 12px 0;
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

        .tab-container {{
            margin: 30px 0;
        }}

        .tab-buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .tab-button {{
            padding: 12px 24px;
            background: #f8f9fa;
            border: 2px solid #D53938;
            color: #D53938;
            cursor: pointer;
            border-radius: 5px;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .tab-button:hover {{
            background: #D53938;
            color: white;
        }}

        .tab-button.active {{
            background: #D53938;
            color: white;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
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

            .tab-buttons {{
                flex-direction: column;
            }}

            .tab-button {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div id="product-container">
        <h1>GOODMAN {ac_tonnage} Ton 13.4 SEER2 R-32 Air Conditioning System with Wall-Hung Air Handler</h1>

        <div class="intro-section">
            <p>Experience superior comfort cooling with this complete Goodman {ac_tonnage}-ton air conditioning system featuring a space-saving wall-hung air handler with integrated electric heat. This matched system combines a high-efficiency 13.4 SEER2 air conditioner with a wall-mounted air handler that includes a {ah_heat_kw}kW electric heat kit for reliable winter heating. Perfect for homes where floor space is limited, this system delivers efficient cooling and heating with environmentally-friendly R-32 refrigerant while maximizing your usable living space.</p>
        </div>

        <h2>Technical Specifications</h2>

        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="showTab(event, 'ac-specs')">Air Conditioner</button>
                <button class="tab-button" onclick="showTab(event, 'airhandler-specs')">Wall-Hung Air Handler</button>
            </div>

            <div id="ac-specs" class="tab-content active">
                <h3>Air Conditioner — {ac_model} Specifications</h3>
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
                            <td>Goodman</td>
                        </tr>
                        <tr>
                            <td><strong>Model Number</strong></td>
                            <td>{ac_model}</td>
                        </tr>
                        <tr>
                            <td><strong>Series</strong></td>
                            <td>Classic</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Air Conditioner Condenser</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage</strong></td>
                            <td>{ac_tonnage} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity</strong></td>
                            <td>{ac_cooling:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>SEER2 Rating</strong></td>
                            <td>13.4</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Type</strong></td>
                            <td>R-32</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Charge</strong></td>
                            <td>{int(ac_charge)} oz</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor Type</strong></td>
                            <td>{ac_compressor}</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage/Phase/Frequency</strong></td>
                            <td>{ac_voltage}V-{ac_phase}-{ac_freq}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{ac_mca} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{int(ac_mop)} A</td>
                        </tr>
                        <tr>
                            <td><strong>Sound Level</strong></td>
                            <td>{ac_sound} dBA</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Line Size</strong></td>
                            <td>{ac_liquid}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Line Size</strong></td>
                            <td>{ac_suction}</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{int(ac_width)}" × {int(ac_depth)}" × {ac_height}"</td>
                        </tr>
                        <tr>
                            <td><strong>Shipping Weight</strong></td>
                            <td>{int(ac_weight)} lbs</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div id="airhandler-specs" class="tab-content">
                <h3>Wall-Hung Air Handler — {ah_model} Specifications</h3>
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
                            <td>Goodman</td>
                        </tr>
                        <tr>
                            <td><strong>Model Number</strong></td>
                            <td>{ah_model}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Wall-Mounted Air Handler</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage</strong></td>
                            <td>{ah_tonnage} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Type</strong></td>
                            <td>R-32 Compatible</td>
                        </tr>
                        <tr>
                            <td><strong>Blower Motor Type</strong></td>
                            <td>{ah_motor}</td>
                        </tr>
                        <tr>
                            <td><strong>Metering Device</strong></td>
                            <td>TXV (Thermal Expansion Valve)</td>
                        </tr>
                        <tr>
                            <td><strong>Mounting Type</strong></td>
                            <td>Wall-Mounted</td>
                        </tr>
                        <tr>
                            <td><strong>Integrated Electric Heat Kit</strong></td>
                            <td>{ah_heat_kw} kW ({ah_heat_btuh:,} BTU/h)</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage/Phase/Frequency</strong></td>
                            <td>{ah_voltage}V-{ah_phase}-{ah_freq}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{ah_mca} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{ah_mop} A</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{int(ah_width)}" × {int(ah_depth)}" × {int(ah_height)}"</td>
                        </tr>
                        <tr>
                            <td><strong>Shipping Weight</strong></td>
                            <td>{int(ah_weight)} lbs</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

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
                    <h3>DOE Compliant for Northern Regions</h3>
                    <p>This complete R-32 13.4 SEER2 air conditioning system meets Department of Energy efficiency requirements for residential HVAC installations in Northern U.S. climate zones</p>
                </div>
            </div>
            <p style="margin-top: 20px; text-align: center; color: #666; font-size: 0.9em;"><strong>Important:</strong> Check state and local codes and ordinances before purchasing. Product availability and compliance requirements may vary by region.</p>
        </div>
    </div>

    <script>
        function showTab(event, tabId) {{
            // Hide all tab contents
            const tabContents = document.getElementsByClassName('tab-content');
            for (let content of tabContents) {{
                content.classList.remove('active');
            }}

            // Remove active class from all buttons
            const tabButtons = document.getElementsByClassName('tab-button');
            for (let button of tabButtons) {{
                button.classList.remove('active');
            }}

            // Show the selected tab and mark button as active
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}
    </script>
</body>
</html>"""

    return html

# Generate wall-mount system descriptions
generated_files = []
for ac_model, ah_model in systems:
    ac_data = specs_data[ac_model]
    ah_data = specs_data[ah_model]

    html_content = generate_wallmount_system_description(ac_data, ah_data)

    filename = f"Goodman_R32_AC_WallMount_System_{ac_model}_{ah_model.replace('A', '')}.html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as f:
        f.write(html_content)

    generated_files.append(filename)
    tonnage = format_tonnage(ac_data['tonnage'])
    heat_kw = ah_data['included_heat_kit_kw']
    print(f"Generated: {tonnage} ton with {heat_kw}kW heat - {ac_model} + {ah_model}")

print(f"\n✓ Successfully generated {len(generated_files)} AC + Wall-Mount system descriptions")
