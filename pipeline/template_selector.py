"""
Template Selector - Selects appropriate HTML template based on system configuration
"""

from pathlib import Path
from typing import Optional, Tuple
from config import (
    SINGLE_COMPONENT_TEMPLATES,
    MULTI_COMPONENT_TEMPLATES,
    TEMPLATES_DIR
)


class TemplateSelector:
    """Select the appropriate template for a given system configuration"""

    def __init__(self):
        self.single_templates = SINGLE_COMPONENT_TEMPLATES
        self.multi_templates = MULTI_COMPONENT_TEMPLATES
        self.templates_dir = Path(TEMPLATES_DIR)

    def select_template(self, component_types: list) -> Optional[Tuple[str, Path]]:
        """
        Select template based on component types

        Args:
            component_types: List of component type identifiers from SKU parser

        Returns:
            Tuple of (template_name, template_path) or None if no match
        """
        if not component_types:
            return None

        # Single component
        if len(component_types) == 1:
            return self._select_single_component_template(component_types[0])

        # Multi-component system
        return self._select_multi_component_template(tuple(component_types))

    def _select_single_component_template(self, component_type: str) -> Optional[Tuple[str, Path]]:
        """
        Select template for single component

        Args:
            component_type: Component type identifier

        Returns:
            Tuple of (template_name, template_path) or None
        """
        template_name = self.single_templates.get(component_type)

        if not template_name:
            print(f"⚠️  No template mapping for component type: {component_type}")
            return None

        template_path = self.templates_dir / template_name

        if not template_path.exists():
            print(f"❌ Template file not found: {template_path}")
            return None

        return (template_name, template_path)

    def _select_multi_component_template(self, component_types: tuple) -> Optional[Tuple[str, Path]]:
        """
        Select template for multi-component system

        Args:
            component_types: Tuple of component type identifiers

        Returns:
            Tuple of (template_name, template_path) or None
        """
        template_name = self.multi_templates.get(component_types)

        if not template_name:
            # Try alternate matching strategies
            print(f"⚠️  No exact template mapping for components: {component_types}")

            # Try fuzzy matching for similar systems
            template_name = self._fuzzy_match_template(component_types)

            if not template_name:
                print(f"❌ Could not find suitable template for: {component_types}")
                return None

        template_path = self.templates_dir / template_name

        if not template_path.exists():
            print(f"❌ Template file not found: {template_path}")
            return None

        return (template_name, template_path)

    def _fuzzy_match_template(self, component_types: tuple) -> Optional[str]:
        """
        Attempt fuzzy matching when exact match not found

        Args:
            component_types: Tuple of component types

        Returns:
            Template name or None
        """
        # For 2-component systems, try to match by category
        if len(component_types) == 2:
            comp1, comp2 = component_types

            # AC or HP + any Air Handler -> use air handler template
            if comp1 in ['AC_Condenser', 'HP_Condenser'] and 'AirHandler' in comp2:
                if comp1 == 'AC_Condenser':
                    return 'template_system_ac_airhandler_CORRECTED.html'
                else:
                    return 'template_system_hp_airhandler_CORRECTED.html'

            # AC or HP + any Coil -> use coil template
            if comp1 in ['AC_Condenser', 'HP_Condenser'] and 'Coil' in comp2:
                if comp1 == 'AC_Condenser':
                    return 'template_system_ac_coil_CORRECTED.html'
                else:
                    return 'template_system_hp_coil_CORRECTED.html'

            # Furnace + any Coil -> use furnace coil template
            if 'Furnace' in comp1 and 'Coil' in comp2:
                return 'template_system_furnace_coil_CORRECTED.html'

        # For 3-component systems
        elif len(component_types) == 3:
            comp1, comp2, comp3 = component_types

            # AC + Furnace + Coil
            if comp1 == 'AC_Condenser' and 'Furnace' in comp2 and 'Coil' in comp3:
                return 'template_system_ac_furnace_coil_CORRECTED.html'

            # HP + Furnace + Coil (Dual Fuel)
            if comp1 == 'HP_Condenser' and 'Furnace' in comp2 and 'Coil' in comp3:
                return 'template_system_hp_furnace_coil_dualfuel_CORRECTED.html'

        return None

    def get_template_info(self, template_path: Path) -> dict:
        """
        Get information about a template

        Args:
            template_path: Path to template file

        Returns:
            Dictionary with template info
        """
        if not template_path.exists():
            return {'exists': False}

        # Count placeholders in template
        try:
            content = template_path.read_text()
            placeholder_count = content.count('[')

            return {
                'exists': True,
                'size': template_path.stat().st_size,
                'placeholder_count': placeholder_count,
                'name': template_path.name
            }
        except Exception as e:
            return {
                'exists': True,
                'error': str(e)
            }

    def list_available_templates(self) -> dict:
        """
        List all available templates

        Returns:
            Dictionary categorizing templates
        """
        result = {
            'single_component': [],
            'multi_component': [],
            'total': 0
        }

        # Check single component templates
        for comp_type, template_name in self.single_templates.items():
            template_path = self.templates_dir / template_name
            if template_path.exists():
                result['single_component'].append({
                    'component_type': comp_type,
                    'template': template_name,
                    'exists': True
                })

        # Check multi-component templates
        for comp_types, template_name in self.multi_templates.items():
            template_path = self.templates_dir / template_name
            if template_path.exists():
                result['multi_component'].append({
                    'component_types': comp_types,
                    'template': template_name,
                    'exists': True
                })

        result['total'] = len(result['single_component']) + len(result['multi_component'])
        return result


def test_selector():
    """Test the template selector"""
    print("Template Selector Test")
    print("=" * 80)

    selector = TemplateSelector()

    # Test cases
    test_cases = [
        # Single components
        (['AC_Condenser'], "Single AC Condenser"),
        (['HP_Condenser'], "Single HP Condenser"),
        (['AirHandler_Standard'], "Standard Air Handler"),

        # 2-component systems
        (['AC_Condenser', 'AirHandler_Standard'], "AC + Air Handler"),
        (['AC_Condenser', 'AirHandler_Wall'], "AC + Wall Air Handler"),
        (['HP_Condenser', 'AirHandler_Standard'], "HP + Air Handler"),
        (['AC_Condenser', 'Coil_Upflow'], "AC + Upflow Coil"),

        # 3-component systems
        (['AC_Condenser', 'Furnace_80AFUE', 'Coil_Upflow'], "AC + 80% Furnace + Upflow Coil"),
        (['AC_Condenser', 'Furnace_92AFUE', 'Coil_Horizontal'], "AC + 92% Furnace + Horizontal Coil"),
        (['HP_Condenser', 'Furnace_80AFUE', 'Coil_Upflow'], "HP + 80% Furnace + Upflow Coil (Dual Fuel)"),
    ]

    for component_types, description in test_cases:
        print(f"\n📋 {description}")
        print(f"   Components: {component_types}")

        result = selector.select_template(component_types)

        if result:
            template_name, template_path = result
            print(f"   ✅ Template: {template_name}")
            print(f"   📁 Path: {template_path}")

            info = selector.get_template_info(template_path)
            if info.get('exists'):
                print(f"   📊 Size: {info.get('size', 0):,} bytes")
                print(f"   🔖 Placeholders: {info.get('placeholder_count', 0)}")
        else:
            print(f"   ❌ No template found")

    # List all available templates
    print("\n" + "=" * 80)
    print("Available Templates Summary")
    print("=" * 80)

    available = selector.list_available_templates()
    print(f"\n📄 Single Component Templates: {len(available['single_component'])}")
    for item in available['single_component'][:5]:  # Show first 5
        print(f"   - {item['component_type']}: {item['template']}")

    print(f"\n📄 Multi-Component Templates: {len(available['multi_component'])}")
    for item in available['multi_component'][:5]:  # Show first 5
        print(f"   - {', '.join(item['component_types'])}: {item['template']}")

    print(f"\n✅ Total Templates Available: {available['total']}")


if __name__ == "__main__":
    test_selector()
