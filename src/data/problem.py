


from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class Problem:
    operations_matrix: pd.DataFrame
    distances_matrix: pd.DataFrame
    times_matrix: pd.DataFrame
    costs_matrix: pd.DataFrame
    productivity: pd.Series
    distances_coef: float

    @classmethod
    def from_dataset(cls, 
                     number: int, 
                     operations: int, 
                     sub_operations: int, 
                     cities: int, 
                     distances_coef: float = 0.3, 
                     sheet_name: Optional[str] = None):
        
        if sheet_name is None:
            sheet_name = f"{operations},{sub_operations},{cities}-{number}"

        operations_matrix = pd.read_excel("../data/DataSets.xlsx", 
                                          sheet_name=sheet_name, 
                                          header=4, 
                                          index_col=0, 
                                          usecols=list(range(operations+1)), 
                                          nrows=sub_operations)
        
        distances_matrix = pd.read_excel("../data/DataSets.xlsx", 
                                         sheet_name=sheet_name, 
                                         header=8+sub_operations, 
                                         index_col=0, 
                                         usecols=list(range(cities+1)), 
                                         nrows=cities)
        
        times_matrix = pd.read_excel("../data/DataSets.xlsx", 
                                     sheet_name=sheet_name, 
                                     header=12+sub_operations+cities, 
                                     index_col=0, 
                                     usecols=list(range(cities+1)), 
                                     nrows=sub_operations)
        
        costs_matrix = pd.read_excel("../data/DataSets.xlsx", 
                                     sheet_name=sheet_name, 
                                     header=16+2*sub_operations+cities, 
                                     index_col=0, 
                                     usecols=list(range(cities+1)), 
                                     nrows=sub_operations)
        
        productivity = pd.read_excel("../data/DataSets.xlsx", 
                                     sheet_name=sheet_name, 
                                     header=20+3*sub_operations+cities, 
                                     usecols=list(range(cities)), 
                                     nrows=1).iloc[0]
        
        return Problem(operations_matrix=operations_matrix, 
                       distances_matrix=distances_matrix,
                       times_matrix=times_matrix, 
                       costs_matrix=costs_matrix,
                       productivity=productivity, 
                       distances_coef=distances_coef)
    

    @classmethod
    def from_example(cls): 
        return Problem.from_dataset(0, 5, 10, 10, 0.3, sheet_name="example")
