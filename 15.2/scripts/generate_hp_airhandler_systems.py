#!/usr/bin/env python3
import json
import os

with open('../15.2_specs.json', 'r') as f:
    specs = json.load(f)

systems = [
    ('GLZS5BA1810', 'AMST24BU13'),
    ('GLZS5BA2410', 'AMST24BU13'),
    ('GLZS5BA3010', 'AMST30BU13'),
    ('GLZS5BA3610', 'AMST36BU13'),
    ('GLZS5BA4210', 'AMST42CU13'),
    ('GLZS5BA4810', 'AMST48CU13'),
    ('GLZS5BA6010', 'AMST60DU13'),
]

def format_tonnage(tonnage):
    if tonnage == int(tonnage):
        return str(int(tonnage))
    return str(tonnage)

def format_line_size(size_str):
    conversions = {
        '0.375': '⅜"',
        '0.75': '¾"',
        '0.875': '⅞"',
        '1.125': '1⅛"'
    }
    return conversions.get(size_str, size_str + '"')

JAVASCRIPT_CODE = """
    <script>
        function showTab(event, tabId) {
            const tabContents = document.getElementsByClassName('tab-content');
            for (let i = 0; i < tabContents.length; i++) {
                tabContents[i].classList.remove('active');
            }
            
            const tabButtons = document.getElementsByClassName('tab-button');
            for (let i = 0; i < tabButtons.length; i++) {
                tabButtons[i].classList.remove('active');
            }
            
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }
    </script>
</body>
</html>
"""

for hp_model, ah_model in systems:
    hp_data = specs[hp_model]
    ah_data = specs[ah_model]
    
    tonnage = hp_data['tonnage']
    tonnage_display = format_tonnage(tonnage)
    
    hp_seer2 = hp_data['seer2']
    hp_eer2 = hp_data.get('eer2', 'N/A')
    hp_hspf2 = hp_data['hspf2']
    hp_cooling = hp_data['cooling_capacity_btuh']
    hp_heating = hp_data['heating_capacity_btuh']
    hp_compressor = hp_data['compressor_type']
    hp_voltage = hp_data['voltage']
    hp_phase = hp_data['phase']
    hp_freq = hp_data['frequency_hz']
    hp_mca = hp_data['mca']
    hp_mop = hp_data['mop']
    hp_charge = hp_data['factory_charge_oz']
    hp_sound = hp_data['sound_level_dba']
    hp_height = hp_data['height_in']
    hp_width = hp_data['width_in']
    hp_depth = hp_data['depth_in']
    hp_weight = hp_data['shipping_weight_lb']
    
    ah_motor = ah_data['blower_motor_type']
    ah_motor_hp = ah_data.get('motor_hp', 'N/A')
    ah_voltage = ah_data['voltage']
    ah_phase = ah_data['phase']
    ah_freq = ah_data['frequency_hz']
    ah_mca = ah_data['mca']
    ah_mop = ah_data['mop']
    ah_height = ah_data['height_in']
    ah_width = ah_data['width_in']
    ah_depth = ah_data['depth_in']
    ah_weight = ah_data['shipping_weight_lb']
    ah_airflow = ah_data['airflow_cfm']
    
    liquid_line = format_line_size(str(hp_data['liquid_line_od_in']))
    suction_line = format_line_size(str(hp_data['suction_line_od_in']))
    
    filename = f"../descriptions/Goodman_{tonnage_display}Ton_R410A_HP_System_{hp_model}_{ah_model}.html"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GOODMAN {tonnage_display} Ton 15.2 SEER2 R-410A Heat Pump System with Multi-Positional Air Handler</title>
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
            border: 2px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            color: #333;
            transition: all 0.3s ease;
        }}

        .tab-button:hover {{
            background: #e9ecef;
            border-color: #57A9F9;
        }}

        .tab-button.active {{
            background: linear-gradient(135deg, #D53938 0%, #b32d2c 100%);
            color: white;
            border-color: #D53938;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
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

            .compliance-badge {{
                flex-direction: column;
                text-align: center;
                padding: 20px;
            }}

            .badge-content {{
                text-align: center;
            }}

            .cta-section {{
                padding: 40px 20px;
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
        <h1>GOODMAN {tonnage_display} Ton 15.2 SEER2 R-410A Heat Pump System with Multi-Positional Air Handler</h1>

        <div class="intro-section">
            <p>Experience year-round comfort with this premium Goodman {tonnage_display}-ton R-410A 15.2 SEER2 heat pump system. This complete matched system combines a high-efficiency heat pump outdoor unit with a versatile multi-positional air handler. Designed for reliable heating and cooling performance, this system delivers exceptional energy efficiency, quiet operation, and dependable comfort with R-410A refrigerant.</p>
        </div>

        <h2>Technical Specifications</h2>

        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="showTab(event, 'hp-specs')">Heat Pump</button>
                <button class="tab-button" onclick="showTab(event, 'airhandler-specs')">Air Handler</button>
            </div>

            <div id="hp-specs" class="tab-content active">
                <h3>Heat Pump — {hp_model} Specifications</h3>
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
                            <td><strong>Tonnage</strong></td>
                            <td>{tonnage_display} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant</strong></td>
                            <td>R-410A</td>
                        </tr>
                        <tr>
                            <td><strong>SKU/Model No</strong></td>
                            <td>{hp_model}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Split System Heat Pump</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity</strong></td>
                            <td>{hp_cooling:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>Heating Capacity (47°F)</strong></td>
                            <td>{hp_heating:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>SEER2 Rating</strong></td>
                            <td>Up to {hp_seer2}</td>
                        </tr>
                        <tr>
                            <td><strong>EER2 Rating</strong></td>
                            <td>{hp_eer2}</td>
                        </tr>
                        <tr>
                            <td><strong>HSPF2 Rating</strong></td>
                            <td>{hp_hspf2}</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor Type</strong></td>
                            <td>{hp_compressor}</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage</strong></td>
                            <td>{hp_voltage}V / {hp_phase}Ph / {hp_freq}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{hp_mca} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{int(hp_mop)} A</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Line Size</strong></td>
                            <td>{liquid_line}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Line Size</strong></td>
                            <td>{suction_line}</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Charge</strong></td>
                            <td>{int(hp_charge)} oz</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (H×W×D)</strong></td>
                            <td>{hp_height}" × {int(hp_width)}" × {int(hp_depth)}"</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{int(hp_weight)} lbs</td>
                        </tr>
                        <tr>
                            <td><strong>Sound Level</strong></td>
                            <td>{hp_sound} dBA</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div id="airhandler-specs" class="tab-content">
                <h3>Air Handler — {ah_model} Specifications</h3>
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
                            <td><strong>Tonnage</strong></td>
                            <td>{tonnage_display} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant</strong></td>
                            <td>R-410A Compatible</td>
                        </tr>
                        <tr>
                            <td><strong>SKU/Model No</strong></td>
                            <td>{ah_model}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Multi-Positional Air Handler</td>
                        </tr>
                        <tr>
                            <td><strong>Motor Type</strong></td>
                            <td>{ah_motor}</td>
                        </tr>
                        <tr>
                            <td><strong>Motor HP</strong></td>
                            <td>{ah_motor_hp} HP</td>
                        </tr>
                        <tr>
                            <td><strong>Nominal Cooling Capacity</strong></td>
                            <td>{hp_cooling:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>Airflow</strong></td>
                            <td>{ah_airflow} CFM</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage</strong></td>
                            <td>{ah_voltage}V / {ah_phase}Ph / {ah_freq}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{ah_mca} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Device</strong></td>
                            <td>{ah_mop} A</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Line Connection</strong></td>
                            <td>{liquid_line}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Line Connection</strong></td>
                            <td>{suction_line}</td>
                        </tr>
                        <tr>
                            <td><strong>Metering Device</strong></td>
                            <td>TXV (Internal)</td>
                        </tr>
                        <tr>
                            <td><strong>Cabinet Configuration</strong></td>
                            <td>Multi-Positional (B Cabinet)</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (H×W×D)</strong></td>
                            <td>{ah_height}" × {ah_width}" × {ah_depth}"</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
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
            <p style="margin-top: 30px; text-align: center; color: #666; font-size: 0.95em;"><strong>Note:</strong> Warranty terms and conditions apply. Unit must be registered within 60 days of installation for full coverage.</p>
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
                    <p>This complete R-410A 15.2 SEER2 heat pump system meets Department of Energy efficiency requirements for residential HVAC installations across all U.S. climate zones</p>
                </div>
            </div>
            <p style="margin-top: 20px; text-align: center; color: #666; font-size: 0.9em;"><strong>Important:</strong> Check state and local codes and ordinances before purchasing. Product availability and compliance requirements may vary by region.</p>
        </div>
    </div>
"""
    
    html += JAVASCRIPT_CODE
    
    os.makedirs('../descriptions', exist_ok=True)
    
    with open(filename, 'w') as f:
        f.write(html)
    
    print(f"Generated: {filename}")

print(f"\nSuccessfully generated {len(systems)} heat pump + air handler system descriptions!")
