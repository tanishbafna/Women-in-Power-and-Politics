import csv
import time
import datetime

fields = []
rows = []
delValues = ['startday', 'startmonth', 'startyear', 'endday', 'endmonth', 'endyear', 'location', 'sources', 'notes', 'protesterdemand1', 'protesterdemand2', 'protesterdemand3', 'protesterdemand4', 'protesteridentity', 'stateresponse1', 'stateresponse2', 'stateresponse3', 'stateresponse4', 'stateresponse5', 'stateresponse6', 'stateresponse7', 'protest']
avgs = {
    '0-49': 25,
    '50-99': 75,
    '100-999': 500,
    '1000-1999': 1500,
    '2000-4999': 3500,
    '5000-10000': 7500,
    '>10000': False
}

counter = 0

def i(field):
    return fields.index(field)

if True:

    with open('/Users/tanishbafna/Desktop/Econometrics/Final Paper/unclean.csv') as csvfile:

        csvreader = csv.reader(csvfile, delimiter=',')
        fields = next(csvreader)
        
        delIdx = [i(k) for k in delValues]

        emptyCols = []
        y = -1
        for x in range(fields.count('')):
            y = fields.index('', y + 1)
            emptyCols.append(y)

        delIdx = sorted(delIdx + emptyCols, reverse=True)

        newFields = ['total_days', 'start_timestamp', 'end_timestamp', 'national_scale', 'woman_involvement', 'labor_wage_dispute', 'land_farm_issue', 'police_brutality', 'political_behavior', 'price_tax_policy', 'removal_of_politician', 'social_restrictions', 'accomodation', 'arrests', 'beatings', 'crowd_dispersal', 'ignore', 'killings', 'shootings', 'violent_response', 'violence_degree', 'complete_accomodation', 'temp_accomodation', 'accomodation_after_repression']
        for c in newFields:
            fields.append(c)

        idx = 0

        for row in csvreader:

            if row[i('protestnumber')] == '0':
                continue
            
            try:
                # date columns
                start_date = datetime.date(int(row[i('startyear')]), int(row[i('startmonth')]), int(row[i('startday')]))
                end_date = datetime.date(int(row[i('endyear')]), int(row[i('endmonth')]), int(row[i('endday')]))
                total_days = (end_date - start_date).days


                # coverting to utc timestamps
                start_timestamp = time.mktime(start_date.timetuple()) + 19800.0 #offset for local time
                end_timestamp = time.mktime(end_date.timetuple()) + 19800.0 + 86400.0 #offset for extra day


                # national scale
                possible_strings = [', national', '; national', 'national;', 'national,', 'national:',
                ', National', '; National', 'National,', 'National;', 'National  ', 'National:',
                'national in scope', 'national level']

                found = 0

                location_entry = row[i('location')]
                split = row[i('location')].split()
                if len(split) == 1:
                    if 'national' in split[0].lower():
                        found = 1
                
                else:
                    for s in possible_strings:
                        if s in location_entry:
                            found = 1
                            break
                
                # participants_category
                curr_idx = i('participants_category')
                if row[curr_idx] == '':
                    participants_entry = row[i('participants')]

                    if participants_entry in ['', '.']:
                        continue
                    
                    if '-' in participants_entry:
                        participants_entry = participants_entry[participants_entry.index('-') + 1:] #taking upper limit

                    participants_entry = participants_entry.replace(',', '').replace('>', '').replace('<', '').replace('s', '').replace('+', '').strip()

                    try:
                        participants_entry = int(participants_entry)
                    except:
                        continue
                        
                    if participants_entry < 50:
                        row[curr_idx] = '0-49'
                    elif participants_entry < 100:
                        row[curr_idx] = '50-99'
                    elif participants_entry < 1000:
                        row[curr_idx] = '100-999'
                    elif participants_entry < 2000:
                        row[curr_idx] = '1000-1999'
                    elif participants_entry < 5000:
                        row[curr_idx] = '2000-4999'
                    elif participants_entry <= 10000:
                        row[curr_idx] = '5000-10000'
                    elif participants_entry > 10000:
                        row[curr_idx] = '>10000'
                    else:
                        continue
                
                # participants_entry
                curr_idx = i('participants')
                participants_entry = row[curr_idx]

                participants_entry = participants_entry.replace(',', '').replace('>', '').replace('<', '').replace('s', '').replace('+', '').replace(' and', '-').replace('&', '-').replace('between', '-').replace('about', '').replace('S', '').strip()
                participants_entry_split = [m.lower() for m in participants_entry.split()]

                if '-' in participants_entry:
                    try:
                        find_idx = participants_entry.index('-')
                        avg = ( int(participants_entry[:find_idx].strip()) + int(participants_entry[find_idx+1:].strip()) ) // 2
                    except:
                        avg = avgs[row[i('participants_category')]]

                elif len(participants_entry_split) > 1:
                    temp = [int(s) for s in participants_entry_split if s.isdigit()]

                    if len(temp) == 2:
                        avg = sum(temp) // 2
                
                    elif len(temp) == 1:
                        avg = temp[0]

                    else:

                        if 'ten' in participants_entry_split and 'thouand' in participants_entry_split:
                            avg = 10000
                        
                        elif 'hundred' in participants_entry_split and 'thouand' in participants_entry_split:
                            avg = 100000

                        elif 'dozen' in participants_entry_split or 'hundred' in participants_entry_split:
                            avg = avgs[row[i('participants_category')]]

                        else:
                            avg = avgs[row[i('participants_category')]]
                    
                else:
                    if participants_entry_split[0].isdigit():
                        avg = participants_entry
                    elif 'dozen' in participants_entry_split or 'hundred' in participants_entry_split:
                        avg = avgs[row[i('participants_category')]]
                    else:
                        avg = avgs[row[i('participants_category')]]
                
                row[curr_idx] = avg

                # women specific involvement
                related_words = ['women', 'woman', 'female', 'girl']
                identity_entry = row[i('protesteridentity')]
                identity_match = 0

                for w in related_words:
                    if w in identity_entry.lower():
                        identity_match = 1
                        break

                # demands
                all_demands = [row[i('protesterdemand1')], row[i('protesterdemand2')], row[i('protesterdemand3')], row[i('protesterdemand4')]]

                wage = 1 if 'labor wage dispute' in all_demands else 0
                farm = 1 if 'land farm issue' in all_demands else 0
                police = 1 if 'police brutality' in all_demands else 0
                political = 1 if 'political behavior, process' in all_demands else 0
                price = 1 if 'price increases, tax policy' in all_demands else 0
                removal = 1 if 'removal of politician' in all_demands else 0
                social = 1 if 'social restrictions' in all_demands else 0

                # state response
                all_response = [row[i(f'stateresponse{g + 1}')] for g in range(0, 7) if row[i(f'stateresponse{g + 1}')] not in ['','.']]

                accomodation = 1 if 'accomodation' in all_response else 0
                arrests = 1 if 'arrests' in all_response else 0
                beatings = 1 if 'beatings' in all_response else 0
                dispersal = 1 if 'crowd dispersal' in all_response else 0
                ignore = 1 if 'ignore' in all_response else 0
                killings = 1 if 'killings' in all_response else 0
                shootings = 1 if 'shootings' in all_response else 0
                
                violent = 1 if (arrests + beatings + dispersal + killings + shootings) > 0 else 0
                violence_degree = ((arrests * 2) + (beatings * 3) + dispersal + (killings * 5) + (shootings * 4)) if violent == 1 else 0
                complete_accomodation = 1 if (accomodation == 1 and len(all_response) == 1) else 0
                temp_accomodation = 1 if (accomodation == 1 and all_response[-1] != 'accomodation') else 0
                accomodation_after_repression = 1 if (accomodation == 1 and len(all_response) > 1 and  all_response[-1] == 'accomodation') else 0
                
                # appending
                row.append(int(total_days) + 1)
                row.append(int(start_timestamp))
                row.append(int(end_timestamp))
                row.append(found)
                row.append(identity_match)
                row.append(wage)
                row.append(farm)
                row.append(police)
                row.append(political)
                row.append(price)
                row.append(removal)
                row.append(social)

                row.append(accomodation)
                row.append(arrests)
                row.append(beatings)
                row.append(dispersal)
                row.append(ignore)
                row.append(killings)
                row.append(shootings)

                row.append(violent)
                row.append(violence_degree)
                row.append(complete_accomodation)
                row.append(temp_accomodation)
                row.append(accomodation_after_repression)

            except:
                continue
                
            for x in delIdx:
                row.pop(x)
                
            rows.append(row)

        for x in delIdx:
            fields.pop(x) 
        
        with open('trial.csv', 'w') as csvfile2: 

            csvwriter = csv.writer(csvfile2) 
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)

            print(len(rows))


final_fields = ['id', 'country', 'ccode', 'year', 'region', 'protestnumber', 'total_days', 'start_timestamp', 'end_timestamp', 
'participants_category', 'participants', 'national_scale', 'protesterviolence', 'woman_involvement', 
'labor_wage_dispute', 'land_farm_issue', 'police_brutality', 'political_behavior', 'price_tax_policy', 'removal_of_politician', 'social_restrictions', 
'accomodation', 'ignore', 'violent_response', 'violence_degree',
'complete_accomodation', 'temp_accomodation', 'accomodation_after_repression', 'arrests', 'beatings', 'crowd_dispersal', 'killings', 'shootings']

with open('trial.csv', 'r') as csvfile3:

    reader = csv.DictReader(csvfile3)
    final_rows = [frow for frow in reader]

    kosovo = []

    for l in range(len(final_rows)):
        if final_rows[l]['country'] in ['Yugoslavia', 'Serbia and Montenegro']:
            final_rows[l]['country'] = 'Serbia'
        elif final_rows[l]['country'] == 'Czechoslovakia':
            final_rows[l]['country'] = 'Czech Republic'
        elif final_rows[l]['country'] in ['Germany East', 'Germany West']:
            final_rows[l]['country'] = 'Germany'
        elif final_rows[l]['country'] == 'Kosovo':
            kosovo.append(l)
    
    kosovo = sorted(kosovo, reverse=True)
    for u in kosovo:
        final_rows.pop(u)

    if len(list(final_rows[0].keys())) != len(final_fields):
        print('NO')
        quit()

    with open('final.csv', 'w') as csvfile4:
        writer = csv.DictWriter(csvfile4, fieldnames = final_fields)

        writer.writeheader()
        writer.writerows(final_rows)
    
    

# print(len(rows))
# print(counter)
# print(rows[0])
# print(rows[1])