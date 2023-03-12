from pprint import pprint
import csv
import re


def fix_phonebook():
    with open('phonebook_raw.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
    pprint(contacts_list)

    pattern_name = r'([А-Я][а-я]\w+).([А-Я][а-я]\w+).([А-Я][а-я]\w+)?'
    pattern_phone = r'(\+7|8)([ \(]+|)(\d{3})([\)\- ]+|)(\d{3})([- ]+|)(\d\d)([- ]+|)(\d\d)([ \(]+(доб.).(\d+)(\)|))?'

    counter = 1
    names = {}

    for contact in contacts_list[1:]:
        text = ' '.join(contact[:3])
        name_list = re.findall(pattern_name, text)[0]
        phone = re.sub(pattern_phone, '+7(\\3)\\5-\\7-\\9 \\11\\12', contact[-2])
        phone = phone if 'доб' in phone else phone[:-1]
        contact[-2] = phone
        contact[0], contact[1], contact[2] = name_list
        contacts_list[counter] = contact
        counter += 1
        last_and_firstname = ' '.join(name_list[:-1])
        if last_and_firstname not in names:
            names[last_and_firstname] = dict.fromkeys(contacts_list[0][2:], '')
        for key, value in zip(contacts_list[0][2:], contact[2:]):
            names[last_and_firstname][key] = value if value else names[last_and_firstname].get(key, '')

    new_file = [contacts_list[0], *[name.split(' ') + list(info.values()) for name, info in names.items()]]

    with open('phonebook.csv', 'w', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_file)


if __name__ == '__main__':
    fix_phonebook()
