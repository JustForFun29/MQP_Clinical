import os
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from sqlite3 import IntegrityError
from typing import List

from xml_parser import *
from pathlib import Path
from pprint import PrettyPrinter
from sqlmodel import  Session, SQLModel, create_engine

pp = PrettyPrinter(indent=2)
engine = create_engine("sqlite:///MQP-Clinical-Trials")
SQLModel.metadata.create_all(engine)



def traverse_folders():
    path = "/Users/Dimas/PycharmProjects/MQP_Clinical/archive"
    filelist = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith('.xml'):
                continue
            filelist.append(os.path.join(root, file))


    # REAL CODE IN HERE - FOR MAIN TABLE

    for file in filelist:
        dict0 = extract_xml(file)
        CTPdict = main_schema_dict(dict0)
        if CTPdict is None:
            continue

        # print(dict0)
        print(CTPdict)


        drug_ids = []
        try:
            drug_names = CTPdict.pop("drugs")
            with Session(engine) as session:
                if type(drug_names) == list:
                    for drug_name in drug_names:
                        drug = session.query(DrugTable).filter_by(drug_name=drug_name).first()
                        if drug is not None:
                            drug_ids.append(drug.id)
                else:
                    drug = session.query(DrugTable).filter_by(drug_name=drug_names).first()
                    if drug is not None:
                        drug_ids.append(drug.id)
            print(f'{CTPdict["nct_id"]} - drugs ids are: {drug_ids}')
        except KeyError:
            print(f'{CTPdict["nct_id"]} - no drugs found in that xml file')

        disease_ids = []
        try:
            disease_names = CTPdict.pop("diseases")
            with Session(engine) as session:
                if type(disease_names) == list:
                    for disease_name in disease_names:
                        disease = session.query(DiseaseTable).filter_by(disease_name=disease_name).first()
                        if disease is not None:
                            disease_ids.append(disease.id)
                else:
                    disease = session.query(DiseaseTable).filter_by(disease_name=disease_names).first()
                    if disease is not None:
                        disease_ids.append(disease.id)
            print(f'{CTPdict["nct_id"]} - disease ids are: {disease_ids}')
        except KeyError:
            print(f'{CTPdict["nct_id"]} - no diseases found in that xml file')

        # add MainTable entry with drug and disease ids
        CTPentry = MainTable(**CTPdict)
        with Session(engine) as session:
            session.add(CTPentry)
            session.flush()  # flush the session to ensure the CTPentry.id attribute is populated
            # print(CTPentry)
            print(f"\nAdded {file} with id {CTPentry.nct_id}")
            if drug_ids:
                for drug_id in drug_ids:
                    relationship = MainTableDrugRelationship(main_table_id=CTPentry.nct_id, drug_table_id=drug_id)
                    session.add(relationship)

            if disease_ids:
                for disease_id in disease_ids:
                    relationship = MainTableDiseaseRelationship(main_table_id=CTPentry.nct_id, disease_table_id=disease_id)
                    session.add(relationship)

            session.commit()


    # REAL CODE FOR DRUGS AND DISEASES DATABASE

    for i in filelist:
        dict0 = extract_xml(i)

        if dict0 is None:
            continue
        disease_entry = disease_schema_dict(dict0)
        with Session(engine) as session:
            for entry in disease_entry:
                disease = session.query(DiseaseTable).filter_by(disease_name=entry["disease_name"]).first()
                if not disease:
                    try:
                        disease = DiseaseTable(disease_name=entry["disease_name"])
                        session.add(disease)
                        session.commit()
                    except IntegrityError:
                        session.rollback()
                        disease = session.query(DiseaseTable).filter_by(disease_name=entry["disease_name"]).first()
        print(f"\n Added {i}")

        for drug_entry in drug_schema_dict(dict0):
            with Session(engine) as session:
                drug = session.query(DrugTable).filter_by(drug_name=drug_entry['drug_name']).first()
                if drug is None:
                    # add new drug to database
                    drug = DrugTable(drug_name=drug_entry['drug_name'])
                    session.add(drug)
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
