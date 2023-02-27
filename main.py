import os
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from xml_parser import *
from pathlib import Path
from pprint import PrettyPrinter
from sqlmodel import Field, Session, SQLModel, create_engine, select
import pytest

pp = PrettyPrinter(indent=2)
engine = create_engine("sqlite:///clinical-trial.db")
SQLModel.metadata.create_all(engine)

def traverse_folders():
    path = "/Users/jff/Desktop/MQP/archive"
    filelist = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith('.xml'):
                continue
            filelist.append(os.path.join(root, file))


    # THIS LINES FOR TESTING
    # for file in filelist:
    #     dict0 = extract_xml(file)
    #     main_dict = main_schema_dict(dict0)
    #     pp.pprint(main_dict)

    # for file in filelist:
    #     dict0 = extract_xml(file)
    #     CTPdict = main_schema_dict(dict0)
    #     add_CTPgeneral = MainTable(**CTPdict)
    #     with Session(engine) as session:
    #         session.add(add_CTPgeneral)
    #         session.commit()
    #         print(f"\n Added {file}")


    for i in filelist:
        dict0 = extract_xml(i)
        drug_dict = drug_schema_dict(dict0)
        for drug_entry in drug_dict:
            add_drug = DrugTable(**drug_entry)
            with Session(engine) as session:
                session.add(add_drug)
                session.commit()
        print(f"\n Added {i}")


def main():
    traverse_folders()

# def traverse_folders_2():
#     ## directory with XML files
#     path = "/Users/jff/Desktop/MQP/archive"
#     filenames = []
#
#     ## Count the number of xml files of each folder
#     files = os.listdir(path)
#     print("\n")
#
#     xml_data_to_csv = open('/Users/jff/Desktop/MQP/xml_extract.csv', 'w')
#     list_head = []
#     csvwriter = csv.writer(xml_data_to_csv)
#
#     # Read XML files in a folder
#     for filename in os.listdir(path):
#         if not filename.endswith('.xml'):
#             continue
#         fullname = os.path.join(path, filename)
#         print("\n", fullname)
#         filenames.append(fullname)
#
#     # parse elements in each XML file
#     for filename in filenames:
#         tree = ET.parse(filename)
#         root = tree.getroot()
#
#         extract_xml = []
#
#         ## extract child elements per xml file
#         print("\n")
#         for x in root.iter('Info'):
#             for element in x:
#                 print(element.tag, element.text)
#                 extract_xml.append(element.text)
#
#         ## Write list nodes to csv
#         csvwriter.writerow(extract_xml)
#
#     ## Close CSV file
#     xml_data_to_csv.close()

if __name__ == '__main__':
    main()
