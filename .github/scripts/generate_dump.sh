#!/bin/bash

set -e

run_tests() {
    local tipo=$1
    local asm_dir=""
    local output_dir=""

    if [ "$tipo" == "extra" ]; then
        asm_dir="./inputs/extra_asm"
        output_dir="extra_dumpsim"
    elif [ "$tipo" == "custom" ]; then
        asm_dir="./inputs/custom_asm"
        output_dir="custom_dumpsim"
    else
        # Por defecto o "mandatory"
        asm_dir="./inputs/asm"
        output_dir="mandatory_dumpsim"
    fi

    mkdir -p "$output_dir"

    generar_comandos_sim() {
        for i in {1..27}; do
            echo "rdump"
            echo "mdump 0x10000000 0x10000030"
            echo "r 1"
        done
        # El último dump sin el "r 1" final
        echo "rdump"
        echo "mdump 0x10000000 0x10000030"
    }

    find "$asm_dir" -type f -name "*.s" | while read -r file; do
        echo "Processing $file with asm2hex..."
        ./inputs/asm2hex "$file"

        # Obtenemos el nombre base sin extensión y sin ruta
        base_name=$(basename "$file" .s)
        output_file="${base_name}.x"

        if [ -f "${file%.s}.x" ]; then
            mv "${file%.s}.x" ./inputs/
        fi

        if [ -f "inputs/$output_file" ]; then
            
            # --- Ejecutar sim usuario ---
            echo "Processing $output_file with sim..."
            generar_comandos_sim | ./src/sim "inputs/$output_file" > /dev/null
            mv "dumpsim" "${output_dir}/dumpsim_user_${base_name}"

            # --- Ejecutar sim referencia ---
            echo "Processing $output_file with ref_sim..."
            generar_comandos_sim | ./ref_sim_x86 "inputs/$output_file" > /dev/null
            mv "dumpsim" "${output_dir}/dumpsim_ref_${base_name}"

        else
            echo "Error: No se encontró el archivo generado inputs/$output_file"
        fi
    done
}

run_tests "mandatory"
if [[ "$(ls -A ./inputs/custom_asm)" ]]; then
    run_tests "custom"
fi

run_tests "extra"