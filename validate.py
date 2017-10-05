#!/usr/bin/python
import sys
import re

areacodes_dict = {}
phonenumbers_list = []
valid_phonenumbers = 0
invalid_phonenumbers = 0
invalid_areacode_region = 0

# read area code/region file into a dictionary
try:
    with open(sys.argv[1]) as areacodes_file:
        for line in areacodes_file:
            key = re.search(r'\d+', line.strip())
            value = re.search(r'([a-zA-Z0-9\.\-\&\,]+)\s*([a-zA-Z0-9\.\-\&\,]*)$', line.strip())
            try:
                if key.group() in areacodes_dict: # check for duplicate key
                    pass
                else:
                    areacodes_dict[key.group()] = value.group()
            except AttributeError:
                continue
except IndexError:
    print('Area code/region file missing.')
except FileNotFoundError:
    print('Invalid argument for area code/region filename.')    

# read phone numbers file into a list
try:
    with open(sys.argv[2]) as phonenumbers_file:
        for line in phonenumbers_file:
            phonenumber = re.search(r'^\(?(\d{3})[\.\-\)\s]*(\d{3})[\.\-\)\s]*(\d{4})$', \
                line.strip())            
            if phonenumber:                
                phonenumbers_list.append(phonenumber.group())
                valid_phonenumbers += 1
            else:
                invalid_phonenumbers += 1
except IndexError:
    print('Phone number file missing.')
except FileNotFoundError:
    print('Invalid argument for phone number filename.')

# match area codes of phone # list against keys of area code/region dictionary
output = open('matched.txt', 'w')
for line in phonenumbers_list:
    if line[:3] in areacodes_dict:
        output.write('({0}) {1}-{2} => {3}\n'.format(\
            line[:3], line[3:6], line[6:], areacodes_dict[line[:3]]))
    else:
        invalid_areacode_region += 1

# output pertinent information
print('Valid phone numbers:', valid_phonenumbers)
print('Invalid phone numbers:', invalid_phonenumbers)
print('Invalid area code region:', invalid_areacode_region)

'''
# alternate code for matching area codes with phone numbers using regex
output = open('output.txt', 'w')
for line in phonenumbers_list:
    areacode = re.search(r'^\(?(\d{3})[\.\-\)\s]*(\d{3})[\.\-\)\s]*(\d{4})$', \
        line.strip())
    try:
        if areacode.group(1) in areacodes_dict:
            output.write('({0}) {1}-{2} => {3}\n'.format(areacode.group(1), \
                areacode.group(2), areacode.group(3), areacodes_dict[areacode.group(1)]))
        else:
            invalid_areacode_region += 1
    except AttributeError:
        continue
'''