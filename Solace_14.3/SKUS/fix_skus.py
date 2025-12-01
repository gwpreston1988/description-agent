#!/usr/bin/env python3
import csv

# Read the CSV and extract all system combinations with corrected model numbers
with open('/Users/georgepreston/description-agent/Solace_14.3/Skus.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header

    individual_components = []
    system_combinations = []

    for row in reader:
        # Reconstruct SKU field - it's all columns before the first price column
        sku_parts = []
        for col in row:
            if col.startswith('$'):
                break
            sku_parts.append(col)

        sku = ','.join(sku_parts)

        # Check if it's a system (contains comma)
        if ',' in sku:
            # Split the SKUs and add S- prefix to all
            parts = [part.strip() for part in sku.split(',')]
            corrected_parts = []

            for part in parts:
                # Add S- prefix if not present
                if not part.startswith('S-'):
                    part = 'S-' + part

                # Fix known model number issues
                part = part.replace('AMST60CU13', 'AMST60DU13')
                part = part.replace('AWST18SU1305', 'AWST18SU1305A')
                part = part.replace('AWST24SU1305', 'AWST24SU1305A')
                part = part.replace('AWST30SU1308', 'AWST30LU1308A')
                part = part.replace('AWST30SU1310', 'AWST30LU1310A')
                part = part.replace('AWST36SU1308', 'AWST36LU1308A')
                part = part.replace('AWST36SU1310', 'AWST36LU1310A')
                part = part.replace('CHPT6030D3', 'CHPTA6030D3')

                corrected_parts.append(part)

            system_combinations.append(','.join(corrected_parts))
        else:
            individual_components.append(sku)

    print(f"Individual components: {len(individual_components)}")
    print(f"System combinations: {len(system_combinations)}")
    print(f"Total: {len(individual_components) + len(system_combinations)}")

    # Write complete SKUS file
    with open('SKUS', 'w') as out:
        out.write("# Individual Components - Heat Pumps\n")
        for comp in individual_components:
            if 'GLZS' in comp:
                out.write(comp + '\n')

        out.write("\n# Individual Components - Air Conditioners\n")
        for comp in individual_components:
            if 'GLXS' in comp:
                out.write(comp + '\n')

        out.write("\n# Individual Components - Standard Air Handlers\n")
        for comp in individual_components:
            if 'AMST' in comp:
                out.write(comp + '\n')

        out.write("\n# Individual Components - Wall-Mounted Air Handlers\n")
        for comp in individual_components:
            if 'AWST' in comp:
                out.write(comp + '\n')

        out.write("\n# Individual Components - Thermostats\n")
        for comp in individual_components:
            if 'HKTS' in comp or '0230K' in comp:
                out.write(comp + '\n')

        out.write("\n# Individual Components - 80% AFUE Furnaces\n")
        for comp in individual_components:
            if 'GR9S80' in comp:
                out.write(comp + '\n')

        out.write("\n# Individual Components - 92% AFUE Furnaces\n")
        for comp in individual_components:
            if 'GR9S92' in comp:
                out.write(comp + '\n')

        out.write("\n# Individual Components - Upflow Coils\n")
        for comp in individual_components:
            if 'CAPTA' in comp:
                out.write(comp + '\n')

        out.write("\n# Individual Components - Horizontal Coils\n")
        for comp in individual_components:
            if 'CHPTA' in comp:
                out.write(comp + '\n')

        out.write("\n# HP + Air Handler Systems\n")
        for sys in system_combinations:
            if 'GLZS' in sys and ('AMST' in sys or 'AWST' in sys) and 'GR9S' not in sys:
                out.write(sys + '\n')

        out.write("\n# AC + Air Handler Systems\n")
        for sys in system_combinations:
            if 'GLXS' in sys and ('AMST' in sys or 'AWST' in sys) and 'GR9S' not in sys:
                out.write(sys + '\n')

        out.write("\n# AC + 80% Furnace + Coil Systems\n")
        for sys in system_combinations:
            if 'GLXS' in sys and 'GR9S80' in sys:
                out.write(sys + '\n')

        out.write("\n# HP + 80% Furnace + Coil Systems (Dual Fuel)\n")
        for sys in system_combinations:
            if 'GLZS' in sys and 'GR9S80' in sys:
                out.write(sys + '\n')

        out.write("\n# AC + 92% Furnace + Coil Systems\n")
        for sys in system_combinations:
            if 'GLXS' in sys and 'GR9S92' in sys:
                out.write(sys + '\n')

        out.write("\n# HP + 92% Furnace + Coil Systems (Dual Fuel)\n")
        for sys in system_combinations:
            if 'GLZS' in sys and 'GR9S92' in sys:
                out.write(sys + '\n')

print("\n✅ SKUS file created with all 147 products")
