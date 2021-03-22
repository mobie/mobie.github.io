import subprocess
from schema_to_markdown import schema_to_markdown


def describe(name):
    with open(f'../specs/template_{name}.md') as f:
        md = f.read()
    md += "\n"
    return md


# TODO expose arguments to make autogenerated example nicer
def generate_example(schema):
    cmd = ['fake-schema', schema]
    result = subprocess.run(cmd, capture_output=True)
    example = result.stdout.decode('utf-8')
    err = result.stderr.decode('utf-8')

    if err:
        print("WARNING: example could not be generated for schema", schema, "due to the following error:")
        print(err)
        print("Skipping this example")
        return "\n"

    return example


def describe_and_generate(name):
    with open(f'../specs/template_{name}.md') as f:
        md = f.read()
    schema_file = f'../schema/{name}.schema.json'
    schema = schema_to_markdown(schema_file)
    md += schema
    md += "\n"
    md += "```json\n"
    md += generate_example(schema_file)
    md += "```\n"
    md += "\n"
    return md


def generate_spec_description(out_path):

    # project and dataset are short and probably not changing much,
    # so for now we don't autogenerate the schema description for them
    md = describe("project")
    md += describe("dataset")

    # source and view schema descriptions are autogenerated
    # FIXME autogenerating the example for source fails
    md += describe_and_generate("source")
    md += describe_and_generate("view")

    with open(out_path, 'w') as f:
        f.write(md)


if __name__ == '__main__':
    out_path = '../specs/mobie_spec.md'
    generate_spec_description(out_path)