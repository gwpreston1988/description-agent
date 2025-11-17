#!/usr/bin/env python3
"""
Generate individual component descriptions from JSON specs
"""
import json
from pathlib import Path

# Load specs
with open('14.3_specs.json', 'r') as f:
    specs = json.load(f)

OUTPUT_DIR = Path("Description Directory")

def get_component_html(model, component_data, component_type):
    """Generate HTML for individual component"""

    # Determine component type and build appropriate content
    if component_type == "heat_pump":
        title = f"Goodman {model} {component_data.get('nominal_capacity_tons_cooling', '')} Ton R-32 Heat Pump"
        intro = f"The Goodman {model} is a {component_data.get('nominal_capacity_tons_cooling', '')}-ton R-32 heat pump outdoor unit delivering {component_data.get('seer2_max', 14.3)} SEER2 cooling efficiency and {component_data.get('hspf2_max', 7.5)} HSPF2 heating performance. Featuring a {component_data.get('compressor_type', 'rotary')} compressor and environmentally-friendly R-32 refrigerant, this unit provides reliable year-round comfort with advanced efficiency for both heating and cooling applications."
        warranty_cards = """
                <div class="warranty-card">
                    <div class="warranty-years">10</div>
                    <div class="warranty-label">Year Parts Warranty</div>
                </div>
                <div class="warranty-card">
                    <div class="warranty-years">10</div>
                    <div class="warranty-label">Year Compressor Warranty</div>
                </div>"""
        doe_text = "This R-32 heat pump meets Department of Energy minimum efficiency requirements for all U.S. climate zones"

        specs_rows = f"""
                        <tr>
                            <td><strong>Manufacturer</strong></td>
                            <td>Goodman</td>
                        </tr>
                        <tr>
                            <td><strong>Model Number</strong></td>
                            <td>{model}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Heat Pump Outdoor Unit</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage (Cooling)</strong></td>
                            <td>{component_data.get('nominal_capacity_tons_cooling', 'N/A')} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage (Heating)</strong></td>
                            <td>{component_data.get('nominal_capacity_tons_heating', 'N/A')} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity (Nominal)</strong></td>
                            <td>{component_data.get('cooling_capacity_btu', 0):,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>Heating Capacity (Nominal)</strong></td>
                            <td>{component_data.get('heating_capacity_btu', 0):,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>SEER2 Rating</strong></td>
                            <td>{component_data.get('seer2_max', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>HSPF2 Rating</strong></td>
                            <td>{component_data.get('hspf2_max', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Type</strong></td>
                            <td>{component_data.get('refrigerant', 'R-32')}</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor Type</strong></td>
                            <td>{component_data.get('compressor_type', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor RLA</strong></td>
                            <td>{component_data.get('compressor_rla', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor LRA</strong></td>
                            <td>{component_data.get('compressor_lra', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Fan Motor Type</strong></td>
                            <td>{component_data.get('fan_motor_type', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Fan Motor HP</strong></td>
                            <td>{component_data.get('fan_motor_hp', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Fan Motor FLA</strong></td>
                            <td>{component_data.get('fan_motor_fla', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage/Phase</strong></td>
                            <td>{component_data.get('voltage_phase', '208/230-1')}</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{component_data.get('min_circuit_ampacity', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{component_data.get('max_breaker', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Sound Level</strong></td>
                            <td>{component_data.get('sound_level_db', 'N/A')} dBA</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{component_data.get('dimensions', {}).get('width', 'N/A')} × {component_data.get('dimensions', {}).get('depth', 'N/A')} × {component_data.get('dimensions', {}).get('height', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{component_data.get('weight', 'N/A')} lbs</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Charge</strong></td>
                            <td>{component_data.get('refrigerant_charge_oz', 'N/A')} oz</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Line Size</strong></td>
                            <td>{component_data.get('line_sizes', {}).get('liquid', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Line Size</strong></td>
                            <td>{component_data.get('line_sizes', {}).get('suction', 'N/A')}</td>
                        </tr>"""

    elif component_type == "air_conditioner":
        title = f"Goodman {model} {component_data.get('nominal_capacity_tons', '')} Ton R-32 Air Conditioner"
        intro = f"The Goodman {model} is a {component_data.get('nominal_capacity_tons', '')}-ton R-32 air conditioner outdoor unit delivering {component_data.get('seer2_max', 14.3)} SEER2 cooling efficiency. Featuring a {component_data.get('compressor_type', 'rotary')} compressor and environmentally-friendly R-32 refrigerant, this unit provides reliable cooling performance with advanced energy efficiency for residential applications."
        warranty_cards = """
                <div class="warranty-card">
                    <div class="warranty-years">10</div>
                    <div class="warranty-label">Year Parts Warranty</div>
                </div>
                <div class="warranty-card">
                    <div class="warranty-years">10</div>
                    <div class="warranty-label">Year Compressor Warranty</div>
                </div>"""
        doe_text = "This R-32 air conditioner meets Department of Energy minimum efficiency requirements for all U.S. climate zones"

        specs_rows = f"""
                        <tr>
                            <td><strong>Manufacturer</strong></td>
                            <td>Goodman</td>
                        </tr>
                        <tr>
                            <td><strong>Model Number</strong></td>
                            <td>{model}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Air Conditioner Outdoor Unit</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage</strong></td>
                            <td>{component_data.get('nominal_capacity_tons', 'N/A')} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity (Nominal)</strong></td>
                            <td>{int(float(component_data.get('nominal_capacity_tons', 0)) * 12000):,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>SEER2 Rating</strong></td>
                            <td>14.3</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Type</strong></td>
                            <td>R-32</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor Type</strong></td>
                            <td>{component_data.get('compressor_type', 'Single-Stage Rotary')}</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage/Phase</strong></td>
                            <td>{component_data.get('voltage_phase', '208/230-1')}</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{component_data.get('dimensions_w', 'N/A')}" × {component_data.get('d', 'N/A')}" × {component_data.get('h', 'N/A')}"</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Line Size</strong></td>
                            <td>{component_data.get('service_valve_liquid', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Line Size</strong></td>
                            <td>{component_data.get('suction', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Sound Level</strong></td>
                            <td>{component_data.get('dbs', 'N/A')} dBA</td>
                        </tr>"""

    elif component_type == "gas_furnace":
        afue = component_data.get('afue', 92)
        title = f"Goodman {model} {afue}% AFUE Gas Furnace"
        btu_output = component_data.get('heating_capacity_output', component_data.get('heating_capacity_input', 0))
        btu_str = f"{btu_output:,}" if isinstance(btu_output, (int, float)) else "N/A"
        intro = f"The Goodman {model} is a {afue}% AFUE {component_data.get('stages', 'single-stage')} gas furnace delivering {btu_str} BTU/h of reliable heating output. Featuring a {component_data.get('blower_motor', 'multi-speed ECM')} blower motor and durable aluminized steel heat exchanger, this furnace provides efficient and dependable home heating performance."
        warranty_cards = """
                <div class="warranty-card">
                    <div class="warranty-years">10</div>
                    <div class="warranty-label">Year Parts Warranty</div>
                </div>
                <div class="warranty-card">
                    <div class="warranty-years">∞</div>
                    <div class="warranty-label">Lifetime Heat Exchanger Warranty</div>
                </div>"""
        doe_text = "This gas furnace meets Department of Energy efficiency requirements for residential heating applications"

        dims = component_data.get('dimensions', {})
        specs_rows = f"""
                        <tr>
                            <td><strong>Manufacturer</strong></td>
                            <td>Goodman</td>
                        </tr>
                        <tr>
                            <td><strong>Model Number</strong></td>
                            <td>{model}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Gas Furnace</td>
                        </tr>
                        <tr>
                            <td><strong>BTU Input</strong></td>
                            <td>{f"{component_data.get('heating_capacity_input', 0):,}" if isinstance(component_data.get('heating_capacity_input'), (int, float)) else 'N/A'} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>BTU Output</strong></td>
                            <td>{f"{component_data.get('heating_capacity_output', 0):,}" if isinstance(component_data.get('heating_capacity_output'), (int, float)) else 'N/A'} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>AFUE</strong></td>
                            <td>{afue}%</td>
                        </tr>
                        <tr>
                            <td><strong>Stages</strong></td>
                            <td>{component_data.get('stages', 'Single-Stage')}</td>
                        </tr>
                        <tr>
                            <td><strong>Blower Motor</strong></td>
                            <td>{component_data.get('blower_motor', 'Multi-Speed ECM')}</td>
                        </tr>
                        <tr>
                            <td><strong>Blower HP</strong></td>
                            <td>{component_data.get('blower_hp', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Blower Size</strong></td>
                            <td>{component_data.get('blower_size', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{component_data.get('min_circuit_ampacity', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{component_data.get('max_breaker', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Temperature Rise</strong></td>
                            <td>{component_data.get('temperature_rise', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Vent Diameter</strong></td>
                            <td>{component_data.get('vent_diameter', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Cabinet Width</strong></td>
                            <td>{component_data.get('cabinet_width', dims.get('width', 'N/A'))}</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{dims.get('width', 'N/A')} × {dims.get('depth', 'N/A')} × {dims.get('height', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{component_data.get('weight', 'N/A')} lbs</td>
                        </tr>"""

    elif component_type == "evaporator_coil":
        coil_type = component_data.get('coil_type', 'Cased Upflow')
        title = f"Goodman {model} {component_data.get('tonnage_range', '')} Ton R-32 Evaporator Coil"
        intro = f"The Goodman {model} is a {component_data.get('tonnage_range', '')}-ton {coil_type.lower()} evaporator coil designed for R-32 refrigerant systems. Featuring all-aluminum construction with factory-installed TXV (Thermal Expansion Valve), this coil provides optimal refrigerant metering and efficient heat transfer for reliable cooling performance in residential HVAC applications."
        warranty_cards = """
                <div class="warranty-card">
                    <div class="warranty-years">10</div>
                    <div class="warranty-label">Year Parts Warranty</div>
                </div>"""
        doe_text = "This evaporator coil is designed for use with DOE-compliant R-32 refrigerant systems"

        dims = component_data.get('dimensions', {})
        specs_rows = f"""
                        <tr>
                            <td><strong>Manufacturer</strong></td>
                            <td>Goodman</td>
                        </tr>
                        <tr>
                            <td><strong>Model Number</strong></td>
                            <td>{model}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>{coil_type} Evaporator Coil</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage Range</strong></td>
                            <td>{component_data.get('tonnage_range', 'N/A')} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Type</strong></td>
                            <td>{component_data.get('refrigerant', 'R-32')}</td>
                        </tr>
                        <tr>
                            <td><strong>Expansion Device</strong></td>
                            <td>Factory-Installed {component_data.get('expansion_device', 'TXV')}</td>
                        </tr>
                        <tr>
                            <td><strong>Construction</strong></td>
                            <td>{component_data.get('construction', 'All-Aluminum A-Coil')}</td>
                        </tr>
                        <tr>
                            <td><strong>Cabinet Style</strong></td>
                            <td>{component_data.get('cabinet_style', 'Cased with Drain Pan')}</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{dims.get('width', 'N/A')} × {dims.get('depth', 'N/A')} × {dims.get('height', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{component_data.get('weight', 'N/A')} lbs</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Connection</strong></td>
                            <td>{component_data.get('line_sizes', {}).get('liquid', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Connection</strong></td>
                            <td>{component_data.get('line_sizes', {}).get('suction', 'N/A')}</td>
                        </tr>"""

    elif component_type == "air_handler":
        title = f"Goodman {model} Air Handler"
        tonnage = component_data.get('tonnage_range', component_data.get('cooling_btu_h', '').replace('000', 'k').replace(',', ''))
        intro = f"The Goodman {model} is a multi-position air handler designed for residential HVAC applications. Featuring a variable-speed ECM blower motor and durable construction, this air handler provides efficient air circulation and reliable performance when paired with compatible outdoor units."
        warranty_cards = """
                <div class="warranty-card">
                    <div class="warranty-years">10</div>
                    <div class="warranty-label">Year Parts Warranty</div>
                </div>"""
        doe_text = "This air handler is designed for use with DOE-compliant HVAC systems"

        specs_rows = f"""
                        <tr>
                            <td><strong>Manufacturer</strong></td>
                            <td>Goodman</td>
                        </tr>
                        <tr>
                            <td><strong>Model Number</strong></td>
                            <td>{model}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Multi-Position Air Handler</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity</strong></td>
                            <td>{component_data.get('cooling_btu_h', 'N/A')} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage Range</strong></td>
                            <td>{component_data.get('tonnage_range', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Blower Motor HP</strong></td>
                            <td>{component_data.get('horsepower_hp', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>FLA</strong></td>
                            <td>{component_data.get('fla', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage</strong></td>
                            <td>{component_data.get('voltage', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{component_data.get('min_circuit_ampacity', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{component_data.get('max_overcurrent_device_amps', 'N/A')} A</td>
                        </tr>
                        <tr>
                            <td><strong>Shipping Weight</strong></td>
                            <td>{component_data.get('ship_weight_lbs', 'N/A')} lbs</td>
                        </tr>"""

    else:
        return None

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
        <h1>{title}</h1>

        <div class="intro-section">
            <p>{intro}</p>
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
{specs_rows}
            </tbody>
        </table>

        <div class="warranty-section">
            <h2>Comprehensive Warranty Protection</h2>
            <div class="warranty-grid">
{warranty_cards}
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
                    <h3>DOE Compliant</h3>
                    <p>{doe_text}</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    return html

# Component lists from SKUS file
components = {
    "Heat Pumps": ["GLZS4BA1810", "GLZS4BA2410", "GLZS4BA3010", "GLZS4BA3610", "GLZS4BA4210", "GLZS4BA4810", "GLZS4BA6010"],
    "AC Units": ["GLXS4BA1810", "GLXS4BA2410", "GLXS4BA3010", "GLXS4BA3610", "GLXS4BA4210", "GLXS4BA4810", "GLXS4BA6010"],
    "AMST Air Handlers": ["AMST24BU13", "AMST30BU13", "AMST36BU13", "AMST42CU13", "AMST48CU13", "AMST60DU13", "AMST60CU13"],
    "AWST Wall-Hung": ["AWST18SU1303A", "AWST18SU1305A", "AWST18SU1308A", "AWST24SU1305A", "AWST24SU1308A", "AWST24SU1310A", "AWST30LU1305A", "AWST30LU1308A", "AWST30LU1310A", "AWST36LU1305A", "AWST36LU1308A", "AWST36LU1310A"],
    "80% Furnaces": ["GR9S800403ANA", "GR9S800603ANA", "GR9S800604BNA", "GR9S800804CNA", "GR9S801005CNA"],
    "92% Furnaces": ["GR9S920403AN", "GR9S920603BN", "GR9S920803BN", "GR9S920804CN", "GR9S920805CN", "GR9S921004CN", "GR9S921005CN", "GR9S921205DN"],
    "Upflow Coils": ["CAPTA2422A3", "CAPTA3022A3", "CAPTA3626B3", "CAPTA4230C3", "CAPTA6030C3"],
    "Horizontal Coils": ["CHPTA2426B3", "CHPTA3026B3", "CHPTA3630B3", "CHPTA4230C3", "CHPTA4830C3", "CHPTA6030D3"],
}

total_generated = 0

# Generate Heat Pumps
print("\nGenerating Heat Pumps:")
for model in components["Heat Pumps"]:
    if model in specs:
        html = get_component_html(model, specs[model], "heat_pump")
        if html:
            filename = f"Goodman_R32_HeatPump_{model}.html"
            with open(OUTPUT_DIR / filename, 'w') as f:
                f.write(html)
            print(f"  ✓ {filename}")
            total_generated += 1

# Generate AC Units
print("\nGenerating AC Units:")
for model in components["AC Units"]:
    if model in specs:
        html = get_component_html(model, specs[model], "air_conditioner")
        if html:
            filename = f"Goodman_R32_AirConditioner_{model}.html"
            with open(OUTPUT_DIR / filename, 'w') as f:
                f.write(html)
            print(f"  ✓ {filename}")
            total_generated += 1

# Generate Air Handlers
print("\nGenerating AMST Air Handlers:")
for model in components["AMST Air Handlers"]:
    if model in specs:
        html = get_component_html(model, specs[model], "air_handler")
        if html:
            filename = f"Goodman_Air_Handler_{model}.html"
            with open(OUTPUT_DIR / filename, 'w') as f:
                f.write(html)
            print(f"  ✓ {filename}")
            total_generated += 1

# Generate AWST Wall-Hung Air Handlers
print("\nGenerating AWST Wall-Hung Air Handlers:")
for model in components["AWST Wall-Hung"]:
    if model in specs:
        html = get_component_html(model, specs[model], "air_handler")
        if html:
            filename = f"Goodman_R32_Air_Handler_{model}.html"
            with open(OUTPUT_DIR / filename, 'w') as f:
                f.write(html)
            print(f"  ✓ {filename}")
            total_generated += 1

# Generate 80% Furnaces
print("\nGenerating 80% Furnaces:")
for model in components["80% Furnaces"]:
    if model in specs:
        html = get_component_html(model, specs[model], "gas_furnace")
        if html:
            filename = f"Goodman_80AFUE_Furnace_{model}.html"
            with open(OUTPUT_DIR / filename, 'w') as f:
                f.write(html)
            print(f"  ✓ {filename}")
            total_generated += 1

# Generate 92% Furnaces
print("\nGenerating 92% Furnaces:")
for model in components["92% Furnaces"]:
    # Add 'A' suffix if needed
    model_key = model if model in specs else model + "A"
    if model_key in specs:
        html = get_component_html(model, specs[model_key], "gas_furnace")
        if html:
            filename = f"Goodman_92AFUE_Furnace_{model}.html"
            with open(OUTPUT_DIR / filename, 'w') as f:
                f.write(html)
            print(f"  ✓ {filename}")
            total_generated += 1

# Generate Coils
print("\nGenerating Evaporator Coils:")
for model in components["Upflow Coils"] + components["Horizontal Coils"]:
    if model in specs:
        html = get_component_html(model, specs[model], "evaporator_coil")
        if html:
            coil_type = "Upflow" if "CAPTA" in model else "Horizontal"
            filename = f"Goodman_R32_{coil_type}Coil_{model}.html"
            with open(OUTPUT_DIR / filename, 'w') as f:
                f.write(html)
            print(f"  ✓ {filename}")
            total_generated += 1

print(f"\n✅ Successfully generated {total_generated} individual component descriptions!")
print(f"📁 All files saved to: {OUTPUT_DIR}")
