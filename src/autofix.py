import argparse
import json

import review

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--PATH', type=str, help='Path')
    parser.add_argument('--CONFIG', type=str, help='Config')

    args = parser.parse_args()

    with open(args.CONFIG, 'r') as data:
        config = json.load(data)

    path = args.PATH

    if not path.endswith(".sql"):
        raise Exception("extension type not supported")

    changed, new_data = review.verify(path=path, regex_to_ignore=config["regexToIgnore"])

    if changed:
        with open(path, "w") as data:
            data.writelines(new_data)
