import json
import yaml


def file_print(i_file):
    with open(i_file) as f:
        print(f.read())


class FileConverter:

    def __init__(self):
        super().__init__()

    @staticmethod
    def put(x, o_file):
        with open(o_file, 'w') as f:
            f.write(x)

    def json2yml(self, i_file, o_file):
        with open(i_file) as f:
            self.put(yaml.safe_dump(json.load(f), default_flow_style=False, indent=4), o_file)

    def yml2json(self, i_file, o_file):
        with open(i_file) as f:
            self.put(json.dumps(yaml.safe_load(f), indent=4), o_file)


converter = FileConverter()

converter.json2yml("tspec.json", "tspec.yml")
# conv.yml2json("f2.yml", "f2.json")
