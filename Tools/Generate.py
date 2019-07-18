import numpy as np
import matplotlib.pyplot as plt
import h5py
import cPickle

# creating the hdf5 file
target = h5py.File("../CRDB.hdf5", 'w')

# key list for experiments
Experiments = ["AUG09", "AUG11", "GAM", "HIRES1MONO", "HIRES2MONO", "HIRSTEREO", "HIRESMIA", "ICE", "KASQGS",
               "KASSIBYLL",
               "TA", "TIBETIII1", "TIBETIII2", "TIBETIII3", "TUNKA", "CAS", "KAS05", "GRANQGS2", "AGA03", "AMS", "ATIC",
               "PAMELA", "PAMELA_CATO", "CREAM", "BESS", "TUNKA_Prelim", "CAPRICE98_p", "CAPRICE98_He"]
LegendNames = ["Auger (2009)", "Auger (2011)", "GAMMA", "HiRes-I Mono", "HiRes-II Mono", "HiRes-II Stereo", "HiRes/MIA",
               "IceTop", "Kascade (QGSJet)", "Kascade (Sibyll)",
               "Telecope array", "TibetIII (QGSJet+HD)", "TibetIII (QGSJet+PD)", "TibetIII (Sibyll+HD)", "Tunka133",
               "Casa MIA", "Kascade (2005)", "KASCADE Grande (QGSJet2)",
               "AGASA (2003)", "AMS (2000) [p]", "ATIC (2009)", "PAMELA (2011) [p]", "PAMELA Cato (2013) [p]",
               "CREAM (2011) [p]", "BESS (2015) [p]", "TUNKA_Prelim (2010)", "CAPRICE (1998) [p]",
               "CAPRICE (1998) [He]"]
BibTexNames = ["CRDB_AUG09", "CRDB_AUG11", "CRDB_GAM", "CRDB_HiRes", "CRDB_HiRes", "CRDB_HiRes", "CRDB_HiResMIA",
               "CRDB_ICE", "CRDB_KASKADE", "CRDB_KASKADE",
               "CRDB_TA", "CRDB_TibetIII", "CRDB_TibetIII", "CRDB_TibetIII", "CRDB_Tunka", "CRDB_CasaMIA",
               "CRDB_KASCADE05", "CRDB_Grande", "CRDB_AGA03", "CRDB_AMS", "CRDB_ATIC",
               "CRDB_PAMELA", "CRDB_PAMELA_CATO,", "CRDB_CREAM", "CRDB_BESS", "CRDB_TUNKA_Prelim", "CRDB_CAPRICE98",
               "CRDB_CAPRICE98"]

LegendDict = dict(zip(Experiments, LegendNames))
BibTexDict = dict(zip(Experiments, BibTexNames))

DataBase = {}

# filling the database with data and metadata
for n in Experiments:
    group = target.create_group(n)
    data = np.genfromtxt("../Data/" + n + '.txt', names=True, dtype=float)
    DATA = {"E": 0, "F": 0, "F_stat": 0, "F_low": 0, "F_up": 0, "NOE": 0}
    METADATA = {"Legend": 0, "Cite": 0}

    for x in DATA.keys():
        try:
            DATA[x] = data[x]
        except:
            DATA[x] = np.zeros(len(data['E']))
            print "no " + x + " available"

    METADATA["Legend"] = LegendDict[n]
    METADATA["Cite"] = BibTexDict[n]
    DataBase[n] = {"DATA": DATA, "METADATA": METADATA}

    results = np.column_stack((DATA['E'], DATA['F'], DATA['F_up'], DATA['F_low'], DATA['F_stat'], DATA['NOE']))
    group.create_dataset('data', data=results)
    group.attrs["Legend"] = unicode(LegendDict[n])
    group.attrs["Cite"] = unicode(BibTexDict[n])

with open("../CRDB.ppd", 'w') as f:
    cPickle.dump(DataBase, f)

target.close()
