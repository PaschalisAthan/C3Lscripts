/*
SQL command to isolate the compound name if applicable, the max phase of the compound 
(0=Preclinical, 1=Investigational(Ph1),2=Investigational(Ph2), 3=Investigational(Ph3), 4=Approved),
and the canonical smiles of the compound.
*/
SELECT
	md.chembl_id as ChEMBL_id,
	md.pref_name as Compound,
	md.max_phase as Status,
	cs.canonical_smiles as SMILES
FROM
	molecule_dictionary md,
	compound_structures cs
WHERE
	md.molregno = cs.molregno
AND md.chembl_id = 'CHEMBLXX1'														/* or */
AND md.chembl_id IN ('CHEMBLXX1', 'CHEMBLXX2', ...)									/* or */
AND md.chembl_id IN (SELECT column_with_chembl_ids FROM table_with_chembl_ids);