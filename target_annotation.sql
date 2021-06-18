/*
SQL command to isolate the the first three classes of the protein target (General --> Specific)
and the gene symbol.
*/
SELECT 
	cs.accession,
	pfc.l1 as Protein_Level1,
	pfc.l2 as Protein_Level2,
	pfc.l3 as Protein_Level3,
	tt.gene_name as Gene_Symbol
FROM 
	component_sequences cs,
	protein_classification pc,
	component_class cc,
	theoretical_targets tt,
	target_components tc,
	target_dictionary td,
	protein_family_classification pfc
WHERE 
	cs.accession IN ('UNIPROTid1')													/* or */
	cs.accession IN ('UNIPROTid1', 'UNIPROTid2', ...)								/* or */
	cs.accession IN (SELECT column_with_uniprot_ids FROM table_with_uniprot_ids)
AND cs.accession = tt.target_uniprot_id
AND cs.component_id = cc.component_id
AND cc.protein_class_id = pc.protein_class_id
AND cs.component_id = tc.component_id
AND pc.protein_class_id = pfc.protein_class_id
AND tc.tid = td.tid
AND td.target_type = 'SINGLE PROTEIN'
AND td.organism = 'Homo sapiens';