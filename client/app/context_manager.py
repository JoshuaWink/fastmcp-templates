import yaml

class ContextManager:
    def __init__(self, structure_path):
        with open(structure_path) as f:
            self.structure = yaml.safe_load(f)

    def _assemble(self, structure, context):
        result = {}
        for item in structure:
            if isinstance(item, str):
                if item in context:
                    result[item] = context[item]
            elif isinstance(item, dict):
                for k, v in item.items():
                    if k in context and isinstance(context[k], dict):
                        result[k] = self._assemble(v, context[k])
        return result

    def format_message(self, context):
        return self._assemble(self.structure, context)
