import re
import sys
import os
from pathlib import Path
import curses

# KiCad simulation device primitive type mappings
SPICE_TYPES = {'d': '1', 'q': '2', 'nmk': '3', 'pmk': '3', 'j': '5'}

def index_spice_models(models_dir):
    """Scans local directories to auto-index available .model and .subckt definitions."""
    model_index = {}
    extensions = {'.lib', '.sub', '.mod', '.sp', '.cir', '.txt'}
    search_path = Path(models_dir)
    if not search_path.exists():
        return model_index

    # Strict regex to extract SPICE keywords safely
    model_re = re.compile(r'^\s*\.model\s+([^\s\(\)]+)\s+([a-z0-9]+)', re.IGNORECASE)
    subckt_re = re.compile(r'^\s*\.subckt\s+([^\s]+)', re.IGNORECASE)

    for file_path in search_path.glob('**/*'):
        if file_path.suffix.lower() not in extensions:
            continue
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    sub_match = subckt_re.match(line)
                    if sub_match:
                        name = sub_match.group(1)
                        model_index[name.lower()] = ("4", name, str(file_path.resolve()))
                        continue
                    mod_match = model_re.match(line)
                    if mod_match:
                        name = mod_match.group(1)
                        sim_type = SPICE_TYPES.get(mod_match.group(2).lower(), "4")
                        model_index[name.lower()] = (sim_type, name, str(file_path.resolve()))
        except Exception:
            pass
    return model_index

def draw_menu(stdscr, title, options):
    """Renders a clean Linux CLI selection window."""
    curses.curs_set(0)
    current_row = 0
    
    while True:
        stdscr.clear()
        # Header text
        stdscr.addstr(0, 0, title, curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(1, 0, "Use Up/Down Arrow keys to navigate, press Enter to select.", curses.A_DIM)
        
        for idx, option in enumerate(options):
            if idx == current_row:
                stdscr.addstr(idx + 3, 2, f"-> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 3, 2, f"   {option}")
        
        stdscr.refresh()
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key in:  # Enter keys
            return current_row

def parse_s_expression_blocks(text):
    """Finds top-level (symbol ...) blocks using a fast paren-counter loop."""
    blocks = []
    start = 0
    while True:
        pos = text.find('(symbol ', start)
        if pos == -1:
            break
        
        # Brace matching to extract the exact layout block boundaries
        paren_count = 0
        end_pos = pos
        for i in range(pos, len(text)):
            if text[i] == '(':
                paren_count += 1
            elif text[i] == ')':
                paren_count -= 1
                if paren_count == 0:
                    end_pos = i + 1
                    break
        blocks.append((pos, end_pos))
        start = end_pos
    return blocks

def main_tui(stdscr, sch_path, models_dir):
    sch_file = Path(sch_path)
    spice_db = index_spice_models(models_dir)
    
    if not spice_db:
        stdscr.addstr(0, 0, f"Error: No SPICE models indexed in '{models_dir}'. Press any key to exit.")
        stdscr.getch()
        return

    content = sch_file.read_text(encoding='utf-8')
    block_indices = parse_s_expression_blocks(content)
    
    # Process blocks from end to start to allow string substitutions without shifting indices
    updated_content = content
    
    for start, end in reversed(block_indices):
        block = content[start:end]
        
        ref_match = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        val_match = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
        
        if not ref_match or not val_match:
            continue
            
        ref = ref_match.group(1)
        val = val_match.group(1).strip()
        val_lower = val.lower()
        
        # Native basic passives don't require external model assignment pipelines
        if re.match(r'^[RCL]', ref) and val_lower not in spice_db:
            continue

        # Option A: Fast Auto-Assignment
        if val_lower in spice_db:
            sim_type, official_name, file_path = spice_db[val_lower]
        # Option B: Fallback into Interactive Selection UI
        else:
            suggestions = [name for name in spice_db.keys() if val_lower in name or name in val_lower][:3]
            menu_options = [f"Skip processing {ref}"]
            
            for s in suggestions:
                menu_options.append(f"Auto-link model candidate: '{spice_db[s][1]}' from {Path(spice_db[s][2]).name}")
            menu_options.append("Manually pass file path string")
            
            title = f"Component Unmatched: Reference = {ref} | Value = {val}"
            choice = draw_menu(stdscr, title, menu_options)
            
            if choice == 0:
                continue
            elif choice <= len(suggestions):
                selected_key = suggestions[choice - 1]
                sim_type, official_name, file_path = spice_db[selected_key]
            else:
                # Text input prompt for raw file target configurations
                curses.echo()
                curses.curs_set(1)
                stdscr.clear()
                stdscr.addstr(0, 0, f"Enter full Linux file path to SPICE model for {ref}: ")
                user_file = stdscr.getstr().decode('utf-8').strip()
                stdscr.addstr(2, 0, "Enter target model/subcircuit sub-name (e.g. LM741): ")
                official_name = stdscr.getstr().decode('utf-8').strip()
                sim_type = "4"
                file_path = user_file
                curses.noecho()
                curses.curs_set(0)
                if not os.path.exists(file_path):
                    continue

        # Scrub older sim definitions to guarantee pure overrides
        block = re.sub(r'\(property\s+"sim\.model".*?\)\s*', '', block)
        block = re.sub(r'\(property\s+"sim\.type".*?\)\s*', '', block)
        block = re.sub(r'\(property\s+"sim\.device".*?\)\s*', '', block)
        
        # Format injected properties right before the final closing paren of the component
        spice_properties = (
            f'\n    (property "sim.type" "{sim_type}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))'
            f'\n    (property "sim.model" "{official_name}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))'
            f'\n    (property "sim.device" "{file_path}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))'
        )
        
        # Modify the symbol string safely
        last_paren_idx = block.rfind(')')
        new_block = block[:last_paren_idx] + spice_properties + "\n  )"
        
        # Replace slice in working copy string asset
        updated_content = updated_content[:start] + new_block + updated_content[end:]

    # Output modified schema back safely to file system layout blocks
    sch_file.with_suffix('.sch.bak').write_text(content, encoding='utf-8')
    sch_file.write_text(updated_content, encoding='utf-8')
    
    stdscr.clear()
    stdscr.addstr(0, 0, "Execution finished! KiCad schematic updated cleanly. Press any key to exit.", curses.A_BOLD)
    stdscr.getch()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 linux_spice_tui.py <schematic.kicad_sch> <spice_models_dir>")
    else:
        curses.wrapper(main_tui, sys.argv[1], sys.argv[2])

