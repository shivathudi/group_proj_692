from re import finditer
from cPickle import dump

def process_line(line, d):
    ''' Gets the ID and name for each page in the line. Only uses links that are in namespace 0 (the
    main wikipedia, ignores 'talk' pages, etc) '''

    pattern = "\((\d+),(\d+),'(.*?)','"
    for match in finditer(pattern, line):
        ID, namespace, name = match.groups()
        if namespace == '0':
            d[name.lower()] = int(ID)


def main(impl):
    ''' Reads page.sql line by line and processes it '''
    print 'making title <--> ID dictionaries...'
    insert_terms = 'INSERT INTO `page` VALUES'
    t2id = {}
    infile = '%s-latest-page.sql' % (impl)
    file_handle = open(infile)
    for line in file_handle:
        if line[:len(insert_terms)] == insert_terms:
            process_line(line, t2id)
    file_handle.close()

    id2t = {v:k for k, v in t2id.iteritems()}
    dump(t2id, open('data/%s_title-ID_dict.pkl' % impl, 'w'), 2)
    dump(id2t, open('data/%s_ID-title_dict.pkl' % impl, 'w'), 2)

if __name__ == '__main__':
    main('tlwiki')
