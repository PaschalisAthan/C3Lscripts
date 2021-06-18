import pandas as pd
import requests
from opentargets import OpenTargetsClient
ot = OpenTargetsClient()

'''
This python script is used to match a target list with diseases the targets are associated with.
As input, a list of target Uniprot ids is required.
'''

with open(input_file.csv, 'r') as f_in, open(output_file.csv, 'a') as f_out:
	f_out.write('Target ID' + '\t' + 'Gene Name' + '\t' + 'Association score' + '\t' + 'Disease Name' + '\n')
	df = pd.read_csv(f_in, delimiter = ',', lineterminator = '\n', header = 0)
	all_targs = df['target_uniprot_id'].tolist()
	for i in all_targs:
		targ_name = []
		dis_type_in = []
		dis_type = []
		dis_name = []
		asso_score = []
		final_list = []
		final_list_all = []
		asso_scores = []
		direct = []
		# dis_interest = ['cell proliferation disorder']       							 ## Uncomment if interested in a specific disease	
		a_for_target = ot.get_associations_for_target(i)

		for a in a_for_target:
			targ_name.append(a['target']['gene_info']['symbol'])
			dis_type.append(a['disease']['efo_info']['therapeutic_area']['labels'])
			dis_name.append(a['disease']['efo_info']['label'])
			direct.append(str(a['is_direct']))
			asso_score.append(a['association_score']['overall'])
		for k in range(len(targ_name)):
			if asso_score[k] > 0.5 and direct[k] == 'True':								## Association score can be changed here
				final_list.append(dis_name[k])
				asso_scores.append(str(asso_score[k]))
			
		for l,p in zip(final_list, asso_scores):
			f_out.write(i +'\t' + targ_name[0] + '\t'+ p +'\t'+ l + '\n')
