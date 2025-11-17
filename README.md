# HVAC Description Generator - Universal Pipeline

Complete, automated pipeline for generating HTML product descriptions for HVAC equipment systems.

## Overview

This tool generates professional HTML product descriptions for HVAC systems by:
1. Reading SKU lists from text files
2. Extracting technical specifications from JSON files
3. Selecting appropriate HTML templates based on system configuration
4. Generating dynamic content (titles, introductions, spec tables)
5. Building and saving complete HTML files

## Directory Structure

```
New Plan/
├── pipeline/                    # Core pipeline modules
│   ├── config.py               # Configuration and mappings
│   ├── sku_parser.py           # SKU parsing and system type detection
│   ├── spec_extractor.py       # Spec data extraction from JSON
│   ├── template_selector.py    # Template selection logic
│   ├── content_generator.py    # Dynamic content generation
│   ├── html_builder.py         # HTML assembly
│   └── main_generator.py       # Main orchestration script
│
├── Scripts/                     # HTML templates (18 templates)
│   ├── template_ac_condenser_only_CORRECTED.html
│   ├── template_system_ac_airhandler_CORRECTED.html
│   ├── template_system_hp_furnace_coil_dualfuel_CORRECTED.html
│   └── ... (15 more templates)
│
├── 13.4_SEER2/                 # SEER 13.4 equipment data
│   ├── SKUS/SKUS              # SKU list file
│   ├── Specs/*.json           # Specifications JSON
│   └── Generated_Descriptions/ # Output folder
│
├── 14.3_SEER2/                 # SEER 14.3 equipment data
├── 15.2_SEER2/                 # SEER 15.2 equipment data
├── 16.2 SEER2/                 # SEER 16.2 equipment data
├── 17.2_SEER2/                 # SEER 17.2 equipment data
├── 17.5_SEER2/                 # SEER 17.5 equipment data
└── README.md                    # This file
```

## Quick Start

### 1. Validate Configuration

```bash
cd pipeline
python3 main_generator.py --test-config
```

### 2. Validate SKUs and Specs

```bash
python3 main_generator.py --seer 15.2 --validate-only
```

### 3. Generate Descriptions (Dry Run)

```bash
python3 main_generator.py --seer 15.2 --dry-run
```

### 4. Generate All Descriptions

```bash
python3 main_generator.py --seer 15.2
```

## Usage

### Command Line Options

```
python3 main_generator.py [OPTIONS]

Options:
  --seer RATING          SEER rating to process (e.g., 15.2, 14.3)
  --dry-run             Preview without writing files
  --validate-only       Only validate SKUs and specs
  --test-config         Test pipeline configuration
```

### Examples

```bash
# Generate all descriptions for SEER 15.2
python3 main_generator.py --seer 15.2

# Preview what would be generated without writing files
python3 main_generator.py --seer 15.2 --dry-run

# Check if all SKUs have corresponding specs
python3 main_generator.py --seer 15.2 --validate-only

# Process different SEER ratings
python3 main_generator.py --seer 14.3
python3 main_generator.py --seer 17.2
```

## File Formats

### SKUs File

Location: `{SEER}_SEER2/SKUS/SKUS`

Format:
```
# Comments start with #
Part # Section headers are automatically skipped

# Single component
GLXS5BA1810

# 2-component system
GLXS5BA1810, AMST24BU13

# 3-component system
GLXS5BA1810, GR9S800403ANA, CAPTA2422A3
```

### Specs JSON File

Location: `{SEER}_SEER2/Specs/{SEER}_specs.json`

Format:
```json
{
  "GLXS5BA1810": {
    "model_number": "GLXS5BA1810",
    "brand": "Goodman",
    "equipment_type": "Air Conditioner Condenser",
    "tonnage": 1.5,
    "cooling_capacity_btuh": 18000,
    "seer2": 15.2,
    "refrigerant_type": "R-410A",
    ...
  }
}
```

## System Types Supported

### Single Component Systems (10 types)
- AC Condensers
- Heat Pump Condensers
- Air Handlers (Standard & Wall-Mounted)
- Evaporator Coils (Upflow & Horizontal)
- Gas Furnaces (80%, 92%, 96% AFUE)
- Packaged Units (Gas/Electric & Heat Pump)

### Multi-Component Systems (8 types)
- AC + Air Handler
- HP + Air Handler
- AC + Coil
- HP + Coil
- Furnace + Coil
- AC + Furnace + Coil
- HP + Furnace + Coil (Dual Fuel)

## Template Selection Logic

The pipeline automatically selects the correct template based on:
1. Number of components (1, 2, or 3)
2. Component types (AC, HP, Air Handler, Furnace, Coil)
3. Equipment configuration (Upflow vs. Horizontal, Wall vs. Standard)

## Footer Logic

Templates include two footer variants:
- **Footer A** (SEER < 14.3): Northern Regions Only
- **Footer B** (SEER ≥ 14.3): Nationwide Compliance

The pipeline automatically selects the correct footer based on the SEER2 rating.

## Filename Convention

Generated files follow standardized naming:

```
# Single component
Goodman_R410A_AC_GLXS5BA1810.html

# 2-component system
Goodman_1.5Ton_R410A_AC_System_GLXS5BA1810_AMST24BU13.html

# 3-component system
Goodman_R410A_AC_80AFUE_Upflow_System_GLXS5BA1810_GR9S800403ANA_CAPTA2422A3.html
```

## Troubleshooting

### Missing Specs Error

```
⚠️  Line 24: Missing specs for AMST36CU13
```

**Solution**: Add the missing model number to the specs JSON file with complete specifications.

### No Template Found Error

```
❌ No suitable template found for component types
```

**Solution**: Verify component types are recognized in `config.py` COMPONENT_PATTERNS.

### Template File Not Found

```
❌ Template file not found: template_xxx.html
```

**Solution**: Ensure all 18 template files exist in the `Scripts/` directory.

## Pipeline Architecture

```
main_generator.py
    ├─> config.py (validate paths, load mappings)
    ├─> sku_parser.py (parse SKUS file)
    ├─> spec_extractor.py (load specs JSON)
    │
    └─> For each SKU:
        ├─> template_selector.py (choose template)
        ├─> content_generator.py (generate title, intro, tables)
        └─> html_builder.py (assemble & save HTML)
```

## Adding New Equipment

### 1. Add SKU to SKUS File

```
# Add new model to appropriate section
GLXS5BA7210
```

### 2. Add Specs to JSON File

```json
{
  "GLXS5BA7210": {
    "model_number": "GLXS5BA7210",
    "brand": "Goodman",
    "equipment_type": "Air Conditioner Condenser",
    "tonnage": 6.0,
    ...
  }
}
```

### 3. Run Generator

```bash
python3 main_generator.py --seer 15.2
```

## Adding New SEER Rating

1. Create directory structure:
   ```bash
   mkdir -p "18.0_SEER2/{SKUS,Specs,Generated_Descriptions}"
   ```

2. Add SEER rating to `config.py`:
   ```python
   SEER_DIRS = {
       ...
       "18.0": BASE_DIR / "18.0_SEER2",
   }
   ```

3. Create SKUS file and specs JSON

4. Run generator:
   ```bash
   python3 main_generator.py --seer 18.0
   ```

## Development

### Testing Individual Components

```bash
# Test configuration
python3 config.py

# Test SKU parser
python3 sku_parser.py

# Test spec extractor
python3 spec_extractor.py

# Test template selector
python3 template_selector.py

# Test content generator
python3 content_generator.py

# Test HTML builder
python3 html_builder.py
```

### Modifying Templates

Templates are located in `Scripts/` and use placeholder patterns:
- `[PRODUCT TITLE PLACEHOLDER]` - Replaced with generated title
- `[INTRO PARAGRAPH PLACEHOLDER]` - Replaced with generated intro
- `[SPEC_ROWS_PLACEHOLDER]` - Replaced with spec table rows

## License

Internal tool for HVAC product description generation.

## Support

For issues or questions, contact the development team or create an issue in the repository.
