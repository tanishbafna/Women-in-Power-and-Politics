import csv
from tqdm import tqdm

PATH = '/Users/tanishbafna/Desktop/Econometrics/Final Paper/pythonWork/'

def parties_final():

    end_rows = []
    who_gov_fields = []
    regime_fields = []

    def i_who_gov(idx):
        return who_gov_fields.index(idx)

    def i_regime(idx):
        return regime_fields.index(idx)

    with open(PATH + 'WhoGov_within_V1.2.csv', 'r', encoding = 'latin-1') as who_gov_file:

        who_gov_reader = csv.reader(who_gov_file, delimiter=',', )
        who_gov_fields = next(who_gov_reader) + ['n_portfolio']
        all_who_gov = [row for row in who_gov_reader]

        for row in all_who_gov:
            tot = 0

            if row[i_who_gov('portfolio_1')] != "NA":
                tot += 1
            if row[i_who_gov('portfolio_2')] != "NA":
                tot += 1
            if row[i_who_gov('portfolio_3')] != "NA":
                tot += 1
            if row[i_who_gov('portfolio_4')] != "NA":
                tot += 1
            
            row.append(tot)

        idx_w_c = i_who_gov('country_isocode')
        idx_w_t = i_who_gov('year')
        idx_w_p = i_who_gov('party_english')

        who_gov_parties = set([(row[idx_w_p] + f' ({row[idx_w_c]})').lower().strip().replace('\x92', "'") for row in all_who_gov if row[idx_w_p] not in ['independent', 'na', 'NA', 'na ']])
        who_gov_countries = set([row[idx_w_c] for row in all_who_gov])

        print(f'Parties: {len(who_gov_parties)}')
        print(f'Countries: {len(who_gov_countries)}')

        with open(PATH + 'V-Dem-CPD-Party-V1.csv', 'r', encoding = 'latin-1') as regime_file:

            regime_reader = csv.reader(regime_file, delimiter=',')
            regime_fields = next(regime_reader)
            all_regime = [row for row in regime_reader]

            idx_r_c = i_regime('country_text_id')
            idx_r_p = i_regime('v2paenname')
            idx_r_t = i_regime('year')

            regime_parties = set([(row[idx_r_p] + f' ({row[idx_r_c]})').lower().strip().replace('\x92', "'") for row in all_regime])
            regime_countries = set([row[idx_r_c] for row in all_regime])

            with open (PATH + 'leftOutParties.txt', 'w') as error:
                for i in list(who_gov_parties.difference(regime_parties)):
                    error.write(i + '\n')

            print(f'Left Out Parties: {len(who_gov_parties.difference(regime_parties))}')
            print(f'Left Out Countries: {len(who_gov_countries.difference(regime_countries))}')

            merging = ['v2xpa_illiberal', 'v2xpa_popul', 'v2paanteli', 'v2papeople', 'v2paminor', 'v2paviol', 'v2paimmig', 'v2palgbt', 'v2paculsup', 'v2parelig', 'v2pagender', 'v2pawomlab', 'v2pariglef', 'v2paopresp', 'v2paplur', 'v2pawelf', 'v2paclient']
            deepcopy_fields = who_gov_fields + merging
            errors = {'no info':[], 'missing history':[], 'missing parties':[]}

            data_all = {}
            for x in who_gov_countries:
                data_country = {}

                for row in all_regime:
                    if row[idx_r_c] == x:
                        tempP = row[idx_r_p].lower().strip().replace('\x92', "'")

                        if tempP not in data_country:
                            data_country[tempP] = {}

                        data_country[tempP][int(row[idx_r_t].lower().strip())] = [row[i_regime(var)] for var in merging]
                
                data_all[x] = data_country

            for row_p in tqdm(all_who_gov):

                current_year = int(row_p[idx_w_t].strip())
                current_party = row_p[idx_w_p].lower().strip().replace('\x92', "'")
                current_country = row_p[idx_w_c]

                if current_country in data_all and current_party in data_all[current_country]:
                    yearsAvail = list(data_all[current_country][current_party].keys())

                    if len(yearsAvail) == 0:
                        errors['no info'].append(row_p)
                        continue

                    if current_year in yearsAvail:
                        goYear = current_year
                    else:
                        yearsAvail.append(current_year)
                        sortedYearsAvail = sorted(yearsAvail)

                        if sortedYearsAvail[0] == current_year:
                            if sortedYearsAvail[1] - sortedYearsAvail[0] > 5:
                                errors['missing history'].append(row_p)
                                continue
                            else:
                                goYear = sortedYearsAvail[1]

                        else:
                            goYear = sortedYearsAvail[:sortedYearsAvail.index(current_year)][-1]

                    end_rows.append(row_p + data_all[current_country][current_party][goYear])
                
                else:
                    errors['missing parties'].append(row_p)

            
            
            with open(PATH + 'parties_final2.csv', 'w') as csvfile:

                if len(end_rows[0]) != len(deepcopy_fields):
                    print('NO')
                    quit()

                delIdx = sorted([deepcopy_fields.index('position'),
                deepcopy_fields.index('name'),
                deepcopy_fields.index('party'),
                deepcopy_fields.index('party_english'),
                deepcopy_fields.index('party_otherlanguage'),
                deepcopy_fields.index('classification')], reverse = True)

                for i in end_rows:
                    for j in delIdx:
                        i.pop(j)
                
                for i in delIdx:
                    deepcopy_fields.pop(i)

                writer = csv.writer(csvfile)
                writer.writerow(deepcopy_fields)
                writer.writerows(end_rows)

                for k, v in errors.items():
                    print(f'Error ({k}): {len(v)}')

                print(f'Completed: {len(end_rows)}')

parties_final()

# with open(PATH + 'reformat.csv', 'r') as file:

#     reader = csv.reader(file, delimiter=',')
#     fields = next(reader)
#     allRows = [row for row in reader]

#     time = {}
#     x = set()

#     def i_(idx):
#         return fields.index(idx)
    
#     for row in allRows:

#         if row[i_('year')] not in time:
#             time[row[i_('year')]] = 0

#         if row[i_('female')] == '1':
#             time[row[i_('year')]] += 1

#     for row in allRows:
#         t = str(int(row[i_('year')]) - 1)

#         if t not in time:
#             x.add(t)
#             row.append('')
        
#         else:
#             row.append(time[t])

#     with open(PATH + 'reformat2.csv', 'w') as csvfile:

#         if len(allRows[0]) != len(fields) + 1:
#             print('NO')
#             quit()

#         writer = csv.writer(csvfile)
#         writer.writerow(fields + ['prev_fem'])
#         writer.writerows(allRows)