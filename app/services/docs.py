import typing as t
Json = dict[str | t.Literal["anyOf", "type"], "Json"] | list["Json"] | str | bool

# Workaround for azure api management not accepting openAPI 3.1.0 given here:
# https://github.com/tiangolo/fastapi/discussions/9789#discussioncomment-8629746
def convert_openapi_3_1_to_3_0(json: dict[str, Json]):
    """Will attempt to convert version 3.1.0 of some openAPI json into 3.0.2

    Usage:

        >>> from pprint import pprint
        >>> json = {
        ...     "some_irrelevant_keys": {...},
        ...     "nested_dict": {"nested_key": {"anyOf": [{"type": "string"}, {"type": "null"}]}},
        ...     "examples": [{...}, {...}]
        ... }
        >>> convert_openapi_3_1_to_3_0(json)
        >>> pprint(json)
        {'example': {Ellipsis},
         'nested_dict': {'nested_key': {'anyOf': [{'type': 'string'}],
                                        'nullable': True}},
         'openapi': '3.0.2',
         'some_irrelevant_keys': {Ellipsis}}
    """
    json["openapi"] = "3.0.1"

    def inner(yaml_dict: Json):
        if isinstance(yaml_dict, dict):
            if "anyOf" in yaml_dict and isinstance((anyOf := yaml_dict["anyOf"]), list):
                for i, item in enumerate(anyOf):
                    if isinstance(item, dict) and item.get("type") == "null":
                        anyOf.pop(i)
                        yaml_dict["nullable"] = True
            if "examples" in yaml_dict:
                examples = yaml_dict["examples"]
                del yaml_dict["examples"]
                if isinstance(examples, list) and len(examples):
                    yaml_dict["example"] = examples[0]
            # Jank will need to do this for each
            if "exclusiveMinimum" in yaml_dict:
                yaml_dict["exclusiveMinimum"] = bool(yaml_dict["exclusiveMinimum"])
            for value in yaml_dict.values():
                inner(value)
        elif isinstance(yaml_dict, list):
            for item in yaml_dict:
                inner(item)

    inner(json)