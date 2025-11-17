"""
SKU Parser - Parses SKU strings and detects component/system types
"""

import re
from typing import List, Dict, Tuple
from config import COMPONENT_PATTERNS


class SKUParser:
    """Parse and analyze SKU strings to determine component types and system configuration"""

    def __init__(self):
        self.component_patterns = COMPONENT_PATTERNS

    def parse_sku_line(self, sku_line: str) -> Dict:
        """
        Parse a single SKU line from SKUS file

        Args:
            sku_line: String like "GLXS5BA1810, AMST24BU13" or "GLXS5BA1810"

        Returns:
            Dict with:
                - raw_skus: List of SKU strings
                - component_count: Number of components
                - component_types: List of component type identifiers
                - system_type: String describing the system type
                - is_valid: Boolean indicating if SKUs could be parsed
        """
        # Clean and split the line
        sku_line = sku_line.strip()

        # Skip empty lines, comments, or section headers
        if not sku_line or sku_line.startswith('#') or sku_line.startswith('Part #'):
            return {
                'raw_skus': [],
                'component_count': 0,
                'component_types': [],
                'system_type': None,
                'is_valid': False,
                'error': 'Empty, comment, or header line'
            }

        # Split by comma
        skus = [s.strip() for s in sku_line.split(',') if s.strip()]

        if not skus:
            return {
                'raw_skus': [],
                'component_count': 0,
                'component_types': [],
                'system_type': None,
                'is_valid': False,
                'error': 'No SKUs found'
            }

        # Identify each component type and filter out thermostats
        component_types = []
        filtered_skus = []
        for sku in skus:
            comp_type = self.identify_component(sku)
            # Skip thermostats
            if comp_type == 'Thermostat':
                continue
            if comp_type:
                component_types.append(comp_type)
                filtered_skus.append(sku)
            else:
                # Unknown component
                component_types.append('Unknown')
                filtered_skus.append(sku)

        # Use filtered SKUs without thermostats
        skus = filtered_skus

        # Determine overall system type
        system_type = self.determine_system_type(component_types)

        return {
            'raw_skus': skus,
            'component_count': len(skus),
            'component_types': component_types,
            'system_type': system_type,
            'is_valid': True,
            'error': None
        }

    def identify_component(self, sku: str) -> str:
        """
        Identify component type from SKU prefix

        Args:
            sku: SKU string like "GLXS5BA1810"

        Returns:
            Component type identifier or None
        """
        sku = sku.strip().upper()

        # Check against known patterns
        for pattern, comp_type in self.component_patterns.items():
            if sku.startswith(pattern):
                return comp_type

        return None

    def determine_system_type(self, component_types: List[str]) -> str:
        """
        Determine overall system type from component types

        Args:
            component_types: List of component type identifiers

        Returns:
            System type string
        """
        if not component_types:
            return 'Unknown'

        # Single component
        if len(component_types) == 1:
            return f"Single_{component_types[0]}"

        # 2-component systems
        if len(component_types) == 2:
            comp1, comp2 = component_types

            # AC + Air Handler
            if comp1 == 'AC_Condenser' and 'AirHandler' in comp2:
                if comp2 == 'AirHandler_Wall':
                    return 'AC_AirHandler_Wall'
                return 'AC_AirHandler'

            # HP + Air Handler
            if comp1 == 'HP_Condenser' and 'AirHandler' in comp2:
                if comp2 == 'AirHandler_Wall':
                    return 'HP_AirHandler_Wall'
                return 'HP_AirHandler'

            # AC/HP + Coil
            if comp1 in ['AC_Condenser', 'HP_Condenser'] and 'Coil' in comp2:
                prefix = 'AC' if comp1 == 'AC_Condenser' else 'HP'
                orientation = 'Upflow' if comp2 == 'Coil_Upflow' else 'Horizontal'
                return f'{prefix}_Coil_{orientation}'

            # Furnace + Coil
            if 'Furnace' in comp1 and 'Coil' in comp2:
                afue = comp1.replace('Furnace_', '')
                orientation = 'Upflow' if comp2 == 'Coil_Upflow' else 'Horizontal'
                return f'Furnace_Coil_{afue}_{orientation}'

            return f'System_2Component_{comp1}_{comp2}'

        # 3-component systems
        if len(component_types) == 3:
            comp1, comp2, comp3 = component_types

            # AC + Furnace + Coil
            if comp1 == 'AC_Condenser' and 'Furnace' in comp2 and 'Coil' in comp3:
                afue = comp2.replace('Furnace_', '')
                orientation = 'Upflow' if comp3 == 'Coil_Upflow' else 'Horizontal'
                return f'AC_Furnace_Coil_{afue}_{orientation}'

            # HP + Furnace + Coil (Dual Fuel)
            if comp1 == 'HP_Condenser' and 'Furnace' in comp2 and 'Coil' in comp3:
                afue = comp2.replace('Furnace_', '')
                orientation = 'Upflow' if comp3 == 'Coil_Upflow' else 'Horizontal'
                return f'HP_Furnace_Coil_{afue}_{orientation}_DualFuel'

            return f'System_3Component_{comp1}_{comp2}_{comp3}'

        return 'Unknown_MultiComponent'

    def parse_skus_file(self, file_path: str) -> List[Dict]:
        """
        Parse entire SKUS file

        Args:
            file_path: Path to SKUS file

        Returns:
            List of parsed SKU dictionaries
        """
        results = []

        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    parsed = self.parse_sku_line(line)
                    if parsed['is_valid']:
                        parsed['line_number'] = line_num
                        parsed['original_line'] = line.strip()
                        results.append(parsed)
        except FileNotFoundError:
            print(f"❌ SKUS file not found: {file_path}")
            return []
        except Exception as e:
            print(f"❌ Error reading SKUS file: {e}")
            return []

        return results

    def get_component_details(self, parsed_sku: Dict) -> str:
        """Get human-readable description of the system"""
        if not parsed_sku['is_valid']:
            return "Invalid SKU"

        count = parsed_sku['component_count']
        types = parsed_sku['component_types']

        if count == 1:
            return f"Single Component: {types[0]}"
        elif count == 2:
            return f"2-Component System: {types[0]} + {types[1]}"
        elif count == 3:
            return f"3-Component System: {types[0]} + {types[1]} + {types[2]}"
        else:
            return f"{count}-Component System"


def test_parser():
    """Test the SKU parser with sample data"""
    parser = SKUParser()

    test_cases = [
        "GLXS5BA1810",  # Single AC condenser
        "GLZS5BA2410",  # Single HP condenser
        "GLXS5BA1810, AMST24BU13",  # AC + Air Handler
        "GLXS5BA1810, AWST18SU1305",  # AC + Wall Air Handler
        "GLZS5BA1810, AMST24BU13",  # HP + Air Handler
        "GLXS5BA1810, GR9S800403ANA, CAPTA2422A3",  # AC + 80% Furnace + Upflow Coil
        "GLXS5BA1810, GR9S920403ANA, CHPTA2426B3",  # AC + 92% Furnace + Horizontal Coil
        "GLZS5BA1810, GR9S800403ANA, CAPTA2422A3",  # HP + 80% Furnace + Upflow Coil (Dual Fuel)
        "# Comment line",  # Comment
        "",  # Empty line
    ]

    print("SKU Parser Test")
    print("=" * 80)

    for test in test_cases:
        result = parser.parse_sku_line(test)
        if result['is_valid']:
            print(f"\n✅ Input: {test}")
            print(f"   SKUs: {result['raw_skus']}")
            print(f"   Components: {result['component_count']}")
            print(f"   Types: {result['component_types']}")
            print(f"   System: {result['system_type']}")
            print(f"   Description: {parser.get_component_details(result)}")
        else:
            print(f"\n⏭️  Skipped: {test[:50]}")
            if result['error']:
                print(f"   Reason: {result['error']}")


if __name__ == "__main__":
    test_parser()
