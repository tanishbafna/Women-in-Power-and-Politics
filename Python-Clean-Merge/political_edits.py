import csv

fields = []
rows = []
delValues = ['country isocode', 'DD category', 'Monarchy', 'Commonwealth', 'Monarch name', 'Monarch accession', 'Monarch birthyear', 
'Democracy', 'Presidential', 'President name', 'President accesion', 'President birthyear', 'Interim phase (more than 2 Presidents/year=1)', 
'Colony', 'Colony of', 'Colony administrated by', 'Communist', 'Regime change lag', 'countrycode', 'No. of chambers in parliament', 
'proportional voting', 'Election system', 'No. of members in lower house', 'No. of members in upper house', 'No. of members in third house', 
'New constitution', 'fullsuffrage', 'Suffrage restriction', 'multiparty', 'election month, year', 'alternation', 'postponed election', 
'DD regime', 'Female monarch (0: No; 1: Yes)', 'Female president (0: No; 1: Yes)', 'electoral']

corrections = {
    "Korea, People's Republic": 'North Korea',
    "Korea, Republic of": 'South Korea',
    "United Arab Emirates": 'United Arab Emirate',
    "Bosnia and Herzegovina": 'Bosnia',
    "North Macedonia": 'Macedonia',
    "Congo, Dem. Rep.": 'Congo Kinshasa',
    "Congo, Republic of": 'Congo Brazzaville',
    "Timor-Leste": 'Timor Leste',
    "Gambia, The": 'Gambia'
}

def i(field):
    return fields.index(field)

with open('/Users/tanishbafna/Desktop/Econometrics/Final Paper/regime.csv') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')
    fields = next(csvreader)

    delIdx = [i(k) for k in delValues]

    emptyCols = []
    y = -1
    for x in range(fields.count('')):
        y = fields.index('', y + 1)
        emptyCols.append(y)

    delIdx = sorted(delIdx + emptyCols, reverse=True)

    newFields = ['democracy', 'autocracy', 'female_leader', 'no_elections', 'multi_party_democracy', 'single_party', 'multi_party_autocracy']
    for c in newFields:
        fields.append(c)
    
    for row in csvreader:

        if int(row[i('year')]) < 1990 or row[i('spatial democracy')] == '' or row[i('electoral')] == '' or row[i('spatial electoral')] == '':
            continue
        
        if row[i('\ufeffcountry')] in corrections:
            row[i('\ufeffcountry')] = corrections[row[i('\ufeffcountry')]]

        elif row[i('\ufeffcountry')] == "Russia" and int(row[i('year')]) < 1992:
            row[i('\ufeffcountry')] = 'USSR'
        
        elif 'Ivoire' in row[i('\ufeffcountry')] :
            row[i('\ufeffcountry')] = 'Ivory Coast'
            
        democracy = 0 if row[i('DD regime')] in ['', '3', '4', '5'] else 1
        autocracy = 0 if row[i('DD regime')] in ['', '0', '1', '2'] else 1

        female_leader = 1 if (row[i('Female monarch (0: No; 1: Yes)')] == '1' or row[i('Female president (0: No; 1: Yes)')] == '1') else 0

        if row[i('parliamentary election year')] != '1':
            row[i('parliamentary election year')] = '0'
        
        electoral_entry = row[i('electoral')]
        no_elections = 1 if electoral_entry == '0' else 0
        multi_party_democracy = 1 if electoral_entry == '3' else 0
        single_party = 1 if electoral_entry == '1' else 0
        multi_party_autocracy = 1 if electoral_entry == '2' else 0

        row.append(democracy)
        row.append(autocracy)
        row.append(female_leader)
        row.append(no_elections)
        row.append(multi_party_democracy)
        row.append(single_party)
        row.append(multi_party_autocracy)

        for x in delIdx:
            row.pop(x)

        rows.append(row)
    
    for x in delIdx:
        fields.pop(x) 

    with open('final2.csv', 'w') as csvfile2: 

        fields[i('\ufeffcountry')] = 'country'
        csvwriter = csv.writer(csvfile2) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(rows)
    
    print(len(rows))