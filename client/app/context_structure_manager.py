import yaml
import os

GENERATED_START = '# --- GENERATED START ---'
GENERATED_END = '# --- GENERATED END ---'
UNCAT_HEADER = '### uncategorized--chronological ###'

class ContextStructureManager:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        self.structure, self.uncategorized = self._parse_yaml()

    def _parse_yaml(self):
        with open(self.yaml_path) as f:
            lines = f.readlines()
        in_generated = False
        in_uncat = False
        generated_lines = []
        uncat_lines = []
        for line in lines:
            if GENERATED_START in line:
                in_generated = True
                continue
            if GENERATED_END in line:
                in_generated = False
                continue
            if UNCAT_HEADER in line:
                in_uncat = True
                continue
            if in_generated:
                generated_lines.append(line)
            elif in_uncat:
                uncat_lines.append(line)
        structure = yaml.safe_load(''.join(generated_lines)) if generated_lines else []
        uncategorized = yaml.safe_load(''.join(uncat_lines)) if uncat_lines else []
        return structure, uncategorized

    def add_field(self, field):
        # Add a new uncategorized field
        if not self.uncategorized:
            self.uncategorized = []
        self.uncategorized.append(field)
        # If the uncategorized header is missing, add it to the file
        with open(self.yaml_path, 'r') as f:
            content = f.read()
        if UNCAT_HEADER not in content:
            # Add the header and a newline at the end
            with open(self.yaml_path, 'a') as f:
                f.write(f'\n{UNCAT_HEADER}\n')
        self._write_yaml()

    def _write_yaml(self):
        with open(self.yaml_path, 'r') as f:
            lines = f.readlines()
        out_lines = []
        in_uncat = False
        wrote_uncat = False
        for idx, line in enumerate(lines):
            if UNCAT_HEADER in line:
                out_lines.append(line)
                in_uncat = True
                # Write uncategorized fields (with proper indentation)
                if self.uncategorized:
                    dumped = yaml.dump(self.uncategorized, default_flow_style=False)
                    # Indent if needed (YAML dump may not indent top-level list)
                    for l in dumped.splitlines():
                        out_lines.append(l + '\n')
                wrote_uncat = True
                # Skip any old uncategorized fields until next non-empty, non-comment line or EOF
                j = idx + 1
                while j < len(lines):
                    if lines[j].strip() == '' or lines[j].strip().startswith('#'):
                        out_lines.append(lines[j])
                        j += 1
                    else:
                        break
                # Continue from where we left off
                continue
            if in_uncat and wrote_uncat:
                # After writing uncategorized, just copy the rest
                in_uncat = False
            if not in_uncat:
                out_lines.append(line)
        with open(self.yaml_path, 'w') as f:
            f.writelines(out_lines)

    def get_full_structure(self):
        # Return generated + uncategorized
        return (self.structure or []) + (self.uncategorized or [])

# For test/demo usage
if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), '../context_structure.yaml')
    mgr = ContextStructureManager(path)
    print('Initial structure:', mgr.get_full_structure())
    mgr.add_field('new_field')
    print('After adding:', mgr.get_full_structure())
