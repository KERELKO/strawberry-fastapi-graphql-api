from strawberry.types.nodes import Selection
from strawberry.utils.str_converters import to_snake_case

from src.core.dto import SelectedFields


class BaseStrawberryResolver:
    @classmethod
    def _selections_to_strings(
        cls,
        fields: list[Selection],
        remove_related: bool = True,
    ) -> list[str]:
        list_fields: list[str] = []
        for field in fields:
            if remove_related:
                if not field.selections:
                    list_fields.append(to_snake_case(field.name))
            else:
                if not field.selections:
                    list_fields.append(to_snake_case(field.name))
                    continue
                for related_field in field.selections:
                    list_fields.append(f'{field.name}.{related_field.name}')
        return list_fields

    @classmethod
    def _selections_to_selected_fields(
        cls,
        fields: list[Selection],
        remove_related: bool = False,
    ) -> list[SelectedFields]:
        result: list[SelectedFields] = []
        for field in fields:
            if field.selections:
                obj = SelectedFields(owner=field.name.lower())
                for selection in field.selections:
                    if selection.selections:
                        if remove_related:
                            continue
                        result.extend(
                            cls._selections_to_selected_fields([selection], remove_related=False)
                        )
                    else:
                        obj.fields.append(selection.name)
                result.append(obj)
        return result
