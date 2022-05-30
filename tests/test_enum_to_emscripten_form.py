import os
import sys
from unittest.mock import patch

import enum_to_emscripten_form


here = os.path.abspath(os.path.dirname(__file__))


# def test_parse_args():
test_args = ["enum_to_emscripten_form", "--file", os.path.join(here, 'data', 'issue_enum_reference_rule.txt'), "--className", "Issue", "--enum", "ReferenceRule"]
with patch.object(sys, 'argv', test_args):
    enum_to_emscripten_form.main()


# test_parse_args()
