import csv
from tqdm import tqdm

PATH = '/Users/tanishbafna/Desktop/Econometrics/Final Paper/'

def filter():

    fields = []
    rows = []

    #============================

    def i(field):
        return fields.index(field)

    def stringInside(parent, substring):

        for i in substring:
            if i in parent:
                return True
        
        return False

    #============================

    delValues = ['DD category', 'Monarchy', 'Commonwealth', 'Monarch name', 'Monarch accession', 'Monarch birthyear', 
    'Democracy', 'Presidential', 'President name', 'President accesion', 'President birthyear', 'Interim phase (more than 2 Presidents/year=1)', 
    'Colony', 'Colony of', 'Colony administrated by', 'Communist', 'Regime change lag', 'countrycode', 'No. of chambers in parliament', 
    'proportional voting', 'Election system', 'No. of members in lower house', 'No. of members in upper house', 'No. of members in third house', 
    'New constitution', 'Suffrage restriction', 'multiparty', 'election month, year', 'alternation', 'postponed election', 
    'DD regime', 'Female monarch (0: No; 1: Yes)', 'Female president (0: No; 1: Yes)', 'electoral', 'parliamentary election year']

    #============================

    with open('/Users/tanishbafna/Desktop/Econometrics/Final Paper/regime.csv') as csvfile:

        csvreader = csv.reader(csvfile, delimiter=',')
        fields = next(csvreader)

        #=================

        delIdx = [i(k) for k in delValues]
        emptyCols = []
        y = -1
        for x in range(fields.count('')):
            y = fields.index('', y + 1)
            emptyCols.append(y)

        delIdx = sorted(delIdx + emptyCols, reverse=True)

        #=================

        newFields = ['democracy', 'female_leader', 'opposition', 'gender_suffrage_restriction', 'wealth_suffrage_restriction', 'ethnic_racial_suffrage_restriction', 'literacy_suffrage_restriction', 'other_suffrage_restriction']
        for c in newFields:
            fields.append(c)
        
        #=================
        
        for row in csvreader:

            if int(row[i('year')]) < 1966 or row[i('spatial democracy')] == '' or row[i('electoral')] == '' or row[i('spatial electoral')] == '':
                continue

            democracy = 0 if row[i('DD regime')] in ['', '3', '4', '5'] else 1
            female_leader = 1 if (row[i('Female monarch (0: No; 1: Yes)')] == '1' or row[i('Female president (0: No; 1: Yes)')] == '1') else 0

            #=================

            electoral_entry = row[i('electoral')]
            opposition = 1 if electoral_entry in ['3', '2'] else 0

            #=================

            fullsuffrage = row[i('fullsuffrage')].strip()
            suffrage_restriction_entry = row[i('Suffrage restriction')].lower().split()

            gender_suffrage_restriction = 1 if stringInside(suffrage_restriction_entry, ['male', 'men']) else 0
            ethnic_racial_suffrage_restriction = 1 if stringInside(suffrage_restriction_entry, ['ethnic', 'racial']) else 0
            wealth_suffrage_restriction = 1 if stringInside(suffrage_restriction_entry, ['wealth', 'status', 'income', 'estate', 'money']) else 0
            literacy_suffrage_restriction = 1 if 'literacy' in suffrage_restriction_entry else 0

            total_suffrage_restriction = gender_suffrage_restriction + ethnic_racial_suffrage_restriction + wealth_suffrage_restriction + literacy_suffrage_restriction
            other_suffrage_restriction = 1 if fullsuffrage == '0' and total_suffrage_restriction < 1 else 0

            #=================

            row.append(democracy)
            row.append(female_leader)
            row.append(opposition)

            row.append(gender_suffrage_restriction)
            row.append(ethnic_racial_suffrage_restriction)
            row.append(wealth_suffrage_restriction)
            row.append(literacy_suffrage_restriction)
            row.append(other_suffrage_restriction)

            #=================

            for x in delIdx:
                row.pop(x)

            rows.append(row)
        
        for x in delIdx:
            fields.pop(x) 

        #============================

        with open(PATH + 'regime_filtered.csv', 'w') as csvfile2: 

            fields[i('\ufeffcountry')] = 'country'
            csvwriter = csv.writer(csvfile2) 
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)
        
        print(len(rows))

def merge():

    end_rows = []
    who_gov_fields = []
    regime_fields = []

    def i_who_gov(idx):
        return who_gov_fields.index(idx)

    def i_regime(idx):
        return regime_fields.index(idx)

    merging = ['spatial democracy', 'fullsuffrage', 'spatial electoral', 'free and fair election', 'democracy', 'female_leader', 'opposition', 'gender_suffrage_restriction', 'wealth_suffrage_restriction', 'ethnic_racial_suffrage_restriction', 'literacy_suffrage_restriction', 'other_suffrage_restriction']
    iso_edits = {"ZAR":"COD", "GER":"DEU", "ROM":"ROU"}
    iso_extra = {"YUG", "RVN", "DDR", "SUN", "YEM", "DVN"}

    with open(PATH + 'WhoGov.csv', 'r', encoding = 'ISO-8859-1') as who_gov_file:

        who_gov_reader = csv.reader(who_gov_file, delimiter=',', )
        who_gov_fields = next(who_gov_reader)
        all_who_gov = [row for row in who_gov_reader]

        idx_w_c = i_who_gov('country_isocode')
        idx_w_t = i_who_gov('year')

        # who_gov_countries = set()

        # try:
        #     for row in who_gov_reader:
        #         temp = row[i_who_gov('country_isocode')]
        #         if temp not in who_gov_countries:
        #             who_gov_countries.add(temp)
        # except:
        #     print(temp)
                
        who_gov_countries = set([row[idx_w_c] for row in all_who_gov])

        with open(PATH + 'regime_filtered.csv', 'r') as regime_file:

            regime_reader = csv.reader(regime_file, delimiter=',')
            regime_fields = next(regime_reader)
            all_regime = [row for row in regime_reader]

            idx_r_cy = i_regime('country')
            idx_r_c = i_regime('country isocode')
            idx_r_t = i_regime('year')

            for N, row in enumerate(all_regime):
                temp = row[idx_r_c]
                if temp in iso_edits:
                    all_regime[N][idx_r_c] = iso_edits[temp]

            regime_countries = set([row[idx_r_c] for row in all_regime])

            print(who_gov_countries.difference(regime_countries))

            deepcopy_fields = [z for z in regime_fields]
            deepcopy_fields.remove('country')
            deepcopy_fields.remove('year')
            deepcopy_fields.remove('country isocode')

            deepcopy_fields = who_gov_fields + deepcopy_fields

            errors = []

            for row_p in tqdm(all_who_gov):

                check = False

                for row_r in all_regime:

                    if row_p[idx_w_c] == row_r[idx_r_c] and int(row_p[idx_w_t].strip()) == int(row_r[idx_r_t].strip()):

                        deepcopy = [z for z in row_r]
                        deepcopy.pop(idx_r_t)
                        deepcopy.pop(idx_r_c)
                        deepcopy.pop(idx_r_cy)

                        end_rows.append(row_p + deepcopy)
                        check = True
                        break
                
                if check is False:
                    errors.append(row_p)
            

            with open(PATH + 'merged_who.csv', 'w') as csvfile:

                if len(end_rows[0]) != len(deepcopy_fields):
                    print('NO')
                    quit()

                writer = csv.writer(csvfile)
                writer.writerow(deepcopy_fields)
                writer.writerows(end_rows)

                print(f'Errors: {len(errors)}')
                print(f'Completed: {len(end_rows)}')
    

# with open('/Users/tanishbafna/Downloads/workingStata/merged_who_country.csv') as csvfile:

#     csvreader = csv.reader(csvfile, delimiter=',')
#     fields = next(csvreader)

#     idxDem = fields.index('democracy')
#     idxCountry = fields.index('country_name')

#     allCountries = {}
#     special = set()

#     for row in csvreader:

#         if row[idxCountry] in allCountries:
#             if row[idxDem] != allCountries[row[idxCountry]]:
#                 special.add(row[idxCountry])
#         else:
#             allCountries[row[idxCountry]] = row[idxDem]

# print(special)