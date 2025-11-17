"""
HTML Builder - Populates templates with generated content and builds final HTML
"""

from pathlib import Path
from typing import Dict, List
import re
from content_generator import ContentGenerator
from config import get_footer_type


class HTMLBuilder:
    """Build final HTML files from templates and generated content"""

    def __init__(self, content_generator: ContentGenerator):
        """
        Initialize with a ContentGenerator instance

        Args:
            content_generator: ContentGenerator instance
        """
        self.generator = content_generator

    def build_html(self,
                   template_path: Path,
                   system_type: str,
                   specs: Dict[str, Dict],
                   seer_rating: float,
                   model_numbers: List[str]) -> str:
        """
        Build complete HTML from template and specs

        Args:
            template_path: Path to HTML template file
            system_type: System type from SKU parser
            specs: Dictionary of component specs
            seer_rating: SEER2 rating
            model_numbers: List of model numbers in order

        Returns:
            Complete HTML string
        """
        # Load template
        try:
            template_html = template_path.read_text()
        except Exception as e:
            print(f"❌ Error reading template: {e}")
            return ""

        # Generate content
        title = self.generator.generate_title(system_type, specs, seer_rating)
        intro = self.generator.generate_intro(system_type, specs, seer_rating)

        # Replace title and intro placeholders
        html = template_html
        html = html.replace('[PRODUCT TITLE PLACEHOLDER]', title)
        html = html.replace('[INTRO PARAGRAPH PLACEHOLDER]', intro)

        # Build spec tables for each component
        html = self._populate_spec_tables(html, specs, model_numbers)

        # Handle footer logic
        html = self._handle_footer(html, seer_rating)

        return html

    def _populate_spec_tables(self, html: str, specs: Dict[str, Dict], model_numbers: List[str]) -> str:
        """
        Populate specification tables in HTML by matching labels and replacing [VALUE] placeholders

        Args:
            html: HTML template string
            specs: Dictionary of component specs
            model_numbers: List of model numbers in order

        Returns:
            HTML with populated spec tables
        """
        import re

        # For single component or first component, populate all [VALUE] placeholders
        for idx, model in enumerate(model_numbers):
            spec = specs.get(model)
            if not spec:
                print(f"⚠️  No spec found for {model}, skipping")
                continue

            # Generate rows with labels and values
            rows = self.generator.generate_spec_table_rows(spec)

            # Create a mapping of labels to values (case-insensitive, flexible matching)
            spec_map = {}
            label_aliases = {
                'model number': ['sku/model no', 'skumodel no', 'model', 'sku', 'skumodelno'],
                'refrigerant type': ['refrigerant', 'refrigeranttype'],
                'voltage/phase/frequency': ['voltage', 'electrical'],
                'min circuit ampacity': ['mincircuitampacity', 'mca'],
                'max overcurrent protection': ['maxovercurrentprotection', 'mop', 'max overcurrent device'],
                'dimensions (w×d×h)': ['dimensions (h×w×d)', 'dimensions', 'dimensionshwd', 'dimensionswdh'],
                'shipping weight': ['weight', 'shippingweight'],
            }

            for row in rows:
                label = row['label'].lower().strip()
                value = row['value']

                # Store exact label
                spec_map[label] = value

                # Store clean label (no special chars)
                clean_label = re.sub(r'[^a-z0-9]', '', label)
                spec_map[clean_label] = value

                # Store aliases
                for main_label, aliases in label_aliases.items():
                    if label in aliases or clean_label in [re.sub(r'[^a-z0-9]', '', a) for a in aliases]:
                        spec_map[main_label] = value
                        spec_map[re.sub(r'[^a-z0-9]', '', main_label)] = value

            # Find all table rows with [VALUE] and replace them
            # Pattern: <td><strong>Label</strong></td>\s*<td>\[VALUE\]</td>
            def replace_value(match):
                label_text = match.group(1).lower().strip()
                clean_label = re.sub(r'[^a-z0-9]', '', label_text)

                # Try exact match first
                value = spec_map.get(label_text)
                if value:
                    return f'<td><strong>{match.group(1)}</strong></td>\n                    <td>{value}</td>'

                # Try clean match
                value = spec_map.get(clean_label)
                if value:
                    return f'<td><strong>{match.group(1)}</strong></td>\n                    <td>{value}</td>'

                # Return original if no match
                return match.group(0)

            # Replace all [VALUE] placeholders in table rows
            html = re.sub(
                r'<td><strong>([^<]+)</strong></td>\s*<td>\[VALUE\]</td>',
                replace_value,
                html,
                flags=re.IGNORECASE
            )

            # Continue to next component (multi-component systems have multiple spec tables)

        return html

    def _handle_footer(self, html: str, seer_rating: float) -> str:
        """
        Handle footer selection based on SEER rating

        Args:
            html: HTML string
            seer_rating: SEER2 rating

        Returns:
            HTML with correct footer
        """
        footer_type = get_footer_type(seer_rating)

        # Footers are marked in templates with comments or specific text
        # Footer Type A: Northern Regions Only (SEER < 14.3)
        # Footer Type B: Nationally Approved (SEER >= 14.3)

        if footer_type == 'A':
            # Keep Footer A, remove Footer B
            # Look for footer sections and remove the B section
            # This depends on how footers are marked in templates

            # Pattern to find and remove Footer Type B
            # Assuming footers have identifiable titles
            html = self._remove_footer_section(html, 'DOE Compliant Nationwide', 'DOE Compliant for Northern Regions')

        else:  # footer_type == 'B'
            # Keep Footer B, remove Footer A
            html = self._remove_footer_section(html, 'DOE Compliant for Northern Regions', 'DOE Compliant Nationwide')

        return html

    def _remove_footer_section(self, html: str, remove_pattern: str, keep_pattern: str) -> str:
        """
        Remove one footer section while keeping the other

        Args:
            html: HTML string
            remove_pattern: Pattern to identify footer to remove
            keep_pattern: Pattern to identify footer to keep

        Returns:
            HTML with one footer removed
        """
        # This is a simplified approach
        # In practice, the footers might be wrapped in comments or specific divs

        # For now, just return as-is
        # This would need to be customized based on actual template structure
        return html

    def generate_filename(self, system_type: str, specs: Dict[str, Dict], model_numbers: List[str]) -> str:
        """
        Generate standardized filename for HTML output

        Args:
            system_type: System type from SKU parser
            specs: Dictionary of component specs
            model_numbers: List of model numbers

        Returns:
            Filename string (e.g., "Goodman_1.5Ton_R410A_AC_System_GLXS5BA1810_AMST24BU13.html")
        """
        tonnage = self.generator.extractor.extract_system_tonnage(specs)

        if len(model_numbers) == 1:
            # Single component
            return f"Goodman_R410A_AC_{model_numbers[0]}.html"

        elif len(model_numbers) == 2:
            # 2-component system
            if 'AC' in system_type:
                prefix = 'AC_System'
            elif 'HP' in system_type:
                prefix = 'HP_System'
            else:
                prefix = 'System'

            return f"Goodman_{tonnage}Ton_R410A_{prefix}_{'_'.join(model_numbers)}.html"

        else:
            # 3-component system
            if 'DualFuel' in system_type:
                if '80AFUE' in system_type:
                    afue = '80AFUE'
                else:
                    afue = '92AFUE'

                if 'Upflow' in system_type:
                    orientation = 'Upflow'
                else:
                    orientation = 'Horizontal'

                return f"Goodman_R410A_DualFuel_{afue}_{orientation}_System_{'_'.join(model_numbers)}.html"

            elif 'AC' in system_type:
                if '80AFUE' in system_type:
                    afue = '80AFUE'
                else:
                    afue = '92AFUE'

                if 'Upflow' in system_type:
                    orientation = 'Upflow'
                else:
                    orientation = 'Horizontal'

                return f"Goodman_R410A_AC_{afue}_{orientation}_System_{'_'.join(model_numbers)}.html"

        return f"Goodman_System_{'_'.join(model_numbers)}.html"

    def save_html(self, html: str, output_path: Path) -> bool:
        """
        Save HTML to file

        Args:
            html: HTML string
            output_path: Path where to save the file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            output_path.write_text(html)
            print(f"✅ Saved: {output_path.name}")
            return True

        except Exception as e:
            print(f"❌ Error saving {output_path.name}: {e}")
            return False


def test_html_builder():
    """Test the HTML builder"""
    from pathlib import Path
    from spec_extractor import SpecExtractor
    from content_generator import ContentGenerator
    from template_selector import TemplateSelector

    print("HTML Builder Test")
    print("=" * 80)

    # Setup
    specs_file = Path(__file__).parent.parent / "15.2_SEER2" / "Specs" / "15.2_specs.json"
    extractor = SpecExtractor(str(specs_file))
    generator = ContentGenerator(extractor)
    builder = HTMLBuilder(generator)
    selector = TemplateSelector()

    # Test with AC + Air Handler system
    print("\n1. Testing HTML Generation for AC + Air Handler System")
    print("-" * 80)

    models = ["GLXS5BA1810", "AMST24BU13"]
    component_types = ['AC_Condenser', 'AirHandler_Standard']
    system_type = "AC_AirHandler"
    seer = 15.2

    # Get specs
    specs = extractor.get_multiple_specs(models)

    # Select template
    template_result = selector.select_template(component_types)
    if not template_result:
        print("❌ No template found")
        return

    template_name, template_path = template_result
    print(f"Template: {template_name}")

    # Generate filename
    filename = builder.generate_filename(system_type, specs, models)
    print(f"Filename: {filename}")

    # Build HTML
    html = builder.build_html(template_path, system_type, specs, seer, models)

    if html:
        print(f"✅ HTML generated successfully ({len(html):,} characters)")

        # Show a preview
        preview = html[:500]
        print(f"\nPreview:\n{preview}...")

        # Test saving
        print("\n2. Testing HTML Save")
        print("-" * 80)
        output_dir = Path(__file__).parent.parent / "pipeline" / "test_output"
        output_path = output_dir / filename

        success = builder.save_html(html, output_path)
        if success:
            print(f"✅ Test file saved to: {output_path}")
    else:
        print("❌ Failed to generate HTML")


if __name__ == "__main__":
    test_html_builder()
