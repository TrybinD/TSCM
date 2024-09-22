from abc import ABC, abstractmethod

from src.data.problem import Problem
from src.data.solution import Solution


class BaseSolver(ABC):

    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        raise NotImplementedError