import json
import re

# -------------Acceptable Input Formats---------------#

format1 = ['Lastname', 'Firstname', 'Phonenumber', 'Color', 'Zipcode']
format2 = ['Firstname', 'Lastname', 'Color', 'Zipcode', 'Phonenumber']
format3 = ['Firstname', 'Lastname', 'Zipcode', 'Phonenumber', 'Color']

def Text_to_Json(f):
    final = dict()
    final['entries'] = list()
    final['errors'] = list()
    valid_lines = list()

# -------------Reading line from the File-------------------#

    for (key, line) in enumerate(f.readlines()):
        d = dict()
        phonenumber = re.search(r'\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}',
                                line)
        zipcode = re.search(r'[,\s](\b\d{5}\b)', line)
        fullname = re.search(r'[A-Z][a-z]+\s[A-Z]?.?\s?[A-Z][a-z]+',
                             line)

# -------Eleminating the Invalid Lines / Ballparking mathematical Technique-------#

        if phonenumber and zipcode:
            valid_lines.append(key)
        else:
            final['errors'].append(key)

        if key in valid_lines:
            list_line = line.strip().split(',')

# -----------Validating with Acceptable Formats-----------------#

            if sum(x.isdigit() for x in list_line[-1]) == 5:
                for (k, v) in enumerate(format1):
                    d[v] = list_line[k].strip()
                final['entries'].append(d)
            elif sum(x.isdigit() for x in list_line[3]) == 10 \
                and len(list_line) == 4:
                list_line.insert(3, list_line[3].strip().replace(' ',
                                 '-'))
                if len(fullname.group().split()) > 2:
                    (firstname, lastname) = \
                        (fullname.group().split()[0],
                         fullname.group().split()[1]
                         + fullname.group().split()[2])  # split and store fullname into firstname and lastname
                else:
                    (firstname, lastname) = (list_line[0].split()[0],
                            list_line[0].split()[1])
                list_line[0] = firstname
                list_line.insert(1, lastname)
                for (k, v) in enumerate(format2):
                    d[v] = list_line[k].strip()
                final['entries'].append(d)
            elif sum(x.isdigit() for x in list_line[2]) == 5:
                list_line[3] = list_line[3].strip().replace(' ', '-')
                for (k, v) in enumerate(format3):
                    d[v] = list_line[k].strip()
                final['entries'].append(d)
    return final

def main():
    with open('data.in') as fh:  # opening file as fh(handler)
        result = Text_to_Json(fh)  # callingn function with file as parameter
    if result is not None:
        with open('Json_File.in', 'w') as jh:
            json.dump(result, jh, indent=2, sort_keys=True)  # Exporting the data as Json_File.in
    else:
        print 'Result is empty!'

if __name__ == '__main__':
    main()
