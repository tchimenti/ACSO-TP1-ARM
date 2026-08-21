import re
from pathlib import Path

def parse_dumpsim(filepath: str) -> list[dict]:
   text = Path(filepath).read_text()

   # Separar en bloques por el encabezado de registro
   raw_blocks = re.split(r"Current register/bus values\s*:", text)
   # El primer elemento antes del primer bloque suele ser vacío
   raw_blocks = [b for b in raw_blocks if b.strip()]

   states = []
   for block in raw_blocks:
      state = {}

      # Instruction Count
      m = re.search(r"Instruction Count\s*:\s*(\d+)", block)
      state["instruction_count"] = int(m.group(1)) if m else None

      # PC
      m = re.search(r"PC\s*:\s*(0x[0-9a-fA-F]+)", block)
      state["pc"] = int(m.group(1), 16) if m else None

      # Registros X0..X31
      state["registers"] = {}
      for rm in re.finditer(r"(X\d+)\s*:\s*(0x[0-9a-fA-F]+)", block):
            state["registers"][rm.group(1)] = int(rm.group(2), 16)

      # Flags
      m = re.search(r"FLAG_N\s*:\s*(\d+)", block)
      state["flag_n"] = int(m.group(1)) if m else None

      m = re.search(r"FLAG_Z\s*:\s*(\d+)", block)
      state["flag_z"] = int(m.group(1)) if m else None

      # Memory contents
      state["memory"] = {}
      for mm in re.finditer(
            r"(0x[0-9a-fA-F]+)\s*\(\d+\)\s*:\s*(0x[0-9a-fA-F]+)", block
      ):
            addr = int(mm.group(1), 16)
            val  = int(mm.group(2), 16)
            state["memory"][addr] = val

      states.append(state)

   return states