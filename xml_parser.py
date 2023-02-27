from pathlib import Path
from collections import defaultdict
import pandas as pd
from table_structure import *
import xmltodict
from xml.parsers.expat import ExpatError
from typing import Dict, DefaultDict


def get_terms(val) -> str:
    """
    This function takes a string and returns a list of the terms in the string
    """
    if isinstance(val, list):
        return ";".join(val)
    else:
        return val


def defaultify(d: Dict):
    """
    This function takes a dictionary and returns a defaultdict with the same
    values. Works recursively
    Parameters
    ----------
    d : dict
    """
    if not isinstance(d, dict):
        return d
    return defaultdict(lambda: None, {k: defaultify(v) for k, v in d.items()})


def extract_xml(path_to_xml: Path):
    """
    This function takes a path to an xml file and returns a dictionary with the
    relevant information for the database
    Parameters
    ----------
    path_to_xml : str
    """
    with open(path_to_xml) as f:
        try:
            doc = xmltodict.parse(f.read())
        except ExpatError:
            return None
    return defaultify(doc)


def drug_schema_dict(parsed_dict: Dict[str, str]) -> Dict[str, str]:
    """
    This function takes the parsed dictionary of the xml file and returns a
    dictionary with the drug schema information
    Parameters
    ----------
    parsed_dict : dict
        The dictionary that is returned from the extract_xml function

    Schema can be found at https://docs.google.com/spreadsheets/d/1nDoMNKbCGw4hKuMX2n5Y4rdsm1TOKV8a3MhVNeBKRBA/edit#gid=0
    """
    parsed_dict = parsed_dict["clinical_study"]

    if parsed_dict["intervention"] is None:
        return [{"nct_id": parsed_dict["id_info"]["nct_id"], "drug_name": None},
                {"nct_id": parsed_dict["id_info"]["nct_id"],
                 "drug_name": None}]  # this is done to stop in case there is no intervention field

    if type(parsed_dict["intervention"]) == list:
        for intervention in parsed_dict["intervention"]:
            if intervention["intervention_type"] == "Drug":
                try:
                    drug_dict = {
                        "nct_id": parsed_dict["id_info"]["nct_id"],
                        "drug_name": intervention["intervention_name"],
                    }
                except TypeError:
                    drug_dict = {
                        "nct_id": parsed_dict["id_info"]["nct_id"],
                        "drug_name": None,
                    }
                yield drug_dict
    else:
        if parsed_dict["intervention"]["intervention_type"] == "Drug":
            try:
                drug_dict = {
                    "nct_id": parsed_dict["id_info"]["nct_id"],
                    "drug_name": parsed_dict["intervention"]["intervention_name"],
                }
            except TypeError:
                drug_dict = {
                    "nct_id": parsed_dict["id_info"]["nct_id"],
                    "drug_name": None,
                }

            yield drug_dict


def main_schema_dict(parsed_dict: Dict[str, str]) -> Dict[str, str]:
    """
    This function takes the parsed dictionary of the xml file and returns a
    dictionary with the main schema information
    Parameters
    ----------
    parsed_dict : dict
        The dictionary that is returned from the extract_xml function
    Schema can be found at https://docs.google.com/spreadsheets/d/1nDoMNKbCGw4hKuMX2n5Y4rdsm1TOKV8a3MhVNeBKRBA/edit#gid=0
    """
    try:
        parsed_dict = parsed_dict["clinical_study"]
    except TypeError:
        return None

    main_schema_dict = {
        "nct_id": parsed_dict["id_info"]["nct_id"],
        "org_study_id": parsed_dict["id_info"]["org_study_id"],
        "brief_title": parsed_dict["brief_title"],
        "official_title": parsed_dict["official_title"],
        "overall_status": parsed_dict["overall_status"],
        "study_type": parsed_dict["study_type"],
        "source": parsed_dict["source"],
        "phase": parsed_dict["phase"],
        "start_date": parsed_dict["start_date"],
        # "condition": get_terms(parsed_dict["condition"])
    }
    try:
        main_schema_dict["brief_summary"] = parsed_dict["brief_summary"]["textblock"]  # some files don't have this
    except TypeError:
        main_schema_dict["brief_summary"] = None

    try:
        main_schema_dict["detailed_description"] = parsed_dict["detailed_description"]["textblock"]
    except TypeError:
        main_schema_dict["detailed_description"] = None

    return main_schema_dict