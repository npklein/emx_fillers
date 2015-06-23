'''
Created on Jun 23, 2015

@author: Niek de Klein
'''

def column_names_to_attribute_names(column_names):
    delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
    attribute_names = []
    for column_name in column_names:
        # hacky way to preserve spaces
        column_name = column_name.replace(' ', 'SPAAAAAAAAAACE')
        column_name_clean = column_name.translate(None, delchars)
        column_name_clean = column_name_clean.replace('SPAAAAAAAAAACE','_')
        column_name_clean_list = list(column_name_clean)
        column_name_clean_list[0] = column_name_clean_list[0].lower()
        for index, letter in enumerate(column_name_clean_list[:-1]):
            if column_name_clean_list[index-1] == '_' and letter.isupper():
                column_name_clean_list[index] = letter.lower()
            elif letter.isupper() and not column_name_clean_list[index+1].isupper() \
                                and not column_name_clean_list[index-1].isupper():
                column_name_clean_list[index] = '_'+letter.lower()
        attribute_name = ''.join(column_name_clean_list)
        attribute_names.append(attribute_name)
    return attribute_names

def parse_text(text):
    '''
    Example usage:
    from rnaseq_pipeline_output_parser import parse_tables
    fastqc_data = open('fastqc_data.txt').read()
    new_fastqc_data = []
    for line in fastqc_data.split('\n'):
        if not line.startswith('>>') and not line.startswith('##'):
            new_fastqc_data.append(line)
        else:
            new_fastqc_data.append('replaced')

    print parse_tables.parse_text(new_fastqc_data)
    '''
    splitline_length_old = 0
    header = []
    table_length = 0
    reading_table = False
    splitline_old = ''
    header_list = []
    line_before_header = []
    for line in text:
        splitline = line.strip('\n').split('\t')
        if len(splitline) > 1 and len(splitline) == splitline_length_old:
            table_length += 1
            if not reading_table:
                header = splitline_old
            reading_table = True
        else:
            if table_length > 1:
                header_list.append(column_names_to_attribute_names(header))
                table_length = 0
            reading_table = False
        splitline_length_old = len(splitline)
        splitline_old = splitline
    return header_list

