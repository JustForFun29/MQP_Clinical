from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship



class DiseaseTable(SQLModel, table=True):
    """
    This class is the disease table of the database. It contains the information
    about the diseases mentioned in the trials. It is the disease table of the database.
    Parameters
    ----------
    disease_name : str
        The name of the disease mentioned in the trial
    ntc_id : str
        The unique identifier of the trial
    """
    __tablename__ = "diseasetable"
    id: Optional[int] = Field(default=None, primary_key=True)
    disease_name: str = Field(unique=True)


class MainTable(SQLModel, table=True):
    """
    TO-DO: Add drug table to the schema
    This class is the main table of the database. It contains the information
    that is common to all the trials. It is the main table of the database.
    Parameters
    ----------
    nct_id : str
        The unique identifier of the trial
    brief_title : str
        The brief title of the trial
    official_title : str
        The official title of the trial
    org_study_id : str
        The original study identifier of the trial


    """
    __tablename__ = "maintable"
    id: Optional[int] = Field(default=None, primary_key=True)
    nct_id: str = Field(default=None)
    org_study_id: Optional[str] = Field(default=None)
    brief_title: Optional[str] = Field(default=None)
    official_title: Optional[str] = Field(default=None)
    overall_status: Optional[str] = Field(default=None)
    study_type: Optional[str] = Field(default=None)
    minimum_age: Optional[str] = Field(default=None)
    maximum_age: Optional[str] = Field(default=None)
    gender: Optional[str] = Field(default=None)
    criteria: Optional[str] = Field(default=None)
    intervention_model: Optional[str] = Field(default=None)
    primary_purpose: Optional[str] = Field(default=None)
    masking: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    phase: Optional[str] = Field(default=None)
    start_date: Optional[str] = Field(default=None)
    brief_summary: Optional[str] = Field(default=None)
    detailed_description: Optional[str] = Field(default=None)
    # drug_ids: List[int] = Field(default=None, foreign_key="drugtable.id", nullable=True)
    # disease_ids: List[int] = Field(default=None, foreign_key="diseasetable.id", nullable=True)
    # drug_id: Optional[int] = Field(default=None, foreign_key="drugtable.id", nullable=True)
    # disease_id: Optional[int] = Field(default=None, foreign_key="diseasetable.id", nullable=True)

class MainTableDrugRelationship(SQLModel, table=True):
    """
    This class represents the relationship between the main table and drug table.
    Each record represents a relationship between a MainTable entry, and a DrugTable entry.
    """
    __tablename__ = "maintable_drug_relationship"
    id: Optional[int] = Field(default=None, primary_key=True)
    main_table_id: str = Field(foreign_key="maintable.nct_id")
    drug_table_id: int = Field(foreign_key="drugtable.id")

class MainTableDiseaseRelationship(SQLModel, table=True):
    """
        This class represents the relationship between the main table and disease table.
        Each record represents a relationship between a MainTable entry, and a DiseaseTable entry.
    """
    __tablename__ = "maintable_disease_relationship"
    id: Optional[int] = Field(default=None, primary_key=True)
    main_table_id: str = Field(foreign_key="maintable.nct_id")
    disease_table_id: int = Field(foreign_key="diseasetable.id")


class DrugTable(SQLModel, table=True):
    # WIP!!!
    """
    This class is the drug table of the database. It contains the information
    about the drugs used in the trials. It is the drug table of the database.
    Parameters
    ----------
    nct_id : str
        The unique identifier of the trial
    drug_name : str
        The name of the drug used in the trial
    """
    __tablename__ = "drugtable"
    id: Optional[int] = Field(default=None, primary_key=True)
    drug_name: str = Field(unique=True)
    # main_table_id: Optional[int] = Field(default=None, foreign_key="main_table.id")



