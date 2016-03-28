import numpy as np


def get_links(nodes_at_link, sort=True):
    """Get links and their directions at each node.

    Parameters
    ----------
    nodes_at_link : ndarray of int, shape `(n_links, 2)`
        Node identifier for each link tail and head.

    Returns
    -------
    tuple of ndarray of int
        Tuple of link identifiers for each node, link directions for each
        node and offsets into these arrays for each node.

    Examples
    --------
    ::
        0 -- 1
        |    | \
        2 -- 3 - 4

    >>> import numpy as np
    >>> nodes_at_link = np.array([[2, 3], [3, 4], [2, 0], [3, 1], [4, 1],
    ...                           [0, 1]])
    >>> (links_at_node, link_dirs_at_node, offset_to_node) = get_links(nodes_at_link)
    >>> links_at_node
    array([2, 5, 3, 4, 5, 0, 2, 0, 1, 3, 1, 4])
    >>> link_dirs_at_node
    array([ 1, -1,  1,  1,  1, -1, -1,  1, -1, -1,  1, -1])
    >>> offset_to_node
    array([ 0,  2,  5,  7, 10, 12])
    """
    sorted = np.argsort(nodes_at_link.reshape((-1, )))

    links_at_node = sorted // 2
    link_dirs_at_node = sorted % 2
    link_dirs_at_node[link_dirs_at_node == 0] = -1

    (_, links_per_node) = np.unique(nodes_at_link, return_counts=True)

    offset_to_node = np.empty(len(links_per_node) + 1, dtype=int)
    offset_to_node[0] = 0
    links_per_node.cumsum(out=offset_to_node[1:])

    return links_at_node, link_dirs_at_node, offset_to_node


def links2(nodes_at_link):
    from .ext.elements import get_links_at_node

    nodes_at_link = nodes_at_link.reshape((-1, ))

    n_link_ends = len(nodes_at_link)

    links_at_node = np.empty(n_link_ends, dtype=int)
    link_dirs_at_node = np.empty(n_link_ends, dtype=int)
    offset_to_node = np.empty(n_link_ends + 1, dtype=int)

    get_links_at_node(nodes_at_link, links_at_node, link_dirs_at_node,
                      offset_to_node)

    return links_at_node, link_dirs_at_node, offset_to_node


