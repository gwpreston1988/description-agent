"""
Content Generator - Generates titles, introductions, and spec tables for HTML
"""

from typing import Dict, List
from spec_extractor import SpecExtractor


class ContentGenerator:
    """Generate dynamic content for HVAC system descriptions"""

    def __init__(self, spec_extractor: SpecExtractor):
        """
        Initialize with a SpecExtractor instance

        Args:
            spec_extractor: SpecExtractor instance with loaded specs
        """
        self.extractor = spec_extractor

    def generate_title(self, system_type: str, specs: Dict[str, Dict], seer_rating: float) -> str:
        """
        Generate HTML title (H1) for the system

        Args:
            system_type: System type from SKU parser
            specs: Dictionary of component specs
            seer_rating: SEER2 rating

        Returns:
            Title string
        """
        # Extract tonnage
        tonnage = self.extractor.extract_system_tonnage(specs)

        # Determine system category
        if 'AC' in system_type and 'HP' not in system_type:
            system_category = "Air Conditioning"
        elif 'HP' in system_type or 'DualFuel' in system_type:
            if 'DualFuel' in system_type:
                system_category = "Dual Fuel Heat Pump"
            else:
                system_category = "Heat Pump"
        else:
            system_category = "HVAC"

        # Build title
        if tonnage > 0:
            title = f"GOODMAN {tonnage} Ton {seer_rating} SEER2 R-410A {system_category} System"
        else:
            title = f"GOODMAN {seer_rating} SEER2 R-410A {system_category} System"

        # Add configuration details
        if 'Wall' in system_type:
            title += " with Wall-Hung Air Handler"
        elif 'AirHandler' in system_type:
            title += " with Air Handler"
        elif 'Furnace' in system_type and 'Coil' in system_type:
            if 'Upflow' in system_type:
                title += " with Gas Furnace and Upflow Coil"
            elif 'Horizontal' in system_type:
                title += " with Gas Furnace and Horizontal Coil"

        return title

    def generate_intro(self, system_type: str, specs: Dict[str, Dict], seer_rating: float) -> str:
        """
        Generate introduction paragraph

        Args:
            system_type: System type from SKU parser
            specs: Dictionary of component specs
            seer_rating: SEER2 rating

        Returns:
            Introduction paragraph HTML
        """
        tonnage = self.extractor.extract_system_tonnage(specs)

        # Base intro templates
        if 'AC_AirHandler_Wall' in system_type:
            intro = f"Experience superior cooling comfort with this complete Goodman {tonnage}-ton air conditioning system featuring a space-saving wall-hung air handler with integrated electric heat. This matched system combines a high-efficiency {seer_rating} SEER2 air conditioner with a wall-mounted air handler that includes a electric heat kit for reliable winter heating. Perfect for homes where floor space is limited, this system delivers efficient cooling and heating with R-410A refrigerant while maximizing your usable living space."

        elif 'AC_AirHandler' in system_type:
            intro = f"This complete Goodman {tonnage}-ton air conditioning system pairs a high-efficiency {seer_rating} SEER2 outdoor condensing unit with a versatile indoor air handler. Designed for reliable cooling performance and quiet operation, this matched system uses R-410A refrigerant and delivers consistent comfort throughout your home. The indoor air handler features a multi-speed blower motor for optimized airflow and energy efficiency."

        elif 'HP_AirHandler_Wall' in system_type:
            intro = f"Experience year-round comfort with this complete Goodman {tonnage}-ton heat pump system featuring a space-saving wall-hung air handler. This matched system combines a high-efficiency {seer_rating} SEER2 heat pump with a wall-mounted air handler that provides both heating and cooling. Perfect for homes where floor space is limited, this system delivers efficient climate control with R-410A refrigerant while maximizing your usable living space."

        elif 'HP_AirHandler' in system_type:
            intro = f"This complete Goodman {tonnage}-ton heat pump system delivers year-round comfort with a high-efficiency {seer_rating} SEER2 outdoor unit matched with a versatile indoor air handler. Providing both heating and cooling from a single system, this matched pair uses R-410A refrigerant for reliable performance in all seasons. The indoor air handler features advanced airflow control for optimal comfort and efficiency."

        elif 'DualFuel' in system_type or ('HP' in system_type and 'Furnace' in system_type):
            afue = '80%' if '80AFUE' in system_type else '92%'
            orientation = 'upflow' if 'Upflow' in system_type else 'horizontal'
            intro = f"This advanced Goodman dual fuel system combines the efficiency of a {tonnage}-ton {seer_rating} SEER2 heat pump with the reliability of a {afue} AFUE gas furnace backup. This complete matched system includes a {orientation} evaporator coil and uses R-410A refrigerant. The system automatically switches between electric heat pump operation and gas furnace backup based on outdoor temperature and efficiency, ensuring maximum comfort and minimum operating costs year-round."

        elif 'AC' in system_type and 'Furnace' in system_type:
            afue = '80%' if '80AFUE' in system_type else '92%'
            orientation = 'upflow' if 'Upflow' in system_type else 'horizontal'
            intro = f"This complete Goodman heating and cooling system combines a {tonnage}-ton {seer_rating} SEER2 air conditioner with a {afue} AFUE gas furnace and matched {orientation} evaporator coil. Using R-410A refrigerant, this system delivers reliable year-round comfort with high efficiency ratings for both heating and cooling. The matched coil ensures optimal performance and energy savings while the gas furnace provides dependable heat during cold weather."

        else:
            intro = f"This Goodman HVAC system features high-efficiency performance with a {seer_rating} SEER2 rating and R-410A refrigerant. Designed for reliable comfort and energy savings."

        return intro

    def generate_spec_table_rows(self, component_spec: Dict) -> List[Dict[str, str]]:
        """
        Generate spec table rows for a single component

        Args:
            component_spec: Specification dictionary for one component

        Returns:
            List of dictionaries with 'label' and 'value' keys
        """
        rows = []
        equipment_type = component_spec.get('equipment_type', 'Unknown')

        # Common rows for all equipment
        rows.append({'label': 'Manufacturer', 'value': component_spec.get('brand', 'Goodman')})

        # Tonnage (for condensers and air handlers)
        if 'tonnage' in component_spec and component_spec['tonnage']:
            rows.append({'label': 'Tonnage', 'value': self.extractor.format_value(component_spec['tonnage'], 'tonnage')})

        # Refrigerant
        if 'refrigerant_type' in component_spec:
            rows.append({'label': 'Refrigerant', 'value': component_spec.get('refrigerant_type', 'R-410A')})

        # Model Number
        rows.append({'label': 'SKU/Model No', 'value': component_spec.get('model_number', 'N/A')})

        # Equipment Type
        rows.append({'label': 'Product Type', 'value': equipment_type})

        # Type-specific specs
        if 'Condenser' in equipment_type or 'Heat Pump' in equipment_type:
            self._add_condenser_specs(rows, component_spec)
        elif 'Air Handler' in equipment_type:
            self._add_air_handler_specs(rows, component_spec)
        elif 'Furnace' in equipment_type:
            self._add_furnace_specs(rows, component_spec)
        elif 'Coil' in equipment_type:
            self._add_coil_specs(rows, component_spec)

        return rows

    def _add_condenser_specs(self, rows: List[Dict], spec: Dict):
        """Add condenser-specific specs"""
        if 'cooling_capacity_btuh' in spec and spec['cooling_capacity_btuh']:
            rows.append({'label': 'Cooling Capacity', 'value': self.extractor.format_value(spec['cooling_capacity_btuh'], 'cooling_capacity_btuh')})

        if 'heating_capacity_btuh' in spec and spec['heating_capacity_btuh']:
            rows.append({'label': 'Heating Capacity', 'value': self.extractor.format_value(spec['heating_capacity_btuh'], 'heating_capacity_btuh')})

        if 'seer2' in spec and spec['seer2']:
            rows.append({'label': 'SEER2 Rating', 'value': f"Up to {spec['seer2']}"})

        if 'eer2' in spec and spec['eer2']:
            rows.append({'label': 'EER2 Rating', 'value': str(spec['eer2'])})
        else:
            rows.append({'label': 'EER2 Rating', 'value': 'None'})

        if 'hspf2' in spec and spec['hspf2']:
            rows.append({'label': 'HSPF2 Rating', 'value': str(spec['hspf2'])})

        if 'compressor_type' in spec:
            rows.append({'label': 'Compressor Type', 'value': spec['compressor_type']})

        if 'voltage' in spec:
            voltage = spec['voltage']
            phase = spec.get('phase', 1)
            freq = spec.get('frequency_hz', 60)
            rows.append({'label': 'Voltage', 'value': f"{voltage}V / {phase}Ph / {freq}Hz"})

        if 'mca' in spec:
            rows.append({'label': 'Min Circuit Ampacity', 'value': f"{spec['mca']} A"})

        if 'mop' in spec:
            rows.append({'label': 'Max Overcurrent Protection', 'value': f"{spec['mop']} A"})

        if 'liquid_line_od_in' in spec:
            rows.append({'label': 'Liquid Line Size', 'value': self.extractor.format_value(spec['liquid_line_od_in'], 'liquid_line_od_in')})

        if 'suction_line_od_in' in spec:
            rows.append({'label': 'Suction Line Size', 'value': self.extractor.format_value(spec['suction_line_od_in'], 'suction_line_od_in')})

        if 'factory_charge_oz' in spec:
            rows.append({'label': 'Refrigerant Charge', 'value': self.extractor.format_value(spec['factory_charge_oz'], 'factory_charge_oz')})

        self._add_physical_dimensions(rows, spec)

        if 'sound_level_dba' in spec:
            rows.append({'label': 'Sound Level', 'value': f"{spec['sound_level_dba']} dBA"})

    def _add_air_handler_specs(self, rows: List[Dict], spec: Dict):
        """Add air handler-specific specs"""
        if 'motor_type' in spec:
            rows.append({'label': 'Motor Type', 'value': spec['motor_type']})

        if 'motor_hp' in spec and spec['motor_hp']:
            rows.append({'label': 'Motor HP', 'value': f"{spec['motor_hp']} HP"})
        else:
            rows.append({'label': 'Motor HP', 'value': 'N/A HP'})

        if 'electric_heat_kw' in spec and spec['electric_heat_kw']:
            rows.append({'label': 'Integrated Electric Heat', 'value': f"{spec['electric_heat_kw']} kW"})

        if 'nominal_cooling_capacity_btuh' in spec and spec['nominal_cooling_capacity_btuh']:
            rows.append({'label': 'Nominal Cooling Capacity', 'value': self.extractor.format_value(spec['nominal_cooling_capacity_btuh'], 'nominal_cooling_capacity_btuh')})

        if 'airflow_cfm' in spec and spec['airflow_cfm']:
            rows.append({'label': 'Airflow', 'value': f"{spec['airflow_cfm']} CFM"})
        else:
            rows.append({'label': 'Airflow', 'value': 'None CFM'})

        if 'voltage' in spec:
            voltage = spec['voltage']
            phase = spec.get('phase', 1)
            freq = spec.get('frequency_hz', 60)
            rows.append({'label': 'Voltage', 'value': f"{voltage}V / {phase}Ph / {freq}Hz"})

        if 'mca' in spec:
            rows.append({'label': 'Min Circuit Ampacity', 'value': f"{spec['mca']} A"})

        if 'mop' in spec:
            rows.append({'label': 'Max Overcurrent Device', 'value': f"{spec['mop']} A"})

        if 'liquid_line_connection_od_in' in spec:
            rows.append({'label': 'Liquid Line Connection', 'value': self.extractor.format_value(spec['liquid_line_connection_od_in'], 'liquid_line_connection_od_in')})

        if 'suction_line_connection_od_in' in spec:
            rows.append({'label': 'Suction Line Connection', 'value': self.extractor.format_value(spec['suction_line_connection_od_in'], 'suction_line_connection_od_in')})

        if 'metering_device' in spec:
            rows.append({'label': 'Metering Device', 'value': spec['metering_device']})

        self._add_physical_dimensions(rows, spec)

    def _add_furnace_specs(self, rows: List[Dict], spec: Dict):
        """Add furnace-specific specs"""
        if 'afue' in spec:
            rows.append({'label': 'AFUE Rating', 'value': f"{spec['afue']}%"})

        if 'input_btuh' in spec:
            rows.append({'label': 'Input Capacity', 'value': self.extractor.format_value(spec['input_btuh'], 'input_btuh')})

        if 'output_btuh' in spec:
            rows.append({'label': 'Output Capacity', 'value': self.extractor.format_value(spec['output_btuh'], 'output_btuh')})

        if 'airflow_cfm' in spec:
            rows.append({'label': 'Airflow', 'value': f"{spec['airflow_cfm']} CFM"})

        if 'gas_type' in spec:
            rows.append({'label': 'Fuel Type', 'value': spec['gas_type']})

        if 'voltage' in spec:
            rows.append({'label': 'Voltage', 'value': f"{spec['voltage']}V"})

        if 'ignition_type' in spec:
            rows.append({'label': 'Ignition Type', 'value': spec['ignition_type']})

        self._add_physical_dimensions(rows, spec)

    def _add_coil_specs(self, rows: List[Dict], spec: Dict):
        """Add evaporator coil-specific specs"""
        if 'coil_type' in spec:
            rows.append({'label': 'Coil Type', 'value': spec['coil_type']})

        if 'configuration' in spec:
            rows.append({'label': 'Configuration', 'value': spec['configuration']})

        if 'liquid_line_connection_od_in' in spec:
            rows.append({'label': 'Liquid Line Connection', 'value': self.extractor.format_value(spec['liquid_line_connection_od_in'], 'liquid_line_connection_od_in')})

        if 'suction_line_connection_od_in' in spec:
            rows.append({'label': 'Suction Line Connection', 'value': self.extractor.format_value(spec['suction_line_connection_od_in'], 'suction_line_connection_od_in')})

        if 'metering_device' in spec:
            rows.append({'label': 'Metering Device', 'value': spec['metering_device']})

        self._add_physical_dimensions(rows, spec)

    def _add_physical_dimensions(self, rows: List[Dict], spec: Dict):
        """Add physical dimension specs"""
        if all(k in spec for k in ['height_in', 'width_in', 'depth_in']):
            dims = f"{spec['height_in']}\" × {spec['width_in']}\" × {spec['depth_in']}\""
            rows.append({'label': 'Dimensions (H×W×D)', 'value': dims})

        if 'shipping_weight_lb' in spec:
            rows.append({'label': 'Weight', 'value': f"{spec['shipping_weight_lb']} lbs"})


def test_content_generator():
    """Test the content generator"""
    from pathlib import Path

    print("Content Generator Test")
    print("=" * 80)

    # Load specs
    specs_file = Path(__file__).parent.parent / "15.2_SEER2" / "Specs" / "15.2_specs.json"
    extractor = SpecExtractor(str(specs_file))
    generator = ContentGenerator(extractor)

    # Test with a 2-component system
    print("\n1. Testing AC + Air Handler System")
    print("-" * 80)
    models = ["GLXS5BA1810", "AMST24BU13"]
    specs = extractor.get_multiple_specs(models)
    system_type = "AC_AirHandler"
    seer = 15.2

    title = generator.generate_title(system_type, specs, seer)
    print(f"Title: {title}")

    intro = generator.generate_intro(system_type, specs, seer)
    print(f"\nIntro: {intro[:200]}...")

    print("\nSpec Tables:")
    for model, spec in specs.items():
        if spec:
            print(f"\n  Component: {model}")
            rows = generator.generate_spec_table_rows(spec)
            for row in rows[:5]:  # Show first 5 rows
                print(f"    {row['label']}: {row['value']}")
            print(f"    ... ({len(rows)} total rows)")


if __name__ == "__main__":
    test_content_generator()
