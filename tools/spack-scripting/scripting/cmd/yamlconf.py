import os
import yaml
import fastjsonschema


class YamlConf:
    parameters_ = []

    def __init__(self, yaml_file, yaml_schema):
        cwd = os.getcwd()
        self.yaml_file_ = yaml_file
        with open(self.yaml_file_, 'r') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            self.parameters_ = yaml.load(file, Loader=yaml.FullLoader)

        with open(yaml_schema, 'r') as file:
            self.schema = fastjsonschema.compile(
                yaml.load(file, Loader=yaml.FullLoader))

        print("validating yaml",yaml_file, "against schema",yaml_schema," ...")
        data = self.schema(self.parameters_)
        print("yaml schema valid!")

    def __getitem__(self, key):
        return self.parameters_[key]

    def __setitem__(self, key, value):
        self.parameters_[key] = value

    def yaml_dump(self):
        return yaml.dump(self.parameters_)

    def serialize(self):
        with open(self.yaml_file_, 'w') as file:
            file.write(self.yaml_dump())

    def __str__(self):
        return self.yaml_dump()
