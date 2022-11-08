from pathlib import Path
import json
import os
'''
explore_directory() takes the path to a directoy as an argument
and enumarates the subdirectories. Files within the directory are
ignored. Returns a list of names of the subdirectories.
'''
def explore_directory(directory_path: str) -> [str]:
	d = Path(directory_path)
	if d.is_dir():
		print( [p.name for p in d.iterdir() if p.is_dir()])
		return [p.name for p in d.iterdir() if p.is_dir()]
	else:
		print("Error - the given path does not point to a directory")

'''
parse_enumeration() takes the list of folder names enumarated by
the explore_directory function. The folder names follow a specific
format: #_englishname_chinesename
where # represents the folder number and is required
where englishname represents the english name and is required
where chinesename represents the chinese name and is NOT required
each parameter is seperated by a single '_' character
'''
def parse_enumeration(e_list: [str]) -> {str : [str]}:
	parsed = dict()
	for folder_name in e_list:
		components = folder_name.split('_')
		if components[0].isdigit()==False:
			continue 
		parsed.update({components[0] : components[1:]})
	return parsed

'''
write_json_to_file() takes the output of parse_enumeration() and
writes to a json file with the specified name.
'''
def write_json_to_file(e_dict: dict, filename: str) -> None:
	with open(os.path.dirname(os.path.realpath(__file__))+"/"+filename, 'w') as out:
		json.dump(e_dict, out, ensure_ascii=False)

if __name__ == '__main__':
	write_json_to_file(parse_enumeration(explore_directory(os.path.dirname(os.path.realpath(__file__)))), 'folder.json')
