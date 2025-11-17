#!/usr/bin/env python3
"""
Universal HTML Generator - Generates complete HTML using programmatic approach
Based on proven 15.2 scripts, made universal for all SEER ratings
"""

from pathlib import Path
from typing import Dict, List, Optional


class HTMLGenerator:
    """Generate complete HTML programmatically based on system type"""

    def __init__(self, seer_rating: float):
        """
        Initialize generator with SEER rating

        Args:
            seer_rating: SEER2 rating (e.g., 13.4, 14.3, 15.2, 16.2, 17.2, 17.5)
        """
        self.seer_rating = seer_rating

    def get_doe_footer(self) -> tuple[str, str]:
        """
        Get DOE compliance footer based on SEER rating

        Returns:
            Tuple of (title, description)
        """
        if self.seer_rating < 14.3:
            return (
                "DOE Compliant for Northern Regions Only",
                f"This {self.seer_rating} SEER2 equipment meets Department of Energy efficiency requirements for residential HVAC installations in northern U.S. climate zones only"
            )
        else:
            return (
                "DOE Compliant Nationwide",
                f"This {self.seer_rating} SEER2 equipment meets Department of Energy efficiency requirements for residential HVAC installations across all U.S. climate zones"
            )

    @staticmethod
    def format_tonnage(tonnage: float) -> str:
        """Format tonnage for display"""
        if tonnage == int(tonnage):
            return str(int(tonnage))
        return str(tonnage)

    @staticmethod
    def format_line_size(size_str: str) -> str:
        """Convert decimal line sizes to fractions"""
        conversions = {
            '0.375': '⅜"',
            '0.75': '¾"',
            '0.875': '⅞"',
            '1.125': '1⅛"',
            '0.5': '½"',
            '0.625': '⅝"'
        }
        return conversions.get(str(size_str), str(size_str) + '"')

    def get_common_styles(self) -> str:
        """Get common CSS styles used in all descriptions"""
        return """
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        #product-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #000;
            background: #fff;
        }

        #product-container h1 {
            font-size: 2.5em;
            color: #D53938;
            margin-bottom: 10px;
            padding-bottom: 15px;
            border-bottom: 3px solid #D53938;
            font-weight: 700;
        }

        #product-container h2 {
            font-size: 1.8em;
            color: #D53938;
            margin: 30px 0 15px 0;
            font-weight: 600;
        }

        #product-container h3 {
            font-size: 1.4em;
            color: #57A9F9;
            margin: 25px 0 12px 0;
            font-weight: 600;
        }

        #product-container p {
            line-height: 1.8;
            margin-bottom: 15px;
            font-size: 1.05em;
            color: #333;
        }

        .intro-section {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 8px;
            margin: 25px 0;
            border-left: 5px solid #D53938;
        }

        .specs-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }

        .specs-table thead {
            background: linear-gradient(135deg, #D53938 0%, #b32d2c 100%);
            color: white;
        }

        .specs-table th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1.1em;
        }

        .specs-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }

        .specs-table tbody tr {
            background: #fff;
            transition: all 0.3s ease;
        }

        .specs-table tbody tr:nth-child(even) {
            background: #f8f9fa;
        }

        .specs-table tbody tr:hover {
            background: linear-gradient(90deg, #D53938 0%, #b32d2c 100%) !important;
            color: white;
            transform: scale(1.01);
            box-shadow: 0 4px 12px rgba(213, 57, 56, 0.3);
        }

        .specs-table tbody tr:hover td {
            color: white;
        }

        .warranty-section {
            background: linear-gradient(135deg, #F8F9FA 0%, #e9ecef 100%);
            padding: 50px 30px;
            border-radius: 15px;
            margin: 50px 0;
        }

        .warranty-section h2 {
            color: #D53938;
            text-align: center;
            margin-bottom: 40px;
            font-size: 28px;
        }

        .warranty-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            max-width: 800px;
            margin: 0 auto;
        }

        .warranty-card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            border: 2px solid rgba(213,57,56,0.3);
            transition: all 0.3s ease;
        }

        .warranty-card:hover {
            background: rgba(213,57,56,0.05);
            border-color: #D53938;
            transform: translateY(-5px);
        }

        .warranty-years {
            font-size: 48px;
            font-weight: 700;
            color: #D53938;
        }

        .warranty-label {
            color: #333;
            font-size: 14px;
            font-weight: 600;
        }

        .cta-section {
            background: linear-gradient(135deg, #F8F9FA 0%, #e9ecef 100%);
            padding: 60px 30px;
            border-radius: 15px;
            margin-top: 50px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }

        .cta-content {
            text-align: center;
            margin-bottom: 40px;
        }

        .cta-section h2 {
            color: #D53938;
            margin: 0 0 15px 0;
            font-size: 28px;
            font-weight: 700;
        }

        .cta-section p {
            color: #333;
            margin: 0;
            font-size: 16px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }

        .compliance-badge {
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
        }

        .compliance-badge:hover {
            background: rgba(87,169,249,0.05);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(213,57,56,0.2);
        }

        .badge-icon {
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
        }

        .badge-content {
            text-align: left;
        }

        .badge-content h3 {
            color: #D53938;
            margin: 0 0 8px 0;
            font-size: 18px;
            font-weight: 700;
        }

        .badge-content p {
            color: #555;
            margin: 0;
            font-size: 14px;
            line-height: 1.5;
        }

        .tab-container {
            margin: 30px 0;
        }

        .tab-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .tab-button {
            padding: 12px 24px;
            background: #f8f9fa;
            border: 2px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            color: #333;
            transition: all 0.3s ease;
        }

        .tab-button:hover {
            background: #e9ecef;
            border-color: #57A9F9;
        }

        .tab-button.active {
            background: linear-gradient(135deg, #D53938 0%, #b32d2c 100%);
            color: white;
            border-color: #D53938;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        @media (max-width: 768px) {
            #product-container {
                padding: 15px;
            }

            #product-container h1 {
                font-size: 1.8em;
            }

            #product-container h2 {
                font-size: 1.4em;
            }

            .specs-table {
                font-size: 0.9em;
            }

            .specs-table th,
            .specs-table td {
                padding: 10px;
            }

            .compliance-badge {
                flex-direction: column;
                text-align: center;
                padding: 20px;
            }

            .badge-content {
                text-align: center;
            }

            .cta-section {
                padding: 40px 20px;
            }

            .tab-buttons {
                flex-direction: column;
            }

            .tab-button {
                width: 100%;
            }
        }
    """

    def get_javascript(self) -> str:
        """Get common JavaScript for tab functionality"""
        return """
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

    def generate_ac_airhandler(self, ac_spec: Dict, ah_spec: Dict) -> str:
        """Generate AC + Air Handler system description"""
        tonnage_display = self.format_tonnage(ac_spec['tonnage'])
        liquid_line = self.format_line_size(str(ac_spec['liquid_line_od_in']))
        suction_line = self.format_line_size(str(ac_spec['suction_line_od_in']))

        doe_title, doe_desc = self.get_doe_footer()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GOODMAN {tonnage_display} Ton {self.seer_rating} SEER2 R-32 Air Conditioning System with Multi-Positional Air Handler</title>
    <style>
        {self.get_common_styles()}
    </style>
</head>
<body>
    <div id="product-container">
        <h1>GOODMAN {tonnage_display} Ton {self.seer_rating} SEER2 R-32 Air Conditioning System with Multi-Positional Air Handler</h1>

        <div class="intro-section">
            <p>Experience premium cooling comfort with this Goodman {tonnage_display}-ton {self.seer_rating} SEER2 air conditioning system. This complete matched system combines a high-efficiency air conditioner outdoor unit with a versatile multi-positional air handler. Designed for reliable cooling performance, this system delivers exceptional energy efficiency, quiet operation, and dependable comfort with R-32 refrigerant.</p>
        </div>

        <h2>Technical Specifications</h2>

        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="showTab(event, 'ac-specs')">Air Conditioner</button>
                <button class="tab-button" onclick="showTab(event, 'airhandler-specs')">Air Handler</button>
            </div>

            <div id="ac-specs" class="tab-content active">
                <h3>Air Conditioner — {ac_spec['model_number']} Specifications</h3>
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
                            <td>R-32</td>
                        </tr>
                        <tr>
                            <td><strong>SKU/Model No</strong></td>
                            <td>{ac_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Split System Air Conditioner</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity</strong></td>
                            <td>{ac_spec['cooling_capacity_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>SEER2 Rating</strong></td>
                            <td>Up to {self.seer_rating}</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor Type</strong></td>
                            <td>{ac_spec['compressor_type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage</strong></td>
                            <td>{ac_spec['voltage']}V / {ac_spec['phase']}Ph / {ac_spec['frequency_hz']}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{ac_spec['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{int(ac_spec['mop'])} A</td>
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
                            <td>{int(ac_spec['factory_charge_oz'])} oz</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (H×W×D)</strong></td>
                            <td>{ac_spec['height_in']}" × {int(ac_spec['width_in'])}" × {int(ac_spec['depth_in'])}"</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{int(ac_spec['shipping_weight_lb'])} lbs</td>
                        </tr>
                        <tr>
                            <td><strong>Sound Level</strong></td>
                            <td>{ac_spec['sound_level_dba']} dBA</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div id="airhandler-specs" class="tab-content">
                <h3>Air Handler — {ah_spec['model_number']} Specifications</h3>
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
                            <td><strong>SKU/Model No</strong></td>
                            <td>{ah_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Multi-Positional Air Handler</td>
                        </tr>
                        <tr>
                            <td><strong>Motor Type</strong></td>
                            <td>{ah_spec['blower_motor_type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Nominal Cooling Capacity</strong></td>
                            <td>{ac_spec['cooling_capacity_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>Airflow</strong></td>
                            <td>{ah_spec.get('airflow_cfm') or 'N/A'} CFM</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage</strong></td>
                            <td>{ah_spec['voltage']}V / {ah_spec['phase']}Ph / {ah_spec['frequency_hz']}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{ah_spec['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Device</strong></td>
                            <td>{ah_spec['mop']} A</td>
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
                            <td>{ah_spec['height_in']}" × {ah_spec['width_in']}" × {ah_spec['depth_in']}"</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{int(ah_spec['shipping_weight_lb'])} lbs</td>
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
                    <h3>{doe_title}</h3>
                    <p>{doe_desc}</p>
                </div>
            </div>
            <p style="margin-top: 20px; text-align: center; color: #666; font-size: 0.9em;"><strong>Important:</strong> Check state and local codes and ordinances before purchasing. Product availability and compliance requirements may vary by region.</p>
        </div>
    </div>
"""

        html += self.get_javascript()
        return html


    def generate_hp_airhandler(self, hp_spec: Dict, ah_spec: Dict) -> str:
        """Generate Heat Pump + Air Handler system description"""
        tonnage_display = self.format_tonnage(hp_spec['tonnage'])
        liquid_line = self.format_line_size(str(hp_spec['liquid_line_od_in']))
        suction_line = self.format_line_size(str(hp_spec['suction_line_od_in']))

        doe_title, doe_desc = self.get_doe_footer()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GOODMAN {tonnage_display} Ton {self.seer_rating} SEER2 R-32 Heat Pump System with Multi-Positional Air Handler</title>
    <style>
        {self.get_common_styles()}
    </style>
</head>
<body>
    <div id="product-container">
        <h1>GOODMAN {tonnage_display} Ton {self.seer_rating} SEER2 R-32 Heat Pump System with Multi-Positional Air Handler</h1>

        <div class="intro-section">
            <p>Experience year-round comfort with this premium Goodman {tonnage_display}-ton {self.seer_rating} SEER2 heat pump system. This complete matched system combines a high-efficiency heat pump outdoor unit with a versatile multi-positional air handler. Designed for reliable heating and cooling performance, this system delivers exceptional energy efficiency, quiet operation, and dependable comfort with R-32 refrigerant.</p>
        </div>

        <h2>Technical Specifications</h2>

        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="showTab(event, 'hp-specs')">Heat Pump</button>
                <button class="tab-button" onclick="showTab(event, 'airhandler-specs')">Air Handler</button>
            </div>

            <div id="hp-specs" class="tab-content active">
                <h3>Heat Pump — {hp_spec['model_number']} Specifications</h3>
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
                            <td>R-32</td>
                        </tr>
                        <tr>
                            <td><strong>SKU/Model No</strong></td>
                            <td>{hp_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Split System Heat Pump</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity</strong></td>
                            <td>{hp_spec['cooling_capacity_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>Heating Capacity (47°F)</strong></td>
                            <td>{hp_spec['heating_capacity_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>SEER2 Rating</strong></td>
                            <td>Up to {self.seer_rating}</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor Type</strong></td>
                            <td>{hp_spec['compressor_type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage</strong></td>
                            <td>{hp_spec['voltage']}V / {hp_spec['phase']}Ph / {hp_spec['frequency_hz']}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{hp_spec['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{int(hp_spec['mop'])} A</td>
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
                            <td>{int(hp_spec['factory_charge_oz'])} oz</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (H×W×D)</strong></td>
                            <td>{hp_spec['height_in']}" × {int(hp_spec['width_in'])}" × {int(hp_spec['depth_in'])}"</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{int(hp_spec['shipping_weight_lb'])} lbs</td>
                        </tr>
                        <tr>
                            <td><strong>Sound Level</strong></td>
                            <td>{hp_spec['sound_level_dba']} dBA</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div id="airhandler-specs" class="tab-content">
                <h3>Air Handler — {ah_spec['model_number']} Specifications</h3>
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
                            <td><strong>SKU/Model No</strong></td>
                            <td>{ah_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Multi-Positional Air Handler</td>
                        </tr>
                        <tr>
                            <td><strong>Motor Type</strong></td>
                            <td>{ah_spec['blower_motor_type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Nominal Cooling Capacity</strong></td>
                            <td>{hp_spec['cooling_capacity_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>Airflow</strong></td>
                            <td>{ah_spec.get('airflow_cfm') or 'N/A'} CFM</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage</strong></td>
                            <td>{ah_spec['voltage']}V / {ah_spec['phase']}Ph / {ah_spec['frequency_hz']}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{ah_spec['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Device</strong></td>
                            <td>{ah_spec['mop']} A</td>
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
                            <td>{ah_spec['height_in']}" × {ah_spec['width_in']}" × {ah_spec['depth_in']}"</td>
                        </tr>
                        <tr>
                            <td><strong>Weight</strong></td>
                            <td>{int(ah_spec['shipping_weight_lb'])} lbs</td>
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
                    <h3>{doe_title}</h3>
                    <p>{doe_desc}</p>
                </div>
            </div>
            <p style="margin-top: 20px; text-align: center; color: #666; font-size: 0.9em;"><strong>Important:</strong> Check state and local codes and ordinances before purchasing. Product availability and compliance requirements may vary by region.</p>
        </div>
    </div>
"""

        html += self.get_javascript()
        return html

    def generate_ac_furnace_coil(self, ac_spec: Dict, furnace_spec: Dict, coil_spec: Dict) -> str:
        """Generate AC + Gas Furnace + Coil system description"""
        tonnage_display = self.format_tonnage(ac_spec['tonnage'])
        coil_tonnage = self.format_tonnage(coil_spec['tonnage'])
        afue = furnace_spec['afue']
        orientation = coil_spec['orientation']  # Should be 'Upflow' or 'Horizontal' only

        liquid_line = self.format_line_size(str(ac_spec['liquid_line_od_in']))
        suction_line = self.format_line_size(str(ac_spec['suction_line_od_in']))
        coil_liquid = self.format_line_size(str(coil_spec['liquid_line_od_in']))
        coil_suction = self.format_line_size(str(coil_spec['suction_line_od_in']))

        doe_title, doe_desc = self.get_doe_footer()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GOODMAN {tonnage_display} Ton {self.seer_rating} SEER2 R-32 {afue}% AFUE Gas Furnace Air Conditioning System ({orientation} Coil)</title>
    <style>
        {self.get_common_styles()}
    </style>
</head>
<body>
    <div id="product-container">
        <h1>GOODMAN {tonnage_display} Ton {self.seer_rating} SEER2 R-32 {afue}% AFUE Gas Furnace Air Conditioning System ({orientation} Coil)</h1>

        <div class="intro-section">
            <p>Experience reliable home comfort with this complete Goodman {tonnage_display}-ton HVAC system ({orientation} Coil). This matched system combines a high-efficiency {self.seer_rating} SEER2 air conditioner, a {afue}% AFUE single-stage gas furnace with multi-speed ECM blower, and a precision-engineered {orientation.lower()} evaporator coil with factory-installed TXV. Designed for dependable year-round heating and cooling performance, this system delivers excellent energy efficiency, quiet operation, and proven reliability with environmentally-friendly R-32 refrigerant.</p>
        </div>

        <h2>Technical Specifications</h2>

        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="showTab(event, 'ac-specs')">Air Conditioner</button>
                <button class="tab-button" onclick="showTab(event, 'furnace-specs')">Gas Furnace</button>
                <button class="tab-button" onclick="showTab(event, 'coil-specs')">Evaporator Coil</button>
            </div>

            <div id="ac-specs" class="tab-content active">
                <h3>Air Conditioner — {ac_spec['model_number']} Specifications</h3>
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
                            <td>{ac_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Air Conditioner Condenser</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage</strong></td>
                            <td>{tonnage_display} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity</strong></td>
                            <td>{ac_spec['cooling_capacity_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>SEER2 Rating</strong></td>
                            <td>{self.seer_rating}</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Type</strong></td>
                            <td>R-32</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Charge</strong></td>
                            <td>{int(ac_spec['factory_charge_oz'])} oz</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor Type</strong></td>
                            <td>{ac_spec['compressor_type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage/Phase/Frequency</strong></td>
                            <td>{ac_spec['voltage']}V-{ac_spec['phase']}-{ac_spec['frequency_hz']}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{ac_spec['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{int(ac_spec['mop'])} A</td>
                        </tr>
                        <tr>
                            <td><strong>Sound Level</strong></td>
                            <td>{ac_spec['sound_level_dba']} dBA</td>
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
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{int(ac_spec['width_in'])}" × {int(ac_spec['depth_in'])}" × {ac_spec['height_in']}"</td>
                        </tr>
                        <tr>
                            <td><strong>Shipping Weight</strong></td>
                            <td>{int(ac_spec['shipping_weight_lb'])} lbs</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div id="furnace-specs" class="tab-content">
                <h3>Gas Furnace — {furnace_spec['model_number']} Specifications</h3>
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
                            <td>{furnace_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Gas Furnace</td>
                        </tr>
                        <tr>
                            <td><strong>BTU Input</strong></td>
                            <td>{furnace_spec['input_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>BTU Output</strong></td>
                            <td>{furnace_spec['output_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>AFUE</strong></td>
                            <td>{afue}%</td>
                        </tr>
                        <tr>
                            <td><strong>Heating Stages</strong></td>
                            <td>{furnace_spec['heating_stages']}</td>
                        </tr>
                        <tr>
                            <td><strong>Blower Motor Type</strong></td>
                            <td>{furnace_spec['blower_motor_type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Configuration</strong></td>
                            <td>Multi-Position</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage/Phase/Frequency</strong></td>
                            <td>{furnace_spec['voltage']}V-{furnace_spec['phase']}-{furnace_spec['frequency_hz']}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{furnace_spec['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{furnace_spec['mop']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{furnace_spec['width_in']}" × {furnace_spec['depth_in']}" × {furnace_spec['height_in']}"</td>
                        </tr>
                        <tr>
                            <td><strong>Shipping Weight</strong></td>
                            <td>{int(furnace_spec['shipping_weight_lb'])} lbs</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div id="coil-specs" class="tab-content">
                <h3>Evaporator Coil — {coil_spec['model_number']} Specifications</h3>
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
                            <td>{coil_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Cased {orientation} Evaporator Coil</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage</strong></td>
                            <td>{coil_tonnage} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Metering Device</strong></td>
                            <td>Factory-Installed {coil_spec['metering_device']}</td>
                        </tr>
                        <tr>
                            <td><strong>Configuration</strong></td>
                            <td>Cased</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Line Connection</strong></td>
                            <td>{coil_liquid}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Line Connection</strong></td>
                            <td>{coil_suction}</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{coil_spec['width_in']}" × {coil_spec['depth_in']}" × {coil_spec['height_in']}"</td>
                        </tr>
                        <tr>
                            <td><strong>Shipping Weight</strong></td>
                            <td>{int(coil_spec['shipping_weight_lb'])} lbs</td>
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
                    <h3>{doe_title}</h3>
                    <p>{doe_desc}</p>
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

    def generate_hp_furnace_coil(self, hp_spec: Dict, furnace_spec: Dict, coil_spec: Dict) -> str:
        """Generate HP + Gas Furnace + Coil (Dual Fuel) system description"""
        tonnage_display = self.format_tonnage(hp_spec['tonnage'])
        coil_tonnage = self.format_tonnage(coil_spec['tonnage'])
        afue = furnace_spec['afue']
        orientation = coil_spec['orientation']  # Should be 'Upflow' or 'Horizontal' only

        liquid_line = self.format_line_size(str(hp_spec['liquid_line_od_in']))
        suction_line = self.format_line_size(str(hp_spec['suction_line_od_in']))
        coil_liquid = self.format_line_size(str(coil_spec['liquid_line_od_in']))
        coil_suction = self.format_line_size(str(coil_spec['suction_line_od_in']))

        doe_title, doe_desc = self.get_doe_footer()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GOODMAN {tonnage_display} Ton {self.seer_rating} SEER2 R-32 {afue}% AFUE Dual Fuel System ({orientation} Coil)</title>
    <style>
        {self.get_common_styles()}
    </style>
</head>
<body>
    <div id="product-container">
        <h1>GOODMAN {tonnage_display} Ton {self.seer_rating} SEER2 R-32 {afue}% AFUE Dual Fuel System ({orientation} Coil)</h1>

        <div class="intro-section">
            <p>Experience ultimate year-round comfort with this complete Goodman {tonnage_display}-ton dual fuel HVAC system ({orientation} Coil). This advanced matched system combines a high-efficiency {self.seer_rating} SEER2 heat pump, a {afue}% AFUE single-stage gas furnace with multi-speed ECM blower, and a precision-engineered {orientation.lower()} evaporator coil with factory-installed TXV. The dual fuel configuration automatically switches between electric heat pump and gas furnace operation to optimize efficiency and comfort. Designed for exceptional year-round heating and cooling performance, this system delivers outstanding energy efficiency, quiet operation, and proven reliability with environmentally-friendly R-32 refrigerant.</p>
        </div>

        <h2>Technical Specifications</h2>

        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="showTab(event, 'hp-specs')">Heat Pump</button>
                <button class="tab-button" onclick="showTab(event, 'furnace-specs')">Gas Furnace</button>
                <button class="tab-button" onclick="showTab(event, 'coil-specs')">Evaporator Coil</button>
            </div>

            <div id="hp-specs" class="tab-content active">
                <h3>Heat Pump — {hp_spec['model_number']} Specifications</h3>
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
                            <td>{hp_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Heat Pump Condenser</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage</strong></td>
                            <td>{tonnage_display} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Cooling Capacity</strong></td>
                            <td>{hp_spec['cooling_capacity_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>Heating Capacity (47°F)</strong></td>
                            <td>{hp_spec['heating_capacity_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>SEER2 Rating</strong></td>
                            <td>{self.seer_rating}</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Type</strong></td>
                            <td>R-32</td>
                        </tr>
                        <tr>
                            <td><strong>Refrigerant Charge</strong></td>
                            <td>{int(hp_spec['factory_charge_oz'])} oz</td>
                        </tr>
                        <tr>
                            <td><strong>Compressor Type</strong></td>
                            <td>{hp_spec['compressor_type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage/Phase/Frequency</strong></td>
                            <td>{hp_spec['voltage']}V-{hp_spec['phase']}-{hp_spec['frequency_hz']}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{hp_spec['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{int(hp_spec['mop'])} A</td>
                        </tr>
                        <tr>
                            <td><strong>Sound Level</strong></td>
                            <td>{hp_spec['sound_level_dba']} dBA</td>
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
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{int(hp_spec['width_in'])}" × {int(hp_spec['depth_in'])}" × {hp_spec['height_in']}"</td>
                        </tr>
                        <tr>
                            <td><strong>Shipping Weight</strong></td>
                            <td>{int(hp_spec['shipping_weight_lb'])} lbs</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div id="furnace-specs" class="tab-content">
                <h3>Gas Furnace — {furnace_spec['model_number']} Specifications</h3>
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
                            <td>{furnace_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Gas Furnace</td>
                        </tr>
                        <tr>
                            <td><strong>BTU Input</strong></td>
                            <td>{furnace_spec['input_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>BTU Output</strong></td>
                            <td>{furnace_spec['output_btuh']:,} BTU/h</td>
                        </tr>
                        <tr>
                            <td><strong>AFUE</strong></td>
                            <td>{afue}%</td>
                        </tr>
                        <tr>
                            <td><strong>Heating Stages</strong></td>
                            <td>{furnace_spec['heating_stages']}</td>
                        </tr>
                        <tr>
                            <td><strong>Blower Motor Type</strong></td>
                            <td>{furnace_spec['blower_motor_type']}</td>
                        </tr>
                        <tr>
                            <td><strong>Configuration</strong></td>
                            <td>Multi-Position</td>
                        </tr>
                        <tr>
                            <td><strong>Voltage/Phase/Frequency</strong></td>
                            <td>{furnace_spec['voltage']}V-{furnace_spec['phase']}-{furnace_spec['frequency_hz']}Hz</td>
                        </tr>
                        <tr>
                            <td><strong>Min Circuit Ampacity</strong></td>
                            <td>{furnace_spec['mca']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Max Overcurrent Protection</strong></td>
                            <td>{furnace_spec['mop']} A</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{furnace_spec['width_in']}" × {furnace_spec['depth_in']}" × {furnace_spec['height_in']}"</td>
                        </tr>
                        <tr>
                            <td><strong>Shipping Weight</strong></td>
                            <td>{int(furnace_spec['shipping_weight_lb'])} lbs</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div id="coil-specs" class="tab-content">
                <h3>Evaporator Coil — {coil_spec['model_number']} Specifications</h3>
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
                            <td>{coil_spec['model_number']}</td>
                        </tr>
                        <tr>
                            <td><strong>Product Type</strong></td>
                            <td>Cased {orientation} Evaporator Coil</td>
                        </tr>
                        <tr>
                            <td><strong>Tonnage</strong></td>
                            <td>{coil_tonnage} Ton</td>
                        </tr>
                        <tr>
                            <td><strong>Metering Device</strong></td>
                            <td>Factory-Installed {coil_spec['metering_device']}</td>
                        </tr>
                        <tr>
                            <td><strong>Configuration</strong></td>
                            <td>Cased</td>
                        </tr>
                        <tr>
                            <td><strong>Liquid Line Connection</strong></td>
                            <td>{coil_liquid}</td>
                        </tr>
                        <tr>
                            <td><strong>Suction Line Connection</strong></td>
                            <td>{coil_suction}</td>
                        </tr>
                        <tr>
                            <td><strong>Dimensions (W×D×H)</strong></td>
                            <td>{coil_spec['width_in']}" × {coil_spec['depth_in']}" × {coil_spec['height_in']}"</td>
                        </tr>
                        <tr>
                            <td><strong>Shipping Weight</strong></td>
                            <td>{int(coil_spec['shipping_weight_lb'])} lbs</td>
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
                    <h3>{doe_title}</h3>
                    <p>{doe_desc}</p>
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

    def generate_ac_condenser_only(self, ac_spec: Dict) -> str:
        """Generate HTML for AC condenser only"""
        tonnage_str = self.format_tonnage(ac_spec['tonnage'])
        liquid_line = self.format_line_size(ac_spec.get('liquid_line_od_in', 0.375))
        suction_line = self.format_line_size(ac_spec.get('suction_line_od_in', 0.75))
        doe_title, doe_desc = self.get_doe_footer()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Goodman {tonnage_str} Ton R-32 Air Conditioner Condenser - {ac_spec['model_number']}</title>
    <style>{self.get_common_styles()}</style>
</head>
<body>
    <div id="product-container">
        <h1>Goodman {tonnage_str} Ton R-32 Air Conditioner Condenser - {ac_spec['model_number']}</h1>

        <div class="intro-section">
            <p>The Goodman {ac_spec['model_number']} is a high-efficiency {tonnage_str}-ton air conditioning condenser unit rated at {self.seer_rating} SEER2. This outdoor unit uses eco-friendly R-32 refrigerant and features a reliable {ac_spec.get('compressor_type', 'scroll').lower()} compressor for quiet, efficient cooling. Designed for residential applications, it provides consistent comfort while meeting modern energy efficiency standards. This condenser requires a compatible indoor evaporator coil or air handler (sold separately) to complete your cooling system.</p>
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
                    <td>Goodman</td>
                </tr>
                <tr>
                    <td><strong>Model Number</strong></td>
                    <td>{ac_spec['model_number']}</td>
                </tr>
                <tr>
                    <td><strong>Product Type</strong></td>
                    <td>Air Conditioning Condenser</td>
                </tr>
                <tr>
                    <td><strong>Tonnage</strong></td>
                    <td>{tonnage_str} Tons</td>
                </tr>
                <tr>
                    <td><strong>Cooling Capacity</strong></td>
                    <td>{ac_spec['cooling_capacity_btuh']:,} BTU/h</td>
                </tr>
                <tr>
                    <td><strong>SEER2 Rating</strong></td>
                    <td>{self.seer_rating}</td>
                </tr>
                <tr>
                    <td><strong>Refrigerant Type</strong></td>
                    <td>R-32</td>
                </tr>
                <tr>
                    <td><strong>Refrigerant Charge</strong></td>
                    <td>{ac_spec.get('factory_charge_oz', 'Varies')} oz</td>
                </tr>
                <tr>
                    <td><strong>Compressor Type</strong></td>
                    <td>{ac_spec.get('compressor_type', 'Scroll')}</td>
                </tr>
                <tr>
                    <td><strong>Voltage/Phase/Frequency</strong></td>
                    <td>{ac_spec.get('voltage', 208)}-{ac_spec.get('voltage_max', 230)}V/{ac_spec.get('phase', 1)}-Ph/{ac_spec.get('frequency_hz', 60)}Hz</td>
                </tr>
                <tr>
                    <td><strong>Min Circuit Ampacity</strong></td>
                    <td>{ac_spec.get('mca', 'N/A')} A</td>
                </tr>
                <tr>
                    <td><strong>Max Overcurrent Protection</strong></td>
                    <td>{ac_spec.get('mop', 'N/A')} A</td>
                </tr>
                <tr>
                    <td><strong>Sound Level</strong></td>
                    <td>{ac_spec.get('sound_level_dba', 'N/A')} dBA</td>
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
                    <td><strong>Dimensions (W×D×H)</strong></td>
                    <td>{ac_spec.get('width_in', 'N/A')}" × {ac_spec.get('depth_in', 'N/A')}" × {ac_spec.get('height_in', 'N/A')}"</td>
                </tr>
                <tr>
                    <td><strong>Shipping Weight</strong></td>
                    <td>{int(ac_spec.get('shipping_weight_lb', 0))} lbs</td>
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
                    <h3>{doe_title}</h3>
                    <p>{doe_desc}</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
        return html

    def generate_hp_condenser_only(self, hp_spec: Dict) -> str:
        """Generate HTML for heat pump condenser only"""
        tonnage_str = self.format_tonnage(hp_spec['tonnage'])
        liquid_line = self.format_line_size(hp_spec.get('liquid_line_od_in', 0.375))
        suction_line = self.format_line_size(hp_spec.get('suction_line_od_in', 0.75))
        doe_title, doe_desc = self.get_doe_footer()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Goodman {tonnage_str} Ton R-32 Heat Pump Condenser - {hp_spec['model_number']}</title>
    <style>{self.get_common_styles()}</style>
</head>
<body>
    <div id="product-container">
        <h1>Goodman {tonnage_str} Ton R-32 Heat Pump Condenser - {hp_spec['model_number']}</h1>

        <div class="intro-section">
            <p>The Goodman {hp_spec['model_number']} is a high-efficiency {tonnage_str}-ton heat pump outdoor unit rated at {self.seer_rating} SEER2. This versatile system uses eco-friendly R-32 refrigerant and provides both heating and cooling capabilities with a reliable {hp_spec.get('compressor_type', 'scroll').lower()} compressor. Designed for year-round comfort in moderate climates, it delivers efficient operation while meeting modern energy efficiency standards. This heat pump requires a compatible indoor evaporator coil or air handler (sold separately) to complete your system.</p>
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
                    <td>Goodman</td>
                </tr>
                <tr>
                    <td><strong>Model Number</strong></td>
                    <td>{hp_spec['model_number']}</td>
                </tr>
                <tr>
                    <td><strong>Product Type</strong></td>
                    <td>Heat Pump Condenser</td>
                </tr>
                <tr>
                    <td><strong>Tonnage</strong></td>
                    <td>{tonnage_str} Tons</td>
                </tr>
                <tr>
                    <td><strong>Cooling Capacity</strong></td>
                    <td>{hp_spec['cooling_capacity_btuh']:,} BTU/h</td>
                </tr>
                <tr>
                    <td><strong>Heating Capacity (47°F)</strong></td>
                    <td>{hp_spec.get('heating_capacity_47f_btuh', 0):,} BTU/h</td>
                </tr>
                <tr>
                    <td><strong>SEER2 Rating</strong></td>
                    <td>{self.seer_rating}</td>
                </tr>
                <tr>
                    <td><strong>Refrigerant Type</strong></td>
                    <td>R-32</td>
                </tr>
                <tr>
                    <td><strong>Refrigerant Charge</strong></td>
                    <td>{hp_spec.get('factory_charge_oz', 'Varies')} oz</td>
                </tr>
                <tr>
                    <td><strong>Compressor Type</strong></td>
                    <td>{hp_spec.get('compressor_type', 'Scroll')}</td>
                </tr>
                <tr>
                    <td><strong>Voltage/Phase/Frequency</strong></td>
                    <td>{hp_spec.get('voltage', 208)}-{hp_spec.get('voltage_max', 230)}V/{hp_spec.get('phase', 1)}-Ph/{hp_spec.get('frequency_hz', 60)}Hz</td>
                </tr>
                <tr>
                    <td><strong>Min Circuit Ampacity</strong></td>
                    <td>{hp_spec.get('mca', 'N/A')} A</td>
                </tr>
                <tr>
                    <td><strong>Max Overcurrent Protection</strong></td>
                    <td>{hp_spec.get('mop', 'N/A')} A</td>
                </tr>
                <tr>
                    <td><strong>Sound Level</strong></td>
                    <td>{hp_spec.get('sound_level_dba', 'N/A')} dBA</td>
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
                    <td><strong>Dimensions (W×D×H)</strong></td>
                    <td>{hp_spec.get('width_in', 'N/A')}" × {hp_spec.get('depth_in', 'N/A')}" × {hp_spec.get('height_in', 'N/A')}"</td>
                </tr>
                <tr>
                    <td><strong>Shipping Weight</strong></td>
                    <td>{int(hp_spec.get('shipping_weight_lb', 0))} lbs</td>
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
                    <h3>{doe_title}</h3>
                    <p>{doe_desc}</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
        return html

    def generate_air_handler_only(self, ah_spec: Dict) -> str:
        """Generate HTML for air handler only"""
        tonnage_str = self.format_tonnage(ah_spec.get('tonnage', 2.0))
        liquid_line = self.format_line_size(ah_spec.get('liquid_line_od_in', 0.375))
        suction_line = self.format_line_size(ah_spec.get('suction_line_od_in', 0.75))
        doe_title, doe_desc = self.get_doe_footer()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Goodman {tonnage_str} Ton R-32 Air Handler - {ah_spec['model_number']}</title>
    <style>{self.get_common_styles()}</style>
</head>
<body>
    <div id="product-container">
        <h1>Goodman {tonnage_str} Ton R-32 Air Handler - {ah_spec['model_number']}</h1>

        <div class="intro-section">
            <p>The Goodman {ah_spec['model_number']} is a high-efficiency multi-position air handler designed for use with R-32 refrigerant systems. Featuring an advanced {ah_spec.get('blower_motor_type', 'ECM')} blower motor, this unit delivers precise airflow control and reduced energy consumption. The multi-position cabinet design allows for flexible installation in upflow, downflow, or horizontal configurations. This air handler requires a compatible outdoor condensing unit (sold separately) to complete your heating and cooling system.</p>
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
                    <td>Goodman</td>
                </tr>
                <tr>
                    <td><strong>Model Number</strong></td>
                    <td>{ah_spec['model_number']}</td>
                </tr>
                <tr>
                    <td><strong>Product Type</strong></td>
                    <td>Air Handler</td>
                </tr>
                <tr>
                    <td><strong>Tonnage</strong></td>
                    <td>{tonnage_str} Tons</td>
                </tr>
                <tr>
                    <td><strong>Airflow Capacity</strong></td>
                    <td>{ah_spec.get('airflow_cfm', 'Varies')} CFM</td>
                </tr>
                <tr>
                    <td><strong>Blower Motor Type</strong></td>
                    <td>{ah_spec.get('blower_motor_type', 'ECM')}</td>
                </tr>
                <tr>
                    <td><strong>Motor Horsepower</strong></td>
                    <td>{ah_spec.get('motor_hp', 'N/A')} HP</td>
                </tr>
                <tr>
                    <td><strong>Refrigerant Type</strong></td>
                    <td>R-32</td>
                </tr>
                <tr>
                    <td><strong>Voltage/Phase/Frequency</strong></td>
                    <td>{ah_spec.get('voltage', 115)}V/{ah_spec.get('phase', 1)}-Ph/{ah_spec.get('frequency_hz', 60)}Hz</td>
                </tr>
                <tr>
                    <td><strong>Min Circuit Ampacity</strong></td>
                    <td>{ah_spec.get('mca', 'N/A')} A</td>
                </tr>
                <tr>
                    <td><strong>Max Overcurrent Protection</strong></td>
                    <td>{ah_spec.get('mop', 'N/A')} A</td>
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
                    <td><strong>Cabinet Configuration</strong></td>
                    <td>Multi-Position</td>
                </tr>
                <tr>
                    <td><strong>Dimensions (H×W×D)</strong></td>
                    <td>{ah_spec.get('height_in', 'N/A')}" × {ah_spec.get('width_in', 'N/A')}" × {ah_spec.get('depth_in', 'N/A')}"</td>
                </tr>
                <tr>
                    <td><strong>Shipping Weight</strong></td>
                    <td>{int(ah_spec.get('shipping_weight_lb', 0))} lbs</td>
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
                    <h3>{doe_title}</h3>
                    <p>{doe_desc}</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
        return html

    def generate_coil_only(self, coil_spec: Dict) -> str:
        """Generate HTML for evaporator coil only"""
        tonnage_str = self.format_tonnage(coil_spec.get('tonnage', 2.0))
        orientation = coil_spec.get('orientation', 'Multi-Position')
        liquid_line = self.format_line_size(coil_spec.get('liquid_line_od_in', 0.375))
        suction_line = self.format_line_size(coil_spec.get('suction_line_od_in', 0.75))
        doe_title, doe_desc = self.get_doe_footer()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Goodman {tonnage_str} Ton R-32 {orientation} Evaporator Coil - {coil_spec['model_number']}</title>
    <style>{self.get_common_styles()}</style>
</head>
<body>
    <div id="product-container">
        <h1>Goodman {tonnage_str} Ton R-32 {orientation} Evaporator Coil - {coil_spec['model_number']}</h1>

        <div class="intro-section">
            <p>The Goodman {coil_spec['model_number']} is a high-efficiency {tonnage_str}-ton {orientation.lower()} evaporator coil designed for use with R-32 refrigerant systems. This cased coil features {coil_spec.get('metering_device', 'TXV')} metering for optimal refrigerant control and includes a factory-installed drain pan for easy installation. Designed for {orientation.lower()} applications, it pairs with compatible outdoor condensing units to deliver reliable cooling performance. This evaporator coil requires a compatible outdoor unit and furnace or air handler (sold separately) to complete your system.</p>
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
                    <td>Goodman</td>
                </tr>
                <tr>
                    <td><strong>Model Number</strong></td>
                    <td>{coil_spec['model_number']}</td>
                </tr>
                <tr>
                    <td><strong>Product Type</strong></td>
                    <td>{orientation} Evaporator Coil</td>
                </tr>
                <tr>
                    <td><strong>Tonnage</strong></td>
                    <td>{tonnage_str} Tons</td>
                </tr>
                <tr>
                    <td><strong>Refrigerant Type</strong></td>
                    <td>R-32</td>
                </tr>
                <tr>
                    <td><strong>Metering Device</strong></td>
                    <td>{coil_spec.get('metering_device', 'TXV')}</td>
                </tr>
                <tr>
                    <td><strong>Coil Configuration</strong></td>
                    <td>{orientation}</td>
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
                    <td><strong>Dimensions (W×D×H)</strong></td>
                    <td>{coil_spec.get('width_in', 'N/A')}" × {coil_spec.get('depth_in', 'N/A')}" × {coil_spec.get('height_in', 'N/A')}"</td>
                </tr>
                <tr>
                    <td><strong>Shipping Weight</strong></td>
                    <td>{int(coil_spec.get('shipping_weight_lb', 0))} lbs</td>
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
                    <h3>{doe_title}</h3>
                    <p>{doe_desc}</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
        return html

    def generate_furnace_only(self, furnace_spec: Dict) -> str:
        """Generate HTML for gas furnace only"""
        afue = furnace_spec.get('afue_percent', 80)
        doe_title, doe_desc = self.get_doe_footer()

        # Warranty depends on heat exchanger type
        if afue >= 90:
            warranty_he = "Lifetime"
        else:
            warranty_he = "Lifetime"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Goodman {afue}% AFUE Gas Furnace - {furnace_spec['model_number']}</title>
    <style>{self.get_common_styles()}</style>
</head>
<body>
    <div id="product-container">
        <h1>Goodman {afue}% AFUE Gas Furnace - {furnace_spec['model_number']}</h1>

        <div class="intro-section">
            <p>The Goodman {furnace_spec['model_number']} is a {afue}% AFUE-rated gas furnace delivering {furnace_spec.get('output_btuh', 0):,} BTU/h of heating output. This reliable heating solution features a {furnace_spec.get('heating_stages', 'single-stage')} design and {furnace_spec.get('blower_motor_type', 'multi-speed ECM')} blower motor for consistent comfort and energy efficiency. Designed for residential applications, this furnace provides dependable heating performance with modern efficiency standards. This unit requires professional installation and may require a compatible evaporator coil (sold separately) for air conditioning applications.</p>
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
                    <td>Goodman</td>
                </tr>
                <tr>
                    <td><strong>Model Number</strong></td>
                    <td>{furnace_spec['model_number']}</td>
                </tr>
                <tr>
                    <td><strong>Product Type</strong></td>
                    <td>Gas Furnace</td>
                </tr>
                <tr>
                    <td><strong>AFUE Rating</strong></td>
                    <td>{afue}%</td>
                </tr>
                <tr>
                    <td><strong>Input BTU/h</strong></td>
                    <td>{furnace_spec.get('input_btuh', 0):,}</td>
                </tr>
                <tr>
                    <td><strong>Output BTU/h</strong></td>
                    <td>{furnace_spec.get('output_btuh', 0):,}</td>
                </tr>
                <tr>
                    <td><strong>Fuel Type</strong></td>
                    <td>Natural Gas</td>
                </tr>
                <tr>
                    <td><strong>Heating Stages</strong></td>
                    <td>{furnace_spec.get('heating_stages', 'Single Stage')}</td>
                </tr>
                <tr>
                    <td><strong>Blower Motor Type</strong></td>
                    <td>{furnace_spec.get('blower_motor_type', 'Multi-Speed ECM')}</td>
                </tr>
                <tr>
                    <td><strong>Voltage/Phase/Frequency</strong></td>
                    <td>{furnace_spec.get('voltage', 115)}V/{furnace_spec.get('phase', 1)}-Ph/{furnace_spec.get('frequency_hz', 60)}Hz</td>
                </tr>
                <tr>
                    <td><strong>Min Circuit Ampacity</strong></td>
                    <td>{furnace_spec.get('mca', 'N/A')} A</td>
                </tr>
                <tr>
                    <td><strong>Max Overcurrent Protection</strong></td>
                    <td>{furnace_spec.get('mop', 'N/A')} A</td>
                </tr>
                <tr>
                    <td><strong>Dimensions (H×W×D)</strong></td>
                    <td>{furnace_spec.get('height_in', 'N/A')}" × {furnace_spec.get('width_in', 'N/A')}" × {furnace_spec.get('depth_in', 'N/A')}"</td>
                </tr>
                <tr>
                    <td><strong>Shipping Weight</strong></td>
                    <td>{int(furnace_spec.get('shipping_weight_lb', 0))} lbs</td>
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
                    <div class="warranty-years">∞</div>
                    <div class="warranty-label">{warranty_he} Heat Exchanger Warranty</div>
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
                    <h3>{doe_title}</h3>
                    <p>{doe_desc}</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
        return html


if __name__ == "__main__":
    # Test the HTML generator
    print("HTML Generator Test")
    print("=" * 80)

    # Test with sample data
    test_ac_spec = {
        'model_number': 'GLXS5BA1810',
        'tonnage': 1.5,
        'cooling_capacity_btuh': 18000,
        'seer2': 15.2,
        'eer2': 12.5,
        'compressor_type': 'Scroll',
        'voltage': 208,
        'phase': 1,
        'frequency_hz': 60,
        'mca': 15,
        'mop': 20,
        'factory_charge_oz': 96,
        'liquid_line_od_in': 0.375,
        'suction_line_od_in': 0.75,
        'sound_level_dba': 72,
        'height_in': 30.5,
        'width_in': 29,
        'depth_in': 29,
        'shipping_weight_lb': 135
    }

    test_ah_spec = {
        'model_number': 'AMST24BU13',
        'blower_motor_type': 'ECM',
        'motor_hp': 0.5,
        'airflow_cfm': 800,
        'voltage': 115,
        'phase': 1,
        'frequency_hz': 60,
        'mca': 12,
        'mop': 15,
        'height_in': 50,
        'width_in': 17.5,
        'depth_in': 21,
        'shipping_weight_lb': 85
    }

    # Test with 15.2 SEER (Nationwide)
    generator = HTMLGenerator(15.2)
    html = generator.generate_ac_airhandler(test_ac_spec, test_ah_spec)
    print(f"✅ Generated AC + Air Handler HTML ({len(html):,} characters)")
    print(f"   DOE Footer: {generator.get_doe_footer()[0]}")

    # Test with 13.4 SEER (Northern only)
    generator_low = HTMLGenerator(13.4)
    html_low = generator_low.generate_ac_airhandler(test_ac_spec, test_ah_spec)
    print(f"✅ Generated AC + Air Handler HTML for low SEER ({len(html_low):,} characters)")
    print(f"   DOE Footer: {generator_low.get_doe_footer()[0]}")

    print("\n✅ HTML Generator ready for integration")
