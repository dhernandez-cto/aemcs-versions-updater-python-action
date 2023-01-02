import yaml
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file',help="Path to file")
parser.add_argument("name",help="AEMCS site module name to be modified or added")
parser.add_argument("tag",help="The module Git tag (version)")
parser.add_argument("sha", help="The commit hash")
parser.add_argument("url", help="The Git repository url where the module is stored")

args = parser.parse_args()

try: 
  with open(args.file,'r') as versions_file:
    modules=yaml.safe_load(versions_file)
except FileNotFoundError:
    sys.stdout.write(f"File {args.file} not found! It will be created\n")
    modules = {}

print(f"Current {args.file} content: ", yaml.dump(modules))

new_values = dict(tag=args.tag, sha=args.sha, url=args.url)
if args.name in modules:
    print(f"Module {args.name} found in {args.file} with values {modules[args.name]}, updating to {new_values}")
else:
    print(f"Module {args.name} not found in {args.file}, adding new entry for", {args.name:new_values})

modules.update({args.name:new_values})

with open(args.file, 'w') as outfile:
    yaml.dump(modules, outfile, default_flow_style=False)
