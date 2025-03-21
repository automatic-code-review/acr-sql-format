import argparse
import json
import os

import review

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--DIR', type=str, help='Dir')
    parser.add_argument('--CONFIG', type=str, help='Config')

    args = parser.parse_args()

    with open(args.CONFIG, 'r') as data:
        config = json.load(data)

    source_path = args.DIR
    regex_to_ignore = config['regexToIgnore']

    for root, dirs, files in os.walk(source_path):
        for file in files:
            if not file.endswith(".sql"):
                continue

            path = os.path.join(root, file)
            changed, new_data = review.verify(path=path, regex_to_ignore=regex_to_ignore)

            if changed:
                with open(path, "w") as data:
                    data.writelines(new_data)
