def read_write():
    with open('ds.csv', 'r') as ds_csv:
        with open('ds.tsv', 'w') as ds_tsv:

            for line in ds_csv:
                line = line.replace(',"', '\t"')
                line = line.replace(',false', '\tfalse')
                line = line.replace(',true', '\ttrue')
                ds_tsv.write(line)

if __name__ == '__main__':
    read_write()