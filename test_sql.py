from sqlmodel import Field, Session, SQLModel, create_engine, select
from pathlib import Path
from table_structure import *
from xml_parser import *

test_xml = [
    Path("archive/NCT0000xxxx/NCT00000102.xml"),
    Path("archive/NCT0000xxxx/NCT00000111.xml"),
]

engine = create_engine("sqlite:///testing_database.db")
SQLModel.metadata.create_all(engine)


def test_sql_main_schema():
    """
    This function tests the main_schema_dict function for the xml_parser.py
    can be added to an sql database
    """

    for i in test_xml:
        dict0 = extract_xml(i)
        CTPdict = main_schema_dict(dict0)
        add_CTPgeneral = MainTable(**CTPdict)
        with Session(engine) as session:
            session.add(add_CTPgeneral)
            session.commit()
            print(f"\n Added {i.stem}")


def test_sql_drug_schema():
    """
    This function tests the drug_schema_dict function for the xml_parser.py
    can be added to an sql database
    """
    for i in test_xml:
        dict0 = extract_xml(i)
        drug_dict = drug_schema_dict(dict0)
        for drug_entry in drug_dict:
            add_drug = DrugTable(**drug_entry)
            with Session(engine) as session:
                session.add(add_drug)
                session.commit()
        print(f"\n Added {i.stem}")

test_sql_main_schema()
# test_sql_drug_schema()