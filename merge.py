import csv
from tqdm import tqdm

end_rows = []
protest_fields = []
regime_fields = []

def i_protest(idx):
    return protest_fields.index(idx)

def i_regime(idx):
    return regime_fields.index(idx)

final_fields = ['id', 'country', 'ccode', 'year', 'region', 'protestnumber', 'total_days', 'start_timestamp', 'end_timestamp', 
'participants_category', 'participants', 'national_scale', 'protesterviolence', 'woman_involvement', 
'labor_wage_dispute', 'land_farm_issue', 'police_brutality', 'political_behavior', 'price_tax_policy', 'removal_of_politician', 'social_restrictions', 
'accomodation', 'ignore', 'violent_response', 'violence_degree',
'complete_accomodation', 'temp_accomodation', 'accomodation_after_repression', 'arrests', 'beatings', 'crowd_dispersal', 'killings', 'shootings',
'spatial democracy', 'spatial electoral', 'free and fair election', 'parliamentary election year', 'democracy', 'autocracy', 
'female_leader', 'no_elections', 'multi_party_democracy', 'single_party', 'multi_party_autocracy']

merging = ['spatial democracy', 'spatial electoral', 'free and fair election', 'parliamentary election year', 'democracy', 'autocracy', 
'female_leader', 'no_elections', 'multi_party_democracy', 'single_party', 'multi_party_autocracy']

with open('final.csv', 'r') as protest_file:

    protest_reader = csv.reader(protest_file, delimiter=',')
    protest_fields = next(protest_reader)
    all_protest = [row for row in protest_reader]
    protest_countries = set([row[i_protest('country')] for row in protest_reader])
    
    with open('final2.csv', 'r') as regime_file:

        regime_reader = csv.reader(regime_file, delimiter=',')
        regime_fields = next(regime_reader)
        all_regime = [row for row in regime_reader]
        regime_countries = set([row[i_regime('country')] for row in regime_reader])
    
        #print(list(protest_countries - regime_countries))

        idx_p_c = i_protest('country')
        idx_p_t = i_protest('year')
        idx_r_c = i_regime('country')
        idx_r_t = i_regime('year')

        deepcopy_fields = [z for z in regime_fields]
        deepcopy_fields.remove('country')
        deepcopy_fields.remove('year')
        deepcopy_fields = protest_fields + deepcopy_fields

        # assert deepcopy_fields == final_fields

        for row_p in tqdm(all_protest):

            check = False

            for row_r in all_regime:

                if row_p[idx_p_c] == row_r[idx_r_c] and int(row_p[idx_p_t].strip()) == int(row_r[idx_r_t].strip()):

                    deepcopy = [z for z in row_r]
                    deepcopy.pop(idx_r_t)
                    deepcopy.pop(idx_r_c)

                    end_rows.append(row_p + deepcopy)
                    check = True
                    break
            
            if check is False:
                print(row_p)
        

        with open('merged.csv', 'w') as csvfile:

            if len(end_rows[0]) != len(deepcopy_fields):
                print('NO')
                quit()

            writer = csv.writer(csvfile)
            writer.writerow(deepcopy_fields)
            writer.writerows(end_rows)

            
        
        