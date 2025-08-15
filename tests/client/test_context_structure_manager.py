import os
import pytest
yaml_path = os.path.join(os.path.dirname(__file__), '../../client/context_structure.yaml')
from client.app.context_structure_manager import ContextStructureManager

def test_parse_and_add_field(tmp_path):
    # Copy the sample yaml to a temp file
    test_yaml = tmp_path / "context_structure.yaml"
    with open(yaml_path) as f:
        test_yaml.write_text(f.read())
    mgr = ContextStructureManager(str(test_yaml))
    orig = mgr.get_full_structure()
    assert isinstance(orig, list)
    # Add a new uncategorized field
    mgr.add_field('test_field')
    updated = mgr.get_full_structure()
    assert 'test_field' in updated
    # Check that the field is in the uncategorized section
    with open(test_yaml) as f:
        content = f.read()
    assert 'test_field' in content
    assert '### uncategorized--chronological ###' in content

def test_multiple_fields(tmp_path):
    test_yaml = tmp_path / "context_structure.yaml"
    with open(yaml_path) as f:
        test_yaml.write_text(f.read())
    mgr = ContextStructureManager(str(test_yaml))
    mgr.add_field('field1')
    mgr.add_field('field2')
    struct = mgr.get_full_structure()
    assert 'field1' in struct and 'field2' in struct
