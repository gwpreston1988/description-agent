#!/usr/bin/env python3
"""
Generate all remaining 80% AFUE system descriptions
"""
import json
from pathlib import Path

# Load specs
with open('14.3_specs.json', 'r') as f:
    specs = json.load(f)

OUTPUT_DIR = Path("Description Directory")

# Tonnage mapping for filenames
TONNAGE_MAP = {1.5: "15Ton", 2: "2Ton", 2.5: "25Ton", 3: "3Ton", 3.5: "35Ton", 4: "4Ton", 5: "5Ton"}

# AC specs (complete from JSON analysis)
AC_SPECS = {
    "GLXS4BA1810": {"tonnage": 1.5, "btu": 18000, "seer2": 14.3, "compressor_type": "Single-Stage Rotary", "compressor_rla": 8.0, "compressor_lra": 40.0, "fan_motor": "PSC (1/6 HP)", "fan_fla": 1.00, "mca": 11.3, "mocp": 15, "sound": 72.0, "dimensions": "28\" × 28\" × 28\"", "weight": 95, "refrigerant_oz": 68, "liquid_line": "⅜\"", "suction_line": "¾\""},
    "GLXS4BA2410": {"tonnage": 2, "btu": 24000, "seer2": 14.3, "compressor_type": "Single-Stage Rotary", "compressor_rla": 8.0, "compressor_lra": 40.0, "fan_motor": "PSC (1/6 HP)", "fan_fla": 1.00, "mca": 11.3, "mocp": 15, "sound": 74.0, "dimensions": "27\" × 26\" × 26\"", "weight": 121, "refrigerant_oz": 68, "liquid_line": "⅜\"", "suction_line": "¾\""},
    "GLXS4BA3010": {"tonnage": 2.5, "btu": 30000, "seer2": 14.3, "compressor_type": "Single-Stage Rotary", "compressor_rla": 10.2, "compressor_lra": 51.0, "fan_motor": "PSC (1/5 HP)", "fan_fla": 1.10, "mca": 14.1, "mocp": 20, "sound": 71.0, "dimensions": "32\" × 29\" × 29\"", "weight": 151, "refrigerant_oz": 88, "liquid_line": "⅜\"", "suction_line": "¾\""},
    "GLXS4BA3610": {"tonnage": 3, "btu": 36000, "seer2": 14.3, "compressor_type": "Single-Stage Scroll", "compressor_rla": 14.1, "compressor_lra": 71.0, "fan_motor": "PSC (1/4 HP)", "fan_fla": 1.40, "mca": 19.2, "mocp": 25, "sound": 67.0, "dimensions": "39½\" × 29\" × 29\"", "weight": 165, "refrigerant_oz": 112, "liquid_line": "⅜\"", "suction_line": "⅞\""},
    "GLXS4BA4210": {"tonnage": 3.5, "btu": 42000, "seer2": 14.3, "compressor_type": "Single-Stage Scroll", "compressor_rla": 17.9, "compressor_lra": 90.0, "fan_motor": "PSC (1/3 HP)", "fan_fla": 1.80, "mca": 24.4, "mocp": 30, "sound": 73.0, "dimensions": "35¾\" × 35½\" × 35½\"", "weight": 235, "refrigerant_oz": 144, "liquid_line": "⅜\"", "suction_line": "1⅛\""},
    "GLXS4BA4810": {"tonnage": 4, "btu": 48000, "seer2": 14.3, "compressor_type": "Single-Stage Scroll", "compressor_rla": 20.4, "compressor_lra": 102.0, "fan_motor": "PSC (1/3 HP)", "fan_fla": 1.80, "mca": 27.7, "mocp": 35, "sound": 73.0, "dimensions": "35¾\" × 35½\" × 35½\"", "weight": 245, "refrigerant_oz": 156, "liquid_line": "⅜\"", "suction_line": "⅞\""},
    "GLXS4BA6010": {"tonnage": 5, "btu": 60000, "seer2": 14.3, "compressor_type": "Single-Stage Scroll", "compressor_rla": 24.7, "compressor_lra": 123.0, "fan_motor": "PSC (1/3 HP)", "fan_fla": 1.80, "mca": 33.4, "mocp": 40, "sound": 76.0, "dimensions": "39½\" × 35½\" × 35½\"", "weight": 260, "refrigerant_oz": 180, "liquid_line": "⅜\"", "suction_line": "⅞\""},
}

# Heat Pump specs
HP_SPECS = {
    "GLZS4BA1810": {"tonnage": 1.5, "btu": 18000, "seer2": 14.3, "hspf2": 7.5, "compressor_type": "Single-Stage Rotary", "compressor_rla": 8.2, "compressor_lra": 41.2, "fan_motor": "PSC (1/6 HP)", "fan_fla": 0.95, "mca": 11.2, "mocp": 15, "sound": 74.0, "dimensions": "32½\" × 29\" × 29\"", "weight": 150, "refrigerant_oz": 70, "liquid_line": "⅜\"", "suction_line": "¾\""},
    "GLZS4BA2410": {"tonnage": 2, "btu": 24000, "seer2": 14.3, "hspf2": 7.5, "compressor_type": "Single-Stage Rotary", "compressor_rla": 8.2, "compressor_lra": 41.2, "fan_motor": "PSC (1/6 HP)", "fan_fla": 0.95, "mca": 11.2, "mocp": 15, "sound": 74.0, "dimensions": "32½\" × 29\" × 29\"", "weight": 150, "refrigerant_oz": 70, "liquid_line": "⅜\"", "suction_line": "¾\""},
    "GLZS4BA3010": {"tonnage": 2.5, "btu": 30000, "seer2": 14.3, "hspf2": 7.5, "compressor_type": "Single-Stage Rotary", "compressor_rla": 10.2, "compressor_lra": 51.0, "fan_motor": "PSC (1/5 HP)", "fan_fla": 1.10, "mca": 14.1, "mocp": 20, "sound": 77.0, "dimensions": "39½\" × 29\" × 29\"", "weight": 190, "refrigerant_oz": 88, "liquid_line": "⅜\"", "suction_line": "¾\""},
    "GLZS4BA3610": {"tonnage": 3, "btu": 36000, "seer2": 14.3, "hspf2": 7.5, "compressor_type": "Single-Stage Scroll", "compressor_rla": 14.1, "compressor_lra": 71.0, "fan_motor": "PSC (1/4 HP)", "fan_fla": 1.40, "mca": 19.2, "mocp": 25, "sound": 75.0, "dimensions": "35¾\" × 35½\" × 35½\"", "weight": 211, "refrigerant_oz": 112, "liquid_line": "⅜\"", "suction_line": "⅞\""},
    "GLZS4BA4210": {"tonnage": 3.5, "btu": 42000, "seer2": 14.3, "hspf2": 7.5, "compressor_type": "Single-Stage Scroll", "compressor_rla": 17.9, "compressor_lra": 90.0, "fan_motor": "PSC (1/3 HP)", "fan_fla": 1.80, "mca": 24.4, "mocp": 30, "sound": 72.0, "dimensions": "35¾\" × 35½\" × 35½\"", "weight": 277, "refrigerant_oz": 144, "liquid_line": "⅜\"", "suction_line": "1⅛\""},
    "GLZS4BA4810": {"tonnage": 4, "btu": 48000, "seer2": 14.3, "hspf2": 7.5, "compressor_type": "Single-Stage Scroll", "compressor_rla": 20.4, "compressor_lra": 102.0, "fan_motor": "PSC (1/3 HP)", "fan_fla": 1.80, "mca": 27.7, "mocp": 35, "sound": 74.0, "dimensions": "36½\" × 35½\" × 35½\"", "weight": 284, "refrigerant_oz": 156, "liquid_line": "⅜\"", "suction_line": "1⅛\""},
    "GLZS4BA6010": {"tonnage": 5, "btu": 60000, "seer2": 14.3, "hspf2": 7.5, "compressor_type": "Single-Stage Scroll", "compressor_rla": 24.7, "compressor_lra": 123.0, "fan_motor": "PSC (1/3 HP)", "fan_fla": 1.80, "mca": 33.4, "mocp": 40, "sound": 75.0, "dimensions": "39½\" × 35½\" × 35½\"", "weight": 309, "refrigerant_oz": 180, "liquid_line": "⅜\"", "suction_line": "1⅛\""},
}

# 80% Furnace specs
FURNACE_80 = {
    "GR9S800403ANA": {"btu_input": 40000, "btu_output": 32000, "cabinet_width": "14.5\"", "dimensions": "14.5\" × 28\" × 33\"", "weight": 120, "blower_hp": "¾", "blower_size": "10\" × 8\"", "num_burners": 4, "temp_rise": "35–65°F", "vent_diameter": "3\"", "mca": 13.0, "mocp": 15},
    "GR9S800603ANA": {"btu_input": 60000, "btu_output": 48000, "cabinet_width": "17.5\"", "dimensions": "17.5\" × 28\" × 33⅜\"", "weight": 108, "blower_hp": "¾", "blower_size": "10\" × 8\"", "num_burners": 4, "temp_rise": "45–75°F", "vent_diameter": "3\"", "mca": 13.0, "mocp": 15},
    "GR9S800604BNA": {"btu_input": 60000, "btu_output": 48000, "cabinet_width": "17.5\"", "dimensions": "17.5\" × 28\" × 33⅜\"", "weight": 108, "blower_hp": "¾", "blower_size": "10\" × 8\"", "num_burners": 4, "temp_rise": "45–75°F", "vent_diameter": "3\"", "mca": 13.0, "mocp": 15},
    "GR9S800804CNA": {"btu_input": 80000, "btu_output": 64000, "cabinet_width": "21\"", "dimensions": "21\" × 28\" × 33⅜\"", "weight": 132, "blower_hp": "¾", "blower_size": "10\" × 10\"", "num_burners": 4, "temp_rise": "45–75°F", "vent_diameter": "3\"", "mca": 15.0, "mocp": 20},
    "GR9S801005CNA": {"btu_input": 100000, "btu_output": 80000, "cabinet_width": "21\"", "dimensions": "21\" × 28\" × 33⅜\"", "weight": 124, "blower_hp": "¾", "blower_size": "10\" × 10\"", "num_burners": 5, "temp_rise": "50–80°F", "vent_diameter": "3\"", "mca": 15.0, "mocp": 20},
}

def get_html_template(title, intro, ac_or_hp, furnace, coil, system_type="ac"):
    """Generate complete HTML for a system"""

    is_dual_fuel = system_type == "dual_fuel"
    unit_type = "Heat Pump" if is_dual_fuel else "Air Conditioner"
    tab_name = "Heat Pump" if is_dual_fuel else "Air Conditioner"

    # Build AC/HP table rows
    unit_rows = f"""                        <tr>
                            <td><strong>Manufacturer</strong></td>
                            <td>Goodman</td>
                        </tr>
                        <tr>
                            <td><strong>Model</strong></td>
                            <td>{ac_or_hp['model']}</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage</strong></td>
                            <td>{ac_or_hp['tonnage']} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity (Nominal)</strong></td>
                            <td>{ac_or_hp['btu']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>SEER2 Rating</strong></td>
                            <td>{ac_or_hp['seer2']}</td>
                        </tr>"""

    if is_dual_fuel:
        unit_rows += f"""
                        <tr>
                            <td><strong>HSPF2 Rating</strong></td>
                            <td>{ac_or_hp['hspf2']}</td>
                        </tr>
                        <tr>
                            <td><strong>Heating Capacity (Nominal)</strong></td>
                            <td>{ac_or_hp['btu']:,} BTU/h</td>
                        </tr>"""

    unit_rows += f"""
                        <tr>
                            <td><strong>Refrigerant</strong></td>
                            <td>R-32</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor Type</strong></td>
                            <td>{ac_or_hp['compressor_type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor RLA</strong></td>
                            <td>{ac_or_hp['compressor_rla']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor LRA</strong></td>
                            <td>{ac_or_hp['compressor_lra']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Fan Motor Type</strong></td>
                            <td>{ac_or_hp['fan_motor']}</td>
                        </tr>
                        <tr>
                            <td><strong>Fan Motor FLA</strong></td>
                            <td>{ac_or_hp['fan_fla']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage</strong></td>
                            <td>208–230V / 1Ph / 60Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{ac_or_hp['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{ac_or_hp['mocp']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Sound Level</strong></td>
                            <td>{ac_or_hp['sound']} dBA</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (H×W×D)</strong></td>
                            <td>{ac_or_hp['dimensions']}</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{ac_or_hp['weight']} lbs</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Charge</strong></td>
                            <td>{ac_or_hp['refrigerant_oz']} oz (Factory charged for 15' line)</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Line Size</strong></td>
                            <td>{ac_or_hp['liquid_line']}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Line Size</strong></td>
                            <td>{ac_or_hp['suction_line']}</td>
                        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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
        <h1>{title}</h1>

        <div class="intro-section">
            <p>{intro}</p>
        </div>

        <h2>Technical Specifications</h2>

        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="showTab(event, 'ac-specs')">{tab_name}</button>
                <button class="tab-button" onclick="showTab(event, 'furnace-specs')">Gas Furnace</button>
                <button class="tab-button" onclick="showTab(event, 'coil-specs')">Evaporator Coil</button>
            </div>

            <div id="ac-specs" class="tab-content active">
                <h3>{unit_type} – {ac_or_hp['model']} Specifications</h3>
                <table class="specs-table">
                    <thead>
                        <tr>
                            <th>Specification</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
{unit_rows}
                    </tbody>
                </table>
            </div>

            <div id="furnace-specs" class="tab-content">
                <h3>Gas Furnace – {furnace['model']} Specifications</h3>
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
                            <td><strong>Model</strong></td>
                            <td>{furnace['model']}</td>
                        </tr>
                        <tr>
                            <td><strong>BTU Input</strong></td>
                            <td>{furnace['btu_input']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>BTU Output</strong></td>
                            <td>{furnace['btu_output']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>AFUE</strong></td>
                            <td>80%</td>
                        </tr>
                        <tr>
                            <td><strong>Stages</strong></td>
                            <td>Single-Stage</td>
                        </tr>
                        <tr>
                            <td><strong>Blower Motor</strong></td>
                            <td>Variable-Speed ECM</td>
                        </tr>
                        <tr>
                            <td><strong>Blower HP</strong></td>
                            <td>{furnace['blower_hp']} HP</td>
                        </tr>
                        <tr>
                            <td><strong>Blower Size</strong></td>
                            <td>{furnace['blower_size']}</td>
                        </tr>
                        <tr>
                            <td><strong>Number of Burners</strong></td>
                            <td>{furnace['num_burners']}</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage</strong></td>
                            <td>115 VAC, 60 Hz, Single-Phase</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{furnace['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Device</strong></td>
                            <td>{furnace['mocp']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Temperature Rise Range</strong></td>
                            <td>{furnace['temp_rise']}</td>
                        </tr>
                        <tr>
                            <td><strong>Vent Diameter</strong></td>
                            <td>{furnace['vent_diameter']}</td>
                        </tr>
                        <tr>
                            <td><strong>Cabinet Width</strong></td>
                            <td>{furnace['cabinet_width']}</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{furnace['dimensions']}</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{furnace['weight']} lbs</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div id="coil-specs" class="tab-content">
                <h3>Evaporator Coil – {coil['model']} Specifications</h3>
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
                            <td><strong>Model</strong></td>
                            <td>{coil['model']}</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage</strong></td>
                            <td>{coil['tonnage_range']}</td>
                        </tr>
                        <tr>
                            <td><strong>Type</strong></td>
                            <td>{coil['type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Expansion Device</strong></td>
                            <td>Factory-Installed TXV (Thermal Expansion Valve)</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant</strong></td>
                            <td>R-32 Compatible</td>
                        </tr>
                        <tr>
                            <td><strong>Construction</strong></td>
                            <td>All-Aluminum A-Coil</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{coil['dimensions']}</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{coil['weight']} lbs</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Connection</strong></td>
                            <td>{coil['liquid']}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Connection</strong></td>
                            <td>{coil['suction']}</td>
                        </tr>
                        <tr>
                            <td><strong>Cabinet Style</strong></td>
                            <td>Cased with Drain Pan</td>
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
                <div class="warranty-card">
                    <div class="warranty-years">∞</div>
                    <div class="warranty-label">Lifetime Heat Exchanger Warranty</div>
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
                    <p>This R-32 {'heat pump' if is_dual_fuel else 'air conditioner'} meets Department of Energy minimum efficiency requirements for all U.S. climate zones</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showTab(event, tabId) {{
            const tabContents = document.getElementsByClassName('tab-content');
            for (let content of tabContents) {{
                content.classList.remove('active');
            }}
            const tabButtons = document.getElementsByClassName('tab-button');
            for (let button of tabButtons) {{
                button.classList.remove('active');
            }}
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}
    </script>
</body>
</html>"""
    return html

def generate_system(ac_model, furnace_model, coil_model, system_type="ac"):
    """Generate a system description file"""

    # Get unit specs
    if system_type == "dual_fuel":
        unit = HP_SPECS[ac_model].copy()
    else:
        unit = AC_SPECS[ac_model].copy()
    unit['model'] = ac_model

    # Get furnace specs
    furnace = FURNACE_80[furnace_model].copy()
    furnace['model'] = furnace_model

    # Get coil specs from JSON
    coil_data = specs.get(coil_model, {})
    coil_dims = coil_data.get("dimensions", {})
    coil = {
        'model': coil_model,
        'tonnage_range': coil_data.get("tonnage_range", "N/A"),
        'type': coil_data.get("coil_type", "Cased Upflow"),
        'dimensions': f"{coil_dims.get('width', 'N/A')} × {coil_dims.get('depth', 'N/A')} × {coil_dims.get('height', 'N/A')}",
        'weight': coil_data.get("weight", "N/A"),
        'liquid': coil_data.get("line_sizes", {}).get("liquid", "⅜\""),
        'suction': coil_data.get("line_sizes", {}).get("suction", "¾\"")
    }

    tonnage = unit["tonnage"]
    tonnage_str = TONNAGE_MAP[tonnage]
    coil_type = "Upflow" if "CAPTA" in coil_model else "Horizontal"

    # Build filename and title
    if system_type == "dual_fuel":
        filename = f"Goodman_{tonnage_str}_R32_143SEER2_80AFUE_DualFuel_HeatPump_System_{ac_model}_{furnace_model}_{coil_model}.html"
        title = f"GOODMAN {tonnage} Ton 14.3 SEER2 R-32 80% AFUE Dual Fuel Heat Pump System ({coil_type} Coil)"
        intro = f"Experience ultimate year-round comfort with this complete Goodman {tonnage}-ton dual fuel heat pump system ({coil_type} Coil). This intelligently matched system combines a high-efficiency 14.3 SEER2 / 7.5 HSPF2 heat pump for efficient heating and cooling, an 80% AFUE single-stage gas furnace with variable-speed ECM blower for supplemental heating during extreme cold, and a precision-engineered {coil_type.lower()} evaporator coil with factory-installed TXV. The system automatically switches between electric heat pump operation and gas furnace backup for optimal efficiency and comfort. Designed for dependable performance with environmentally-friendly R-32 refrigerant."
    else:
        filename = f"Goodman_{tonnage_str}_R32_AC_System_{ac_model}_{furnace_model}_{coil_model}.html"
        title = f"GOODMAN {tonnage} Ton 14.3 SEER2 R-32 80% AFUE AC System ({coil_type} Coil)"
        intro = f"Experience year-round comfort with this complete Goodman {tonnage}-ton air conditioning system ({coil_type} Coil). This matched system combines a high-efficiency 14.3 SEER2 air conditioner for efficient cooling, a 80% AFUE single-stage gas furnace with variable-speed ECM blower for reliable heating, and a precision-engineered {coil_type.lower()} evaporator coil with factory-installed TXV. Designed for dependable performance with environmentally-friendly R-32 refrigerant."

    html = get_html_template(title, intro, unit, furnace, coil, system_type)

    return filename, html

# System combinations to generate
systems = {
    "80% Upflow AC (remaining)": [
        ("GLXS4BA4810", "GR9S800804CNA", "CAPTA6030C3", "ac"),
        ("GLXS4BA6010", "GR9S801005CNA", "CAPTA6030C3", "ac"),
    ],
    "80% Horizontal AC": [
        ("GLXS4BA1810", "GR9S800403ANA", "CHPTA2426B3", "ac"),
        ("GLXS4BA2410", "GR9S800403ANA", "CHPTA2426B3", "ac"),
        ("GLXS4BA3010", "GR9S800603ANA", "CHPTA3026B3", "ac"),
        ("GLXS4BA3610", "GR9S800604BNA", "CHPTA3630B3", "ac"),
        ("GLXS4BA4210", "GR9S800804CNA", "CHPTA4230C3", "ac"),
        ("GLXS4BA4810", "GR9S800804CNA", "CHPTA4830C3", "ac"),
        ("GLXS4BA6010", "GR9S801005CNA", "CHPTA6030D3", "ac"),
    ],
    "80% Upflow Dual Fuel": [
        ("GLZS4BA1810", "GR9S800403ANA", "CAPTA2422A3", "dual_fuel"),
        ("GLZS4BA2410", "GR9S800403ANA", "CAPTA2422A3", "dual_fuel"),
        ("GLZS4BA3010", "GR9S800603ANA", "CAPTA3022A3", "dual_fuel"),
        ("GLZS4BA3610", "GR9S800604BNA", "CAPTA3626B3", "dual_fuel"),
        ("GLZS4BA4210", "GR9S800804CNA", "CAPTA4230C3", "dual_fuel"),
        ("GLZS4BA4810", "GR9S800804CNA", "CAPTA6030C3", "dual_fuel"),
        ("GLZS4BA6010", "GR9S801005CNA", "CAPTA6030C3", "dual_fuel"),
    ],
    "80% Horizontal Dual Fuel": [
        ("GLZS4BA1810", "GR9S800403ANA", "CHPTA2426B3", "dual_fuel"),
        ("GLZS4BA2410", "GR9S800403ANA", "CHPTA2426B3", "dual_fuel"),
        ("GLZS4BA3010", "GR9S800603ANA", "CHPTA3026B3", "dual_fuel"),
        ("GLZS4BA3610", "GR9S800604BNA", "CHPTA3630B3", "dual_fuel"),
        ("GLZS4BA4210", "GR9S800804CNA", "CHPTA4230C3", "dual_fuel"),
        ("GLZS4BA4810", "GR9S800804CNA", "CHPTA4830C3", "dual_fuel"),
        ("GLZS4BA6010", "GR9S801005CNA", "CHPTA6030D3", "dual_fuel"),
    ],
}

# Generate all systems
total_generated = 0
for category, system_list in systems.items():
    print(f"\n{category}:")
    for ac_model, furnace_model, coil_model, sys_type in system_list:
        filename, html = generate_system(ac_model, furnace_model, coil_model, sys_type)
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"  ✓ {filename}")
        total_generated += 1

print(f"\n✅ Successfully generated {total_generated} system descriptions!")
print(f"📁 All files saved to: {OUTPUT_DIR}")
