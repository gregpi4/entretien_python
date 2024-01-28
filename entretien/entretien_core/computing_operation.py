from __future__ import annotations
from dataclasses import dataclass
from typing import List


class OperationType:
    VALUE = 0
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3


@dataclass
class OperationLine:
    operation_type: OperationType
    arg_1: str
    arg_2: str


class OperationStream:
    instance = None

    def __init__(self) -> None:
        self._all_operations = []
        self._index = 0
        self._all_answers = []

    @classmethod
    def get_instance(cls) -> OperationStream:
        if cls.instance is None:
            cls.instance = OperationStream()
        return cls.instance

    @property
    def number_of_operations(self) -> int:
        return len(self._all_operations)

    @property
    def has_value(self) -> bool:
        return self._index < len(self._all_operations)

    def get_value(self) -> OperationLine:
        value = self._all_operations[self._index]
        self._index += 1
        return value

    def __iter__(self) -> OperationStream:
        return self

    def __next__(self) -> OperationLine:
        # Implement your logic here to return the next value
        # and raise StopIteration when there are no more values
        # For example:
        if self.has_value:
            value = self.get_value()
            return value
        else:
            raise StopIteration

    def add_line_answer(self, result_line: int) -> None:
        self._all_answers.append(result_line)


class OperationStreamBuilder:
    def __init__(self) -> None:
        self._operation_stream = OperationStream.get_instance()
        self._expected_answers = []

    def add_value(self, value: str) -> OperationStreamBuilder:
        self._operation_stream._all_operations.append(
            OperationLine(OperationType.VALUE, value, "_")
        )
        return self

    def add_addition(self, arg_1: str, arg_2: str) -> OperationStreamBuilder:
        self._operation_stream._all_operations.append(
            OperationLine(OperationType.ADD, arg_1, arg_2)
        )
        return self

    def add_subtraction(self, arg_1: str, arg_2: str) -> OperationStreamBuilder:
        self._operation_stream._all_operations.append(
            OperationLine(OperationType.SUBTRACT, arg_1, arg_2)
        )
        return self

    def add_multiplication(self, arg_1: str, arg_2: str) -> OperationStreamBuilder:
        self._operation_stream._all_operations.append(
            OperationLine(OperationType.MULTIPLY, arg_1, arg_2)
        )
        return self

    def build(self) -> OperationStream:
        return self._operation_stream

    def __enter__(self) -> OperationStream:
        return self._operation_stream

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.verify_answers(self._operation_stream._all_answers)

    def verify_answers(self, answers: List[int]) -> None:
        if len(answers) != len(self._expected_answers):
            raise ValueError(
                f"Expected {len(self._expected_answers)} answers,"
                f"but got {len(answers)}."
            )

        for index in range(len(self._expected_answers)):
            if answers[index] != self._expected_answers[index]:
                raise ValueError(
                    f"Answer at index {index} is incorrect."
                    f"Expected {self._expected_answers[index]},"
                    f"but got {answers[index]}."
                )
