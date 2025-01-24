from samplesheetutils.utils.input import *
import csv, yaml, json

def create_csv(data, header_seq, header_fasta, fp):
    fp.write(f"{header_seq},{header_fasta}\n")
    for row in data:
        fp.write(sanitize_input(row.name) + "," + row.path + "\n")
    fp.flush()

def create_yaml_boltz(data, fp):
    output_data = {
        "version": 1,
        "sequences": []
    }
    for row in data:
        append_data = {"protein": {
            "id": row.name[:min(4,len(row.name))],
            "sequence": row.data
        }}
        if row.msa:
            append_data["protein"]["msa"] = row.msa
        #output_data["sequences"].append({"protein": {
        #    "id": row.name[:min(4,len(row.name))],
        #    "sequence": row.data
        #}})
        output_data["sequences"].append(append_data)

    yaml.dump(output_data, fp, default_flow_style=False)

def create_json(data, fp):
    dict_data = {"entities": []}

    for row in data:
        dict_data["entities"].append({"type": "protein", "sequence": row.data, "count": "1"})

    json.dump(dict_data, fp)
    fp.flush()

