"""
Spec Extractor - Loads and extracts specifications from JSON files
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class SpecExtractor:
    """Extract and format specifications from JSON spec files"""

    def __init__(self, specs_file_path: str):
        """
        Initialize with path to specs JSON file

        Args:
            specs_file_path: Path to {SEER}_specs.json file
        """
        self.specs_file_path = Path(specs_file_path)
        self.specs_data = {}
        self.load_specs()

    def load_specs(self):
        """Load specs from JSON file"""
        try:
            with open(self.specs_file_path, 'r') as f:
                self.specs_data = json.load(f)
            print(f"✅ Loaded {len(self.specs_data)} specifications from {self.specs_file_path.name}")
        except FileNotFoundError:
            print(f"❌ Specs file not found: {self.specs_file_path}")
            self.specs_data = {}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
            self.specs_data = {}

    def get_spec(self, model_number: str) -> Optional[Dict]:
        """
        Get specifications for a specific model number
        Handles flexible matching with/without 'A' suffix

        Args:
            model_number: Model number like "GLXS5BA1810"

        Returns:
            Dictionary of specifications or None if not found
        """
        # Try exact match first
        spec = self.specs_data.get(model_number)
        if spec:
            return spec

        # Map GSZV7SA to GZV7SA specs (17.5 SEER2)
        if model_number.startswith('GSZV7SA'):
            replacement = model_number.replace('GSZV7SA', 'GZV7SA')
            spec = self.specs_data.get(replacement)
            if spec:
                # Return a copy with the original model number
                spec_copy = spec.copy()
                spec_copy['model_number'] = model_number
                return spec_copy

        # Try with 'A' suffix if not found
        if not model_number.endswith('A'):
            spec = self.specs_data.get(model_number + 'A')
            if spec:
                return spec

        # Try without 'A' suffix if not found
        if model_number.endswith('A'):
            spec = self.specs_data.get(model_number[:-1])
            if spec:
                return spec

        # Try other common variations for furnaces
        # GR9S920403ANA -> GR9S920403AN (extra 'A' at end)
        if model_number.endswith('ANA'):
            spec = self.specs_data.get(model_number[:-1])
            if spec:
                return spec
        if model_number.endswith('BNA'):
            spec = self.specs_data.get(model_number[:-1])
            if spec:
                return spec
        if model_number.endswith('CNA'):
            spec = self.specs_data.get(model_number[:-1])
            if spec:
                return spec

        # Handle common typos
        # AMST36CU13 -> AMST36BU13
        if 'AMST36CU13' in model_number:
            spec = self.specs_data.get(model_number.replace('CU13', 'BU13'))
            if spec:
                return spec

        # CHPTA3626B3 -> CHPTA3630B3
        if 'CHPTA3626B3' in model_number:
            spec = self.specs_data.get(model_number.replace('3626', '3630'))
            if spec:
                return spec

        # CAPT6030C3 -> CAPTA6030C3 (missing A after CAPT)
        if model_number.startswith('CAPT') and not model_number.startswith('CAPTA'):
            spec = self.specs_data.get(model_number.replace('CAPT', 'CAPTA', 1))
            if spec:
                return spec

        return None

    def enrich_coil_spec(self, spec: Dict) -> Dict:
        """
        Enrich coil spec with derived/default fields for compatibility

        Args:
            spec: Coil specification dictionary

        Returns:
            Enriched specification dictionary
        """
        if not spec or 'equipment_type' not in spec:
            return spec

        # Derive orientation from equipment_type
        if 'orientation' not in spec:
            equipment_type = spec.get('equipment_type', '').lower()
            if 'upflow' in equipment_type:
                spec['orientation'] = 'Upflow'
            elif 'horizontal' in equipment_type:
                spec['orientation'] = 'Horizontal'
            else:
                spec['orientation'] = 'Multi-Position'

        # Add default metering device if missing
        if 'metering_device' not in spec:
            spec['metering_device'] = 'TXV'

        # Add default line sizes if missing (typical values, will be overridden if actual values exist)
        if 'liquid_line_od_in' not in spec:
            spec['liquid_line_od_in'] = 0.375  # 3/8" is common

        if 'suction_line_od_in' not in spec:
            # Estimate based on tonnage if available
            tonnage = spec.get('tonnage', 2.0)
            if tonnage <= 2.0:
                spec['suction_line_od_in'] = 0.75
            elif tonnage <= 3.5:
                spec['suction_line_od_in'] = 0.875
            else:
                spec['suction_line_od_in'] = 1.125

        # Add default shipping weight if missing
        if 'shipping_weight_lb' not in spec:
            # Estimate based on tonnage
            tonnage = spec.get('tonnage', 2.0)
            spec['shipping_weight_lb'] = int(20 + (tonnage * 10))  # Rough estimate

        return spec

    def enrich_furnace_spec(self, spec: Dict) -> Dict:
        """
        Enrich furnace spec with derived/default fields for compatibility

        Args:
            spec: Furnace specification dictionary

        Returns:
            Enriched specification dictionary
        """
        if not spec:
            return spec

        # Map 'stages' to 'heating_stages' if needed
        if 'heating_stages' not in spec and 'stages' in spec:
            stages = spec['stages']
            if stages == 1:
                spec['heating_stages'] = 'Single Stage'
            elif stages == 2:
                spec['heating_stages'] = 'Two Stage'
            else:
                spec['heating_stages'] = f'{stages} Stage'

        # Extract AFUE from equipment_type if not present
        if 'afue_percent' not in spec:
            equipment_type = spec.get('equipment_type', '')
            if '96%' in equipment_type or '96' in equipment_type:
                spec['afue_percent'] = 96
            elif '92%' in equipment_type or '92' in equipment_type:
                spec['afue_percent'] = 92
            elif '80%' in equipment_type or '80' in equipment_type:
                spec['afue_percent'] = 80
            else:
                spec['afue_percent'] = 80  # Default

        # Derive blower_motor_type if missing
        if 'blower_motor_type' not in spec:
            # Check if it's variable speed or ECM based on equipment type or default
            equipment_type = spec.get('equipment_type', '').lower()
            if 'variable' in equipment_type or 'ecm' in equipment_type:
                spec['blower_motor_type'] = 'Variable Speed ECM'
            else:
                # Default to multi-speed for modern furnaces
                spec['blower_motor_type'] = 'Multi-Speed ECM'

        return spec

    def get_multiple_specs(self, model_numbers: List[str]) -> Dict[str, Dict]:
        """
        Get specifications for multiple model numbers

        Args:
            model_numbers: List of model numbers

        Returns:
            Dictionary mapping model_number to specs
        """
        result = {}
        missing = []

        for model in model_numbers:
            spec = self.get_spec(model)
            if spec:
                result[model] = spec
            else:
                missing.append(model)

        if missing:
            print(f"⚠️  Missing specs for: {', '.join(missing)}")

        return result

    def format_value(self, value, key: str = "") -> str:
        """
        Format a spec value for display in HTML

        Args:
            value: The value to format
            key: The spec key (for context-aware formatting)

        Returns:
            Formatted string
        """
        if value is None or value == "":
            return "N/A"

        # Handle numeric values
        if isinstance(value, (int, float)):
            # Special formatting for specific fields
            if 'tonnage' in key.lower():
                return f"{value} Ton"
            elif 'btuh' in key.lower() or 'capacity' in key.lower():
                return f"{int(value):,} BTU/h"
            elif 'seer' in key.lower() or 'eer' in key.lower() or 'hspf' in key.lower() or 'afue' in key.lower():
                return f"{value}"
            elif 'voltage' in key.lower():
                return f"{value}V"
            elif 'weight' in key.lower():
                return f"{value} lbs"
            elif 'height' in key.lower() or 'width' in key.lower() or 'depth' in key.lower():
                return f"{value}\""
            elif 'line' in key.lower() and 'in' in key.lower():
                # Convert decimal to fraction for line sizes
                if value == 0.375:
                    return "⅜\""
                elif value == 0.75:
                    return "¾\""
                elif value == 0.5:
                    return "½\""
                elif value == 0.625:
                    return "⅝\""
                else:
                    return f"{value}\""
            elif 'oz' in key.lower():
                return f"{int(value)} oz"
            else:
                return str(value)

        # Return string values as-is
        return str(value)

    def extract_system_tonnage(self, specs: Dict[str, Dict]) -> float:
        """
        Extract tonnage from system specs (uses first condenser found)

        Args:
            specs: Dictionary of component specs

        Returns:
            Tonnage as float
        """
        for model, spec in specs.items():
            if spec and 'tonnage' in spec:
                return spec['tonnage']

        return 0.0

    def extract_seer_rating(self, specs: Dict[str, Dict]) -> float:
        """
        Extract SEER2 rating from system specs (uses first condenser found)

        Args:
            specs: Dictionary of component specs

        Returns:
            SEER2 rating as float
        """
        for model, spec in specs.items():
            if spec and 'seer2' in spec and spec['seer2']:
                return spec['seer2']

        return 0.0

    def validate_specs(self, model_numbers: List[str]) -> tuple[bool, List[str]]:
        """
        Validate that all required model numbers have specs

        Args:
            model_numbers: List of model numbers to validate

        Returns:
            Tuple of (all_found: bool, missing: List[str])
        """
        missing = []
        for model in model_numbers:
            if not self.get_spec(model):
                missing.append(model)

        return (len(missing) == 0, missing)


def test_extractor():
    """Test the spec extractor"""
    import sys

    # Try to find a specs file
    test_file = Path(__file__).parent.parent / "15.2_SEER2" / "Specs" / "15.2_specs.json"

    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        print("Please ensure 15.2_specs.json exists in 15.2_SEER2/Specs/")
        sys.exit(1)

    print("Spec Extractor Test")
    print("=" * 80)

    extractor = SpecExtractor(str(test_file))

    # Test single spec extraction
    print("\n1. Testing single spec extraction:")
    print("-" * 80)
    model = "GLXS5BA1810"
    spec = extractor.get_spec(model)
    if spec:
        print(f"✅ Found specs for {model}:")
        print(f"   Brand: {spec.get('brand')}")
        print(f"   Type: {spec.get('equipment_type')}")
        print(f"   Tonnage: {extractor.format_value(spec.get('tonnage'), 'tonnage')}")
        print(f"   SEER2: {spec.get('seer2')}")
        print(f"   Cooling: {extractor.format_value(spec.get('cooling_capacity_btuh'), 'cooling_capacity_btuh')}")
    else:
        print(f"❌ No specs found for {model}")

    # Test multiple spec extraction
    print("\n2. Testing multiple spec extraction:")
    print("-" * 80)
    models = ["GLXS5BA1810", "AMST24BU13"]
    specs = extractor.get_multiple_specs(models)
    print(f"✅ Retrieved specs for {len(specs)}/{len(models)} models")
    for model, spec in specs.items():
        print(f"   - {model}: {spec.get('equipment_type')}")

    # Test validation
    print("\n3. Testing validation:")
    print("-" * 80)
    test_models = ["GLXS5BA1810", "AMST24BU13", "NONEXISTENT123"]
    all_found, missing = extractor.validate_specs(test_models)
    if all_found:
        print("✅ All specs found")
    else:
        print(f"⚠️  Missing specs: {missing}")

    # Test tonnage extraction
    print("\n4. Testing tonnage extraction:")
    print("-" * 80)
    tonnage = extractor.extract_system_tonnage(specs)
    print(f"✅ System tonnage: {tonnage} tons")

    # Test SEER extraction
    print("\n5. Testing SEER extraction:")
    print("-" * 80)
    seer = extractor.extract_seer_rating(specs)
    print(f"✅ System SEER2: {seer}")


if __name__ == "__main__":
    test_extractor()
