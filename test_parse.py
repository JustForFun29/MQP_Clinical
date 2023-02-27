from xml_parser import *
from pathlib import Path
from pprint import PrettyPrinter
import pytest

pp = PrettyPrinter(indent=2)

test_xml = [
    Path("archive/NCT0000xxxx/NCT00000102.xml"),

    Path("archive/NCT0000xxxx/NCT00000111.xml"),
]


def test_main_schema():
    """
    This function tests the main_schema_dict function for the xml_parser.py
    """
    for i in test_xml:
        dict0 = extract_xml(i)
        main_dict = main_schema_dict(dict0)
        pp.pprint(main_dict)


def test_drug_schema():
    """
    This function tests the drug_schema_dict function for the xml_parser.py

    """
    for i in test_xml:
        dict0 = extract_xml(i)
        drug_dict = drug_schema_dict(dict0)
        for i in drug_dict:
            pp.pprint(i)

# test_main_schema();
test_drug_schema();