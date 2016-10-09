from re import finditer
from cPickle import load, dump


link_dict = {}


def process_line(line, d):
    '''
    Example contents of line: 
    (12,0,'A._S._Neill',3),(12,0,'AK_Press',4),....

    Each tuple is of the form ('from' page, namespace, 'to' page).  Only consider
    links that are in namespace 0 (the main wikipedia, ignores 'talk' pages, etc).
    Annoyingly, the 'from' pages are given by ID and the 'to' pages by name.
    Use the dictionary d to map the text names to IDs for consistency (and some space savings).
    '''

    pattern = "\((\d+),(\d+),'(.*?)',(\d+)\)[,;]"
    for match in finditer(pattern, line):
        from_page, namespace, to_page, from_ns = match.groups()

        from_page = int(from_page)
        try:
            if from_page not in link_dict:
                link_dict[from_page] = [d[to_page.lower()]]
            else:
                link_dict[from_page].append(d[to_page.lower()])
        except:
            pass

    return None


def main(impl):
    ''' Reads pagelinks.sql line by line and processes it. Needs the pickled 
    dictionary mapping page names to IDs '''

    print('building the graph...')
    insert_text = 'INSERT INTO `pagelinks` VALUES'
    d = load(open('data/%s_title-ID_dict.pkl'%(impl)))
    with open('%s-latest-pagelinks.sql' % (impl)) as infile:
        for line in infile:
            if line[:len(insert_text)] == insert_text:
                process_line(line, d)




current_impl = 'tlwiki'
if __name__ == '__main__':
    main(current_impl)
    output = open('data/%s_link_dict.pkl' % current_impl, 'w')
    dump(link_dict, output, 2)
    output.close()


