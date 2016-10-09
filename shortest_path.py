from cPickle import load

impl = 'tlwiki'


title_to_ID_dict = load(open('data/%s_title-ID_dict.pkl' % (impl)))
ID_to_title_dict = load(open('data/%s_ID-title_dict.pkl' % (impl)))

link_dict = load(open('data/%s_link_dict.pkl' % (impl)))


def find_shortest_path(start, end, q=[]):

    start_term = "_".join(start.lower().split())
    end_term = "_".join(end.lower().split())

    start_path = title_to_ID_dict[start_term]
    end_path = title_to_ID_dict[end_term]
    visited_list = []
    q.append([start_path])

    while len(q) != 0:
        tmp_path = q.pop(0)
        last_path = tmp_path[len(tmp_path) - 1]
        # print last_path, ID_to_title_dict[last_path]

        if last_path == end_path:
            return [ID_to_title_dict[each] for each in tmp_path]

        if last_path not in visited_list:
            try:
                for link in link_dict[last_path]:
                    if link not in tmp_path:
                        new_path = tmp_path + [link]
                        q.append(new_path)
                        visited_list.append(last_path)
            except:
                pass

    return "No path found"


print find_shortest_path('thomas paine', 'europa')

