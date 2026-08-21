#!/usr/bin/env python3
"""
Parser de resultados de tests (JUnit XML).
Calcula la nota final según la fórmula de corrección.

Nota final:
  - Si algún mandatory falla → 3
  - Si no: nota = max(FLOOR, 9 - (error_64/3) - (2*error_32/43))
    donde error_64 = extra tests con prefijo "64" que fallaron  (max 9)
          error_32 = extra tests sin prefijo "64" que fallaron  (max 43)
"""

import xml.etree.ElementTree as ET
import sys

# ── Configuración ────────────────────────────────────────────────────────────
FLOOR       = 4     # Nota mínima posible (cambiable)
MAX_64      = 9     # Total de extra tests de 64-bit
MAX_32      = 43    # Total de extra tests de 32-bit
# ─────────────────────────────────────────────────────────────────────────────

PASS = "PASS"
FAIL = "FAIL"
SKIP = "SKIP"


def classify(classname: str) -> str:
    for cat in ("mandatory", "extra", "custom"):
        if cat in classname:
            return cat
    return "unknown"


def is_64bit(name: str) -> bool:
    return "64" in name


def parse_report(xml_path: str) -> None:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    testcases = root.findall(".//testcase")
    if not testcases:
        print("No se encontraron testcases en el XML.")
        return

    results = []
    for tc in testcases:
        name      = tc.get("name", "")
        classname = tc.get("classname", "")
        category  = classify(classname)

        if tc.find("skipped") is not None:
            status = SKIP
        elif tc.find("failure") is not None or tc.find("error") is not None:
            status = FAIL
        else:
            status = PASS

        results.append({
            "name":     name,
            "category": category,
            "status":   status,
        })

    # ── Tabla resumen por categoría con barras ────────────────────────────────
    categories = ["mandatory", "extra", "custom", "unknown"]
    BAR_WIDTH = 20

    def make_bar(passed, total):
        if total == 0:
            return "─" * BAR_WIDTH
        filled = round(BAR_WIDTH * passed / total)
        return "█" * filled + "░" * (BAR_WIDTH - filled)

    def pct(passed, total):
        return f"{100*passed//total:3d}%" if total else "  N/A"

    col_headers = ["Categoría", "Total", "Pass", "Fail", "Skip", "Progreso"]
    col_w = [10, 7, 6, 6, 6, BAR_WIDTH + 5]

    sep = "┼".join("─" * w for w in col_w)
    top = "┬".join("─" * w for w in col_w)
    bot = "┴".join("─" * w for w in col_w)

    def row(*cells):
        return "│".join(f"{str(c):<{w}}" for c, w in zip(cells, col_w))

    print(f"┌{top}┐")
    print(f"│{row(*col_headers)}│")
    print(f"├{sep}┤")

    for cat in categories:
        cat_results = [r for r in results if r["category"] == cat]
        if not cat_results:
            continue
        total = len(cat_results)
        passed = sum(1 for r in cat_results if r["status"] == PASS)
        failed = sum(1 for r in cat_results if r["status"] == FAIL)
        skipped = sum(1 for r in cat_results if r["status"] == SKIP)
        bar = make_bar(passed, total)
        progress = f"{bar} {pct(passed, total)}"
        print(f"│{row(cat, total, passed, failed, skipped, progress)}│")

    print(f"└{bot}┘")

    # ── Lista detallada de tests ──────────────────────────────────────────────
    print()
    col_name = max(len(r["name"]) for r in results)
    col_cat  = max(len(r["category"]) for r in results)
    header = f"  {'Test':<{col_name}}  {'Categoría':<{col_cat}}  Estado"
    print(header)
    print("  " + "─" * (len(header) - 2))
    for r in results:
        mark = "✓" if r["status"] == PASS else ("·" if r["status"] == SKIP else "✗")
        print(f"  {r['name']:<{col_name}}  {r['category']:<{col_cat}}  {mark}")

    # ── Cálculo de nota ───────────────────────────────────────────────────────
    mandatory_failed = any(
        r["status"] == FAIL for r in results if r["category"] == "mandatory"
    )

    extra_64_aciertos = sum(
        1 for r in results
        if r["category"] == "extra" and r["status"] == PASS and is_64bit(r["name"])
    )
    extra_32_aciertos = sum(
        1 for r in results
        if r["category"] == "extra" and r["status"] == PASS and not is_64bit(r["name"])
    )
    extra_64_errors = MAX_64 - extra_64_aciertos
    extra_32_errors = MAX_32 - extra_32_aciertos

    print()
    print("=== Resumen ===")
    print(f"  Mandatory fallidos  : {sum(1 for r in results if r['category'] == 'mandatory' and r['status'] == FAIL)}")
    print(f"  Extra 64-bit aciertos: {extra_64_aciertos}/{MAX_64}")
    print(f"  Extra 32-bit aciertos: {extra_32_aciertos}/{MAX_32}")

    if mandatory_failed:
        nota = 3.0
        print(f"\n  Nota final: {nota}  (Tests basicos no aprobados)")
    else:
        raw  = 9 - (extra_64_errors / 3) - (2 * extra_32_errors / MAX_32)
        nota = max(FLOOR, raw)
        print("\n === Nota ===")
        print(f"\n  Fórmula: 9 - ({extra_64_errors}/3) - (2×{extra_32_errors}/{MAX_32}) = {raw:.2f}")
        print(f"  Nota final grupal: {nota:.2f}")
        print("--------------------------------------------------------------------------------------------------------------")
        print("IMPORTANTE:")
        print("     - La nota máxima por el tp es 9. El punto restante se puede dar por prolijidad de código y el coloquio.")
        print("     - Por más que el TP grupal esté aprobado, se puede desaprobar el TP de forma individual en el coloquio.")



if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "report.xml"
    parse_report(path)
