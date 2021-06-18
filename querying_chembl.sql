/* 
SQL command to isolate:
 -Compounds that interact with targets of interest to an extent that the user can select
 or
 -Targets that compounds of interest interact with to an extent that the user can select
*/
SELECT
    md.chembl_id as Compound_Chembl_id,
    cs.accession as Target_Uniprot_id,
    vs.mutation as Target_Mutation,                                                 /* When querying gene mutations */
    act.standard_type as Bioactivity_Type,
    act.standard_relation as Bioactivity_Relation,
    act.standard_value as Bioactivity_Value,
    act.standard_units as Bioactivity_Units
FROM 
    molecule_dictionary md,
    activities act,
    assays ass,
    target_dictionary td,
    target_components tc,
    component_sequences cs,
    variant_sequences vs                                                            /* When querying gene mutations */
WHERE
    md.molregno=act.molregno
AND ass.assay_id=act.assay_id
AND ass.tid=td.tid
AND td.tid=tc.tid
AND tc.component_id=cs.component_id
AND ass.variant_id IS NOT null                                                      /* When querying gene mutations (combine with next line) */
AND ass.variant_id = vs.variant_id            
AND ass.variant_id IS null                                                          /* When querying wild types */
AND td.organism = 'Homo sapiens'
AND td.target_type = 'SINGLE PROTEIN'                                               
AND md.chembl_ID IN (SELECT column_with_chembl_ids FROM table_with_chembl_ids)      /* When querying to find target */
AND cs.accession IN (SELECT column_with_uniprot_ids FROM table_with_uniprot_ids)    /* When querying to find compounds */
AND standard_type IN ('IC50','Ki', 'EC50', 'Kd')
AND standard_units = 'nM'