import json


def require_dot(descr):
    if descr != "" and not descr.endswith("."):
        descr += "."
    return descr


def add_array(name, prop, md, indent, schema):
    items = prop['items']
    descr = prop.get("description", "")
    descr = require_dot(descr)
    if isinstance(items, dict):  # case dict

        def _add_items(items, md):
            if 'type' in items:
                type_ = items['type']
                if type_ in ('boolean', 'string', 'number', 'integer', 'object', 'array'):
                    line = f"{indent}- `{name}`: {descr} Contains a list of {items['type']}s.\n"
                    md += line
                else:
                    assert False, f"Giving up for items {items}"
            elif "oneOf" in items:
                assert len(items) == 1
                line = f"{indent}- `{name}`: {descr} Contains a list with items of exactly one of:\n"
                md += line
                one_of = items["oneOf"]
                md = add_one_of(one_of, md, indent, schema)
            elif "anyOf" in items:
                assert len(items) == 1
                line = f"{indent}- `{name}`: {descr} Contains a list with items:\n"
                md += line
                any_of = items["anyOf"]
                md = add_any_of(any_of, md, indent + "\t", schema)
            else:
                assert False, f"Giving up for items {items}"
            return md

        if "$ref" in items:
            items = get_reference(items['$ref'], schema)
            md = _add_items(items, md)
        else:
            md = _add_items(items, md)

    else:  # case list
        tuple_ = ", ".join(item["type"] for item in items)
        line = f"{indent}- `{name}`: {descr} Contains a tuple of [{tuple_}].\n"
        md += line
    return md


def get_external_link(reference):
    reference = reference.lstrip("#")
    reference = reference.split("/")
    if reference[0] == '':
        reference = reference[1:]

    # don't follow external references
    if reference[0].startswith('http'):
        reference = reference[-1].split('.')[0]
    else:
        reference = None
    return reference


def get_reference(reference, schema):
    reference = reference.lstrip("#")
    reference = reference.split("/")
    if reference[0] == '':
        reference = reference[1:]
    link = schema
    for ref in reference:
        link = link[ref]
    return link


def follow_reference(name, reference, md, indent, schema):
    reference = reference.lstrip("#")
    reference = reference.split("/")
    if reference[0] == '':
        reference = reference[1:]

    # don't follow external references
    if reference[0].startswith('http'):
        reference = reference[-1].split('.')[0]
        line = f"{indent}- `{name}`: Contains a [{reference}](#{reference}-metadata).\n"
        md += line
        return md

    link = schema
    for ref in reference:
        link = link[ref]
    md = add_field(name, link, md, indent, schema)
    return md


def add_field(name, prop, md, indent, schema):
    type_ = prop.get("type")
    if type_ == "object":
        md = add_obj(name, prop, md, indent, schema)
    elif type_ == "array":
        md = add_array(name, prop, md, indent, schema)
    elif "$ref" in prop:
        md = follow_reference(name, prop["$ref"], md, indent, schema)
    else:
        descr = prop.get("description", "")
        descr = require_dot(descr)
        line = f"{indent}- `{name}`: {descr}\n"
        md += line
    return md


def add_props(props, md, indent, schema):
    props = {k: props[k] for k in sorted(props.keys())}
    for name, prop in props.items():
        md = add_field(name, prop, md, indent, schema)
    return md


def add_one_of(one_of, md, indent, schema, anon=False):
    for item in one_of:
        if anon:
            tab = ""
        else:
            md += f"{indent}- \n"
            tab = "\t"
        md = add_props(item['properties'], md, indent + tab, schema)
    return md


def add_any_of(any_of, md, indent, schema):
    for item in any_of:
        md = add_field("", item, md, indent, schema)
    return md


def add_obj(name, obj, md, indent, schema):
    descr = obj.get("description", "")
    descr = require_dot(descr)

    required = obj.get('required', [])

    anonymous = name == ''
    line = f"`{name}`: {descr}"

    additional = obj.get('additionalProperties', None)
    if isinstance(additional, dict):
        additional_type = get_external_link(additional["$ref"])
        assert additional_type is not None
        line += f" Contains fields of type [{additional_type}](#{additional_type}-metadata)."

    if required:
        required = [f'`{req}`' for req in required]
        if len(required) == 1:
            line += f" The field {required[0]} is required."
        else:
            required = ', '.join(required[:-1]) + f" and {required[-1]}"
            line += f" The fields {required} are required."

    if not anonymous:
        line = f"{indent}- " + line
        indent += "\t"

    # check the properties of this object:
    props = obj.get("properties", None)
    if props is None:  # irregular cases

        # check if we have a "oneOf"
        one_of = obj.get("oneOf")
        if one_of is not None:
            line += "Must contain exactly one of the following items:\n"
            if not anonymous:
                md += line
            md = add_one_of(one_of, md, indent, schema, anonymous)
        else:
            if not anonymous:
                md += (line + "\n")

    else:  # regular case with properties
        if not anonymous:
            md += (line + "\n")
        md = add_props(props, md, indent, schema)

    return md


def schema_to_markdown(schema):
    with open(schema) as f:
        schema = json.load(f)
    md = ""
    indent = ""
    md = add_obj("", schema, md, indent, schema)
    return md


if __name__ == '__main__':
    # md = schema_to_markdown('../schema/project.schema.json')
    # md = schema_to_markdown('../schema/dataset.schema.json')
    # md = schema_to_markdown('../schema/source.schema.json')
    md = schema_to_markdown('../schema/view.schema.json')
    print(md)
