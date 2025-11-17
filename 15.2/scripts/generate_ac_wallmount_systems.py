#!/usr/bin/env python3
import json
import os

# Load the specs data
with open('../15.2_specs.json', 'r') as f:
    specs = json.load(f)

# System combinations (AC + Wall-Mount Handler)
systems = [
    ('GLXS5BA1810', 'AWST18SU1305A'),  # 1.5 ton
    ('GLXS5BA2410', 'AWST24SU1305A'),  # 2.0 ton
    ('GLXS5BA3010', 'AWST30LU1308A'),  # 2.5 ton - 8kW
    ('GLXS5BA3010', 'AWST30LU1310A'),  # 2.5 ton - 10kW
    ('GLXS5BA3610', 'AWST36LU1308A'),  # 3.0 ton - 8kW
    ('GLXS5BA3610', 'AWST36LU1310A'),  # 3.0 ton - 10kW
]

def format_tonnage(tonnage):
    """Format tonnage to remove .0 for whole numbers"""
    if tonnage == int(tonnage):
        return str(int(tonnage))
    return str(tonnage)

def format_line_size(size_str):
    """Convert line size to fraction format"""
    conversions = {
        '0.375': '⅜"',
        '0.75': '¾"',
        '0.875': '⅞"',
        '1.125': '1⅛"'
    }
    return conversions.get(size_str, size_str + '"')

# JavaScript code stored separately to avoid f-string conflicts
JAVASCRIPT_CODE = """
    <script>
        function showTab(event, tabId) {
            // Hide all tab contents
            const tabContents = document.getElementsByClassName('tab-content');
            for (let i = 0; i < tabContents.length; i++) {
                tabContents[i].classList.remove('active');
            }
            
            // Remove active class from all tab buttons
            const tabButtons = document.getElementsByClassName('tab-button');
            for (let i = 0; i < tabButtons.length; i++) {
                tabButtons[i].classList.remove('active');
            }
            
            // Show the selected tab content
            document.getElementById(tabId).classList.add('active');
            
            // Add active class to the clicked button
            event.currentTarget.classList.add('active');
        }
        
        // Show first tab by default
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelector('.tab-button').click();
        });
    </script>
</body>
</html>
"""

# Generate HTML for each system
for ac_model, ah_model in systems:
    ac_data = specs[ac_model]
    ah_data = specs[ah_model]
    
    tonnage = ac_data['tonnage']
    tonnage_display = format_tonnage(tonnage)
    
    # Get specs
    ac_seer2 = ac_data['seer2']
    ac_eer2 = ac_data['eer2']
    ac_cooling_capacity = ac_data['cooling_capacity_btuh']
    ac_sound = ac_data['sound_level_dba']
    ac_voltage = ac_data['voltage']
    ac_refrigerant = "R-410A"
    ac_warranty = ac_data.get('warranty_years', '10')
    
    ah_airflow = ah_data['airflow_cfm']
    ah_esp = ah_data.get('esp_iwc', '0.5')
    ah_motor_hp = ah_data.get('motor_hp', ah_data.get('blower_motor_type', 'ECM'))
    ah_voltage_options = ah_data['voltage']
    ah_mounting = ah_data.get('mounting_type', 'Wall-Mounted')
    ah_heat_kw = ah_data.get('included_heat_kit_kw', 'N/A')
    ah_filter_size = ah_data.get('filter_size', 'Standard')
    ah_mop = ah_data['mop']
    ah_mocp = ah_data.get('mocp', ah_data.get('mca', 'N/A'))
    ah_warranty = ah_data.get('warranty_years', '10')
    
    # Line set
    liquid_line = format_line_size(str(ac_data['liquid_line_od_in']))
    suction_line = format_line_size(str(ac_data['suction_line_od_in']))
    
    # Filename
    filename = f"../descriptions/Goodman_{tonnage_display}Ton_R410A_AC_System_{ac_model}_{ah_model}.html"
    
    html_part1 = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GOODMAN {tonnage_display} Ton {ac_seer2} SEER2 R-410A Air Conditioning System with Wall-Hung Air Handler</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #D53938;
            font-size: 2em;
            margin-bottom: 20px;
            line-height: 1.3;
        }}
        
        h2 {{
            color: #333;
            font-size: 1.5em;
            margin-top: 30px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #D53938;
        }}
        
        .intro {{
            font-size: 1.1em;
            margin-bottom: 30px;
            color: #555;
        }}
        
        .doe-badge {{
            display: inline-block;
            background-color: #0066cc;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            margin: 20px 0;
        }}
        
        .tabs {{
            display: flex;
            gap: 10px;
            margin-top: 20px;
            border-bottom: 2px solid #D53938;
        }}
        
        .tab-button {{
            padding: 12px 24px;
            background-color: white;
            border: 2px solid #D53938;
            border-bottom: none;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
            border-radius: 4px 4px 0 0;
        }}
        
        .tab-button:hover {{
            background-color: #f5f5f5;
        }}
        
        .tab-button.active {{
            background-color: white;
            border-color: #D53938;
            border-bottom: 2px solid white;
            margin-bottom: -2px;
            font-weight: bold;
            color: #D53938;
        }}
        
        .tab-content {{
            display: none;
            padding: 20px 0;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .spec-table {{
            width: 100%;
            margin: 20px 0;
            border-collapse: collapse;
        }}
        
        .spec-table th {{
            background-color: #D53938;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        .spec-table td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        
        .spec-table tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        .spec-table td:first-child {{
            font-weight: 600;
            color: #555;
            width: 40%;
        }}
        
        .highlight {{
            background-color: #fff3cd;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 1.5em;
            }}
            
            .tabs {{
                flex-direction: column;
            }}
            
            .tab-button {{
                border: 2px solid #D53938;
                border-radius: 4px;
                margin-bottom: 5px;
            }}
            
            .tab-button.active {{
                margin-bottom: 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>GOODMAN {tonnage_display}.0 Ton Up to {ac_seer2} SEER2 R-410A Air Conditioning System with Wall-Hung Air Handler</h1>
        
        <div class="intro">
            <p>This complete Goodman air conditioning system combines a high-efficiency outdoor condenser with a space-saving wall-mounted air handler featuring integrated electric heat. Perfect for applications where traditional ductwork is not available or practical, this matched system delivers reliable cooling performance and supplemental heating.</p>
        </div>
        
        <div class="doe-badge">DOE Compliant - Nationwide</div>
        
        <h2>Technical Specifications</h2>
        
        <div class="tabs">
            <button class="tab-button" onclick="showTab(event, 'ac-specs')">Air Conditioner</button>
            <button class="tab-button" onclick="showTab(event, 'ah-specs')">Wall Air Handler</button>
            <button class="tab-button" onclick="showTab(event, 'lineset-specs')">Line Set</button>
        </div>
        
        <div id="ac-specs" class="tab-content">
            <table class="spec-table">
                <tr>
                    <th colspan="2">Air Conditioner Specifications - {ac_model}</th>
                </tr>
                <tr>
                    <td>Cooling Capacity</td>
                    <td>{ac_cooling_capacity:,} BTU/h</td>
                </tr>
                <tr>
                    <td>SEER2 Rating</td>
                    <td><span class="highlight">{ac_seer2}</span></td>
                </tr>
                <tr>
                    <td>EER2 Rating</td>
                    <td>{ac_eer2}</td>
                </tr>
                <tr>
                    <td>Refrigerant Type</td>
                    <td>{ac_refrigerant}</td>
                </tr>
                <tr>
                    <td>Sound Rating</td>
                    <td>{ac_sound} dB</td>
                </tr>
                <tr>
                    <td>Electrical</td>
                    <td>{ac_voltage}</td>
                </tr>
                <tr>
                    <td>Warranty</td>
                    <td>{ac_warranty}-Year Limited Warranty</td>
                </tr>
            </table>
        </div>
        
        <div id="ah-specs" class="tab-content">
            <table class="spec-table">
                <tr>
                    <th colspan="2">Wall Air Handler Specifications - {ah_model}</th>
                </tr>
                <tr>
                    <td>Airflow</td>
                    <td>{ah_airflow} CFM</td>
                </tr>
                <tr>
                    <td>Mounting Type</td>
                    <td>{ah_mounting}</td>
                </tr>
                <tr>
                    <td>External Static Pressure</td>
                    <td>{ah_esp} in. w.c.</td>
                </tr>
                <tr>
                    <td>Blower Motor</td>
                    <td>{ah_motor_hp} HP ECM Variable-Speed</td>
                </tr>
                <tr>
                    <td>Integrated Electric Heat</td>
                    <td>{ah_heat_kw} kW</td>
                </tr>
                <tr>
                    <td>Filter Size</td>
                    <td>{ah_filter_size}</td>
                </tr>
                <tr>
                    <td>Voltage Options</td>
                    <td>{ah_voltage_options}</td>
                </tr>
                <tr>
                    <td>MOP (Max Overcurrent Protection)</td>
                    <td>{ah_mop} A</td>
                </tr>
                <tr>
                    <td>MOCP (Min. Circuit Ampacity)</td>
                    <td>{ah_mocp} A</td>
                </tr>
                <tr>
                    <td>Warranty</td>
                    <td>{ah_warranty}-Year Limited Warranty</td>
                </tr>
            </table>
        </div>
        
        <div id="lineset-specs" class="tab-content">
            <table class="spec-table">
                <tr>
                    <th colspan="2">Refrigerant Line Set Requirements</th>
                </tr>
                <tr>
                    <td>Liquid Line Size</td>
                    <td>{liquid_line}</td>
                </tr>
                <tr>
                    <td>Suction Line Size</td>
                    <td>{suction_line}</td>
                </tr>
                <tr>
                    <td>Maximum Line Length</td>
                    <td>50 feet (consult installation manual)</td>
                </tr>
                <tr>
                    <td>Refrigerant Type</td>
                    <td>{ac_refrigerant}</td>
                </tr>
            </table>
        </div>
    </div>
"""
    
    # Combine HTML parts with JavaScript
    html = html_part1 + JAVASCRIPT_CODE
    
    # Create descriptions directory if it doesn't exist
    os.makedirs('../descriptions', exist_ok=True)
    
    # Write the HTML file
    with open(filename, 'w') as f:
        f.write(html)
    
    print(f"Generated: {filename}")

print(f"\nSuccessfully generated {len(systems)} AC + wall-mount system descriptions!")
