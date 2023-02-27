from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


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
    id: Optional[int] = Field(default=None, primary_key=True)
    nct_id: str
    org_study_id: Optional[str] = Field(default=None)
    brief_title: Optional[str] = Field(default=None)
    official_title: Optional[str] = Field(default=None)
    overall_status: Optional[str] = Field(default=None)
    study_type: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    phase: Optional[str] = Field(default=None)
    start_date: Optional[str] = Field(default=None)
    brief_summary: Optional[str] = Field(default=None)
    detailed_description: Optional[str] = Field(default=None)
    # drug_id: Optional[int] = Field(default=None, foreign_key="drug.id")


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
    id: Optional[int] = Field(default=None, primary_key=True)
    nct_id: Optional[str] = Field(default=None, foreign_key="maintable.nct_id")
    drug_name: str
    # main_table_id: Optional[int] = Field(default=None, foreign_key="main_table.id")
