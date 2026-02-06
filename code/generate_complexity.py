import os
import numpy as np
import csv
from collections import defaultdict
from pycldf import Dataset

ds = Dataset.from_metadata("../cosinus/cldf/cldf-metadata.json")

forms = ds.objects("FormTable")
languages = ds.objects("LanguageTable")
concepts = ds.objects("ParameterTable")

table = []
for form in map(lambda x: x.data, forms):
    language, concept = languages[form["Language_ID"]].data, concepts[form["Parameter_ID"]].data
    table += [[form["ID"], language["Name"], language["Glottocode"], concept["Number"],
                  " + ".join(form["Surface_Form"]), 
                  " + ".join(form["Underlying_Form"]), 
                  " ".join(map(lambda x: str(x), form["Cognates"])),
                  " ".join(form["Morphemes"])]]

languages = sorted(set([l[1] for l in table]))

#all_morphemes = sorted(set([s for l in table for s in l[7].split()]))

morphemes_to_keep = ['-ty', '-ty-', 'eight', 'eight1', 'eight2', 'eight3', 'eight4', 'eighty', 'eighty2', 'eleven', 'fifteen', 'fifty', 'fifty1', 'fifty2', 'fifty3', 'fifty4', 'five', 'five-2', 'five-3', 'five1', 'five2', 'five3', 'five4', 'five5', 'forty', 'forty2', 'forty3', 'forty4', 'four', 'four1', 'four2', 'four3', 'four4', 'four5', 'four6', 'fourteen', 'half', 'hundred', 'minus', 'minus2', 'nine', 'nine1', 'nine2', 'ninety', 'ninety1', 'ninety2', 'ninety3', 'one', 'one-2', 'one1', 'one2', 'one3', 'one4', 'one5', 'one_hundred', 'score', 'seven', 'seven-2', 'seven1', 'seven2', 'seven3', 'seven4', 'seven5', 'seventy', 'seventy2', 'six', 'six(2)', 'six1', 'six2', 'six3', 'six4', 'six5', 'sixteen', 'sixty', 'sixty2', 'sixty3', 'teen', 'ten', 'ten1', 'ten2', 'ten3', 'ten4', 'tens', 'tens_suff', 'tenstep', 'thirteen', 'thirty', 'thirty1', 'thirty2', 'three', 'three1', 'three2', 'three3', 'three4', 'three5', 'three6', 'twelve', 'twen', 'twenty', 'twenty2', 'twenty3', 'twenty4', 'twenty5', 'two', 'two-2', 'two1', 'two2', 'two3', 'two4', 'two5', 'ty', 'ty1', 'ty2', 'suff_pl'] #suff_pl represents tens in semitic

concepts = [str(i) for i in range(1,100)]

Z = sum([i**(-2) for i in range(1,100)])

vocab_size_manual_broad = {}

complexity_manual_broad = {}

for lang in languages:
    forms_ = [l for l in table if l[1] == lang]
    #deal with horn of africa
    for i,l in enumerate(forms_):
        forms_[i][7] = forms_[i][7].replace('ty ty','ty')
    if len(forms_) >= 99:
        form_dict = {}
        for l in forms_:
            if l[0].split('-')[-1] == '1':
                form_dict[l[3]] = [s for s in l[7].split() if s in morphemes_to_keep]
        vocab_size_manual_broad[lang] = len(set([s for v in form_dict.values() for s in v]))
        complexity_l = 0
        for i,num in enumerate(concepts):
            length = len(form_dict[num]) + len(form_dict[num]) - 1
            complexity_l += (length/((i+1)**2))/Z
        complexity_manual_broad[lang] = complexity_l

vocab_size_manual_narrow = {}

complexity_manual_narrow = {}

for lang in languages:
    forms_ = [l for l in table if l[1] == lang]
    #deal with horn of africa
    for i,l in enumerate(forms_):
        forms_[i][7] = forms_[i][7].replace('ty ty','ty')
    if len(forms_) >= 99:
        morph_counter = defaultdict(int)
        form_dict = {}
        for l in forms_:
            if l[0].split('-')[-1] == '1':
                form_dict[l[3]] = [s for s in l[7].split() if s in morphemes_to_keep]
                for s in form_dict[l[3]]:
                    morph_counter[s] += 1
        for key in form_dict.keys():
            #if max([morph_counter[s] for s in form_dict[key]]) == 1 and len(form_dict[key]) > 1:
            #    print(lang,key)
            if min([morph_counter[s] for s in form_dict[key]]) == 1:
                form_dict[key] = [''.join(form_dict[key])]
        vocab_size_manual_narrow[lang] = len(set([s for v in form_dict.values() for s in v]))
        complexity_l = 0
        for i,num in enumerate(concepts):
            length = len(form_dict[num]) + len(form_dict[num]) - 1
            complexity_l += (length/((i+1)**2))/Z
        complexity_manual_narrow[lang] = complexity_l

df = [['language','vocab_size_broad','ms_complexity_broad','vocab_size_narrow','ms_complexity_narrow']]

for key in vocab_size_manual_broad.keys():
    ll = [key,str(vocab_size_manual_broad[key]),str(complexity_manual_broad[key]),str(vocab_size_manual_narrow[key]),str(complexity_manual_narrow[key])]
    df.append(ll)

f = open('complexity_measures.tsv','w')

for l in df:
    print('\t'.join(l),file=f)

f.close()