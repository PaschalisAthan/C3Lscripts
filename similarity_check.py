from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem import MACCSkeys
from itertools import product

'''
This python script compares a list of compounds to themselves and calculates the similarity between all the possible combinations of compounds.
The format of the input file should have any type of identifier as first column and the second column should have the canonical SMILES of the compound.
PySpark is used to make the procedure faster.
'''

# File input
def parseLine(line):
    fields = line.split(',')
    chem_id = fields[0]
    canonical_smiles = fields[1]
    return (chem_id, canonical_smiles)

# Compound fingerprint calculation
def transform(smile):
	m1 = Chem.MolFromSmiles(smile[1])
	fp = AllChem.GetMorganFingerprint(m1,2)   						## ECFP4 fingerprint
	# fp = AllChem.GetMorganFingerprint(m1,3)   					## ECFP6 fingerprint
	# fp = MACCSkeys.GenMACCSKeys(m1)   							## MACCS keys fingerprint
	return (smile[0], fp)

# Fingerprint comparison
def dice(tpl):
	sim = DataStructs.DiceSimilarity(fp1,fp2) 						## ECFP4/6 fingerprints
	# sim = DataStructs.FingerprintSimilarity(tpl[0][1],tpl[1][1]) 	## MACCS keys fingerprint
	return (tpl[0][0], tpl[1][0], sim)


conf = SparkConf().setMaster("local").setAppName("Similarity")
sc = SparkContext(conf = conf)

sqlContext = SQLContext(sc)

lines = sc.textFile(input_file.csv)
all_data = lines.map(parseLine)

similarity = all_data.map(transform)
similarity_copy = similarity

cartesian = similarity.cartesian(similarity_copy)

sims = cartesian.map(dice)
sims.take(2)

df = sqlContext.createDataFrame(sims,['id1', 'id2', 'ECFP4'])   	## ECFP4 fingerprint
# df = sqlContext.createDataFrame(sims,['id1', 'id2', 'ECFP6'])   	## ECFP6	fingerprint
# df = sqlContext.createDataFrame(sims,['id1', 'id2', 'MACCS'])   	## MACCS keys fingerprint

df.write.option("sep", ",").option("header", "true").csv(output_folder_name)






