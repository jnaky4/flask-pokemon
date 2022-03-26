import yaml
import types


def yaml_to_dict(filename: str) -> dict:
    """Will print the Yaml file
        Returns: Dict of Yaml File
    """
    with open(filename, "r") as stream:
        try:
            yaml_dict = yaml.safe_load(stream)
            # print(yaml_dict)
            return yaml_dict

        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    dict_of_yaml = yaml_to_dict("docker-compose.yaml")
    print(dict_of_yaml)
