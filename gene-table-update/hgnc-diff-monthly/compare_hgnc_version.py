old_genes = {}
with open("nov_2021_ids.txt", "r") as _old_input:
	_headers = _old_input.readline().rstrip('\r').split('\t')
	for _line in _old_input:
		_items = _line.rstrip('\r').split('\t')
		old_genes[_items[0]] = {
			"symbol": _items[1],
			"type": _items[2],
			"include_in_new": "false"
		}	
	
updated_cnt = 0
updated_protein_coding_cnt = 0
new_cnt = 0
new_protein_coding_cnt = 0
remove_cnt = 0
removed_protein_coding_cnt = 0
output_file = open("diff_hgnc.txt", "w")
output_update_line = ""
output_new_line = ""
output_del_line = ""


with open("dec_2021_ids.txt", "r") as _new_input:
	_headers = _new_input.readline().rstrip('\r').split('\t')
	for _line in _new_input:
		_items = _line.rstrip('\r').split('\t')
		if _items[0] in old_genes.keys():
			if _items[1] == old_genes[_items[0]]["symbol"] and _items[2] == old_genes[_items[0]]["type"]:
				old_genes[_items[0]]["include_in_new"] = "true"
			else: 
				old_genes[_items[0]]["include_in_new"] = "updated"
				output_update_line = output_update_line + old_genes[_items[0]]["symbol"] + "\t" + old_genes[_items[0]]["type"].strip() + " >>>>> " + _items[1] + "\t" + _items[2]
				updated_cnt = updated_cnt + 1
				if _items[2].strip() == "gene with protein product":
					updated_protein_coding_cnt = updated_protein_coding_cnt + 1
		else:
			output_new_line = output_new_line + _items[0] + "\t" + _items[1] + "\t" + _items[2]
			new_cnt = new_cnt + 1
			if _items[2].strip() == "gene with protein product":
				new_protein_coding_cnt = new_protein_coding_cnt + 1

for _old_key in old_genes.keys():
	if old_genes[_old_key]["include_in_new"] == "false":
		output_del_line = output_del_line + _old_key + "\t" + old_genes[_old_key]["symbol"] + "\t" + old_genes[_old_key]["type"]
		remove_cnt = remove_cnt + 1
		if old_genes[_old_key]["type"].strip() == "gene with protein product":
			removed_protein_coding_cnt = removed_protein_coding_cnt + 1			

output_file.write("Added " + str(new_cnt) + " Genes" + " (" + str(new_protein_coding_cnt) + " protein coding)\n")
output_file.write(output_new_line)

output_file.write("Updated " + str(updated_cnt) + " Genes" + " (" + str(updated_protein_coding_cnt) + " protein coding)\n")
output_file.write(output_update_line)

output_file.write("Removed " + str(remove_cnt) + " Genes" + " (" + str(removed_protein_coding_cnt) + " protein coding)\n")
output_file.write(output_del_line)

output_file.close()



