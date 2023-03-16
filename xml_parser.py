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
        except (ExpatError, UnicodeError):
            return None
    return defaultify(doc)


def disease_schema_dict(parsed_dict: Dict[str, str]) -> Dict[str, str]:
    """
    This function takes the parsed dictionary of the xml file and returns a
    dictionary with the drug schema information
    Parameters
    ----------
    parsed_dict : dict
        The dictionary that is returned from the extract_xml function
    """

    parsed_dict = parsed_dict["clinical_study"]

    if parsed_dict["condition"] is None:
        return []

    if type(parsed_dict["condition"]) == list:
        diseases = []
        for condition in parsed_dict["condition"]:
            if condition is None or condition.strip() == "":
                continue
            diseases.append({"disease_name": condition.strip().lower()})
        return diseases
    else:
        condition = parsed_dict["condition"]
        if condition is None or condition.strip() == "":
            return []
        return [{"disease_name": condition.strip().lower()}]
    # parsed_dict = parsed_dict["clinical_study"]
    # nct_id = parsed_dict["id_info"]["nct_id"]
    # diseases = []
    #
    # if parsed_dict["condition"] is None:
    #     diseases.append({"nct_id": nct_id, "disease_name": None})
    #     return diseases
    #
    # if isinstance(parsed_dict["condition"], list):
    #     for disease_name in parsed_dict["condition"]:
    #         diseases.append({"nct_id": nct_id, "disease_name": disease_name})
    # else:
    #     diseases.append({"nct_id": nct_id, "disease_name": parsed_dict["condition"]})
    #
    # return diseases

    # parsed_dict = parsed_dict["clinical_study"]
    #
    # if parsed_dict["condition"] is None:
    #     return [{"nct_id": parsed_dict["id_info"]["nct_id"], "disease_name": None},
    #             {"nct_id": parsed_dict["id_info"]["nct_id"], "disease_name": None}]
    #
    # if type(parsed_dict["condition"]) == list:
    #     for disease in parsed_dict["condition"]:
    #         try:
    #             disease_dict = {
    #                 "nct_id": parsed_dict["id_info"]["nct_id"],
    #                 "disease_name": disease,
    #             }
    #         except TypeError:
    #             disease_dict = {
    #                 "nct_id": parsed_dict["id_info"]["nct_id"],
    #                 "disease_name": None,
    #             }
    #         yield disease_dict
    # else:
    #     try:
    #         disease_dict = {
    #             "nct_id": parsed_dict["id_info"]["nct_id"],
    #             "disease_name": parsed_dict["condition"],
    #         }
    #     except TypeError:
    #         disease_dict = {
    #             "nct_id": parsed_dict["id_info"]["nct_id"],
    #             "disease_name": None,
    #         }
    #     yield disease_dict

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
                {"nct_id": parsed_dict["id_info"]["nct_id"], "drug_name": None}]  # this is done to stop in case there is no intervention field

    if type(parsed_dict["intervention"]) == list:
        for intervention in parsed_dict["intervention"]:
            if intervention["intervention_type"] == "Drug":
                try:
                    drug_dict = {
                        "drug_name": intervention["intervention_name"].lower(),
                    }
                except TypeError:
                    drug_dict = {
                        "drug_name": None,
                    }
                yield drug_dict
    else:
        if parsed_dict["intervention"]["intervention_type"] == "Drug":
            try:
                drug_dict = {
                        "drug_name": parsed_dict["intervention"]["intervention_name"].lower(),
                }
            except TypeError:
                drug_dict = {
                        "drug_name": None
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
        "start_date": parsed_dict["start_date"]
    }

    if "condition" in parsed_dict:
        if parsed_dict["condition"] is None:
            main_schema_dict["diseases"] = None
        elif isinstance(parsed_dict["condition"], list):
            try:
                main_schema_dict["diseases"] = list(
                    filter(lambda x: isinstance(x, str), map(lambda x: x.lower(), parsed_dict["condition"])))
            except TypeError:
                main_schema_dict["diseases"] = None
        else:
            try:
                main_schema_dict["diseases"] = parsed_dict["condition"].lower()
            except AttributeError:
                main_schema_dict["diseases"] = None
    else:
        main_schema_dict["diseases"] = None

    if type(parsed_dict["intervention"]) == list:
        for intervention in parsed_dict["intervention"]:
            if intervention["intervention_type"] == "Drug":
                try:
                    main_schema_dict["drugs"] = intervention["intervention_name"].lower()
                except TypeError:
                    main_schema_dict["drugs"] = None
    else:
            try:
                if parsed_dict["intervention"]["intervention_type"] == "Drug":
                    main_schema_dict["drugs"] = parsed_dict["intervention"]["intervention_name"].lower()
            except TypeError:
                main_schema_dict["drugs"] = None

    try:
        main_schema_dict["drug_name"] = parsed_dict["intervention"]["intervention_name"].lower()
    except TypeError:
        main_schema_dict["drug_name"] = None

    try:
        main_schema_dict["minimum_age"] = parsed_dict["eligibility"]["minimum_age"]
    except TypeError:
        main_schema_dict["minimum_age"] = None

    try:
        main_schema_dict["maximum_age"] = parsed_dict["eligibility"]["maximum_age"]
    except TypeError:
        main_schema_dict["maximum_age"] = None

    try:
        main_schema_dict["gender"] = parsed_dict["eligibility"]["gender"]
    except TypeError:
        main_schema_dict["gender"] = None

    try:
        main_schema_dict["criteria"] = parsed_dict["eligibility"]["criteria"]["textblock"]
    except TypeError:
        main_schema_dict["criteria"] = None

    try:
        main_schema_dict["intervention_model"] = parsed_dict["study_design_info"]["intervention_model"]
    except TypeError:
        main_schema_dict["intervention_model"] = None

    try:
        main_schema_dict["primary_purpose"] = parsed_dict["study_design_info"]["primary_purpose"]
    except TypeError:
        main_schema_dict["primary_purpose"] = None

    try:
        main_schema_dict["masking"] = parsed_dict["study_design_info"]["masking"]
    except TypeError:
        main_schema_dict["masking"] = None


    try:
        main_schema_dict["brief_summary"] = parsed_dict["brief_summary"]["textblock"]  # some files don't have this
    except TypeError:
        main_schema_dict["brief_summary"] = None

    try:
        main_schema_dict["detailed_description"] = parsed_dict["detailed_description"]["textblock"]
    except TypeError:
        main_schema_dict["detailed_description"] = None

    return main_schema_dict