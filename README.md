# HVAC Description Generator

**Automated pipeline for generating professional HTML product descriptions for HVAC equipment systems.**

Transforms SKU lists and technical specifications into rich, SEO-optimized product pages ready for e-commerce platforms.

## Key Features

- **Template-Based Generation** — 18 specialized templates for different HVAC system configurations
- **Multi-Component Support** — Handles single units, 2-component, and 3-component systems
- **Automatic Template Selection** — Intelligently matches components to the correct template
- **SEER-Based Footer Logic** — Automatically applies regional compliance footers
- **Dry-Run Mode** — Preview all changes before generating files
- **Validation Tools** — Verify SKU/spec alignment before generation

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Pipeline** | Python 3 |
| **Preview UI** | Next.js 14, React, TypeScript |
| **Styling** | Tailwind CSS |
| **Output** | Static HTML (e-commerce ready) |

## Quick Start

### Generate Descriptions

```bash
# Validate SKUs have matching specs
python3 generator/main_generator.py --seer 15.2 --validate-only

# Preview without writing files
python3 generator/main_generator.py --seer 15.2 --dry-run

# Generate all descriptions
python3 generator/main_generator.py --seer 15.2
```

### Preview UI

```bash
npm install
npm run dev
```

## Architecture

```
description-agent/
├── generator/                  # Python pipeline
│   ├── config.py              # Paths and mappings
│   ├── sku_parser.py          # SKU parsing and system detection
│   ├── spec_extractor.py      # Spec data extraction
│   ├── template_selector.py   # Template matching logic
│   ├── content_generator.py   # Dynamic content generation
│   ├── html_builder.py        # HTML assembly
│   └── main_generator.py      # CLI orchestration
│
├── app/                        # Next.js preview UI
├── components/                 # React components
├── data/                       # Runtime data
│
├── {SEER}_SEER2/              # Equipment data by efficiency
│   ├── SKUS/                  # SKU list files
│   ├── Specs/                 # JSON specifications
│   └── Generated_Descriptions/ # Output (gitignored)
│
└── legacy/                     # Archived templates
```

## Pipeline Flow

```
SKU List → Parse → Load Specs → Select Template → Generate Content → Build HTML → Save File
   │          │         │              │                │              │
   ▼          ▼         ▼              ▼                ▼              ▼
 SKUS/     System    *.json      Template       Title, Intro,    Complete
 SKUS      Types    Specs        Match          Spec Tables      HTML Page
```

## System Types Supported

### Single Components
- AC Condensers
- Heat Pump Condensers
- Air Handlers (Standard & Wall-Mounted)
- Evaporator Coils (Upflow & Horizontal)
- Gas Furnaces (80%, 92%, 96% AFUE)
- Packaged Units

### Multi-Component Systems
- AC + Air Handler
- HP + Air Handler
- AC + Coil
- HP + Coil
- Furnace + Coil
- AC + Furnace + Coil
- HP + Furnace + Coil (Dual Fuel)

## File Formats

### SKU Input
```
# Comments start with #
GLXS5BA1810                           # Single component
GLXS5BA1810, AMST24BU13               # 2-component system
GLXS5BA1810, GR9S800403ANA, CAPTA2422A3  # 3-component system
```

### Spec JSON
```json
{
  "GLXS5BA1810": {
    "model_number": "GLXS5BA1810",
    "brand": "Goodman",
    "equipment_type": "Air Conditioner Condenser",
    "tonnage": 1.5,
    "seer2": 15.2,
    "refrigerant_type": "R-410A"
  }
}
```

### Output Naming
```
Goodman_1.5Ton_R410A_AC_System_GLXS5BA1810_AMST24BU13.html
```

## Command Reference

```bash
# Test pipeline configuration
python3 generator/main_generator.py --test-config

# Validate SKUs against specs
python3 generator/main_generator.py --seer 15.2 --validate-only

# Dry run (preview only)
python3 generator/main_generator.py --seer 15.2 --dry-run

# Generate all for a SEER rating
python3 generator/main_generator.py --seer 15.2

# Available SEER ratings
--seer 13.4 | 14.3 | 15.2 | 16.2 | 17.2 | 17.5
```

## License

Private - All rights reserved
