"""FieldInputModel - represents field input data."""

from dataclasses import dataclass, field


@dataclass
class FieldInputModel:
    """
    Represents field input data for form filling operations.

    Equivalent to Java class:
        public class FieldInputModel {
            protected Map<String, String> fieldInputData = new HashMap<>();
            public Map<String, String> getFieldInputData() { return fieldInputData; }
        }

    Attributes:
        field_input_data: A dictionary mapping field names to their input values
    """
    field_input_data: dict[str, str] = field(default_factory=dict)

    def get_field_input_data(self) -> dict[str, str]:
        """
        Get the field input data.

        Returns:
            Dictionary of field names to their input values
        """
        return self.field_input_data

