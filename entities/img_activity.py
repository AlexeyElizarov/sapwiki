from entities import Entity, IMGNode


class IMGActivity(Entity):
    """
    IMG-Activity
    """
    _query_table = 'CUS_IMGACH'
    _path = []

    @property
    def reference_nodes(self):
        nodes = []
        query_table = 'TNODEIMGR'
        options = f'REF_OBJECT = "{self.name}" AND REF_TYPE = "COBJ"'
        data, _ = self._read_table(query_table=query_table, options=options)

        if data:
            for item in data:
                node = IMGNode(self._connection)
                node.get(fields=['TREE_ID', 'EXTENSION', 'NODE_ID', 'EXT_KEY', 'NODE_TYPE', 'PARENT_ID'],
                         node_id=item['NODE_ID'])

                if node.name:
                    nodes.append(node)

        return nodes

    def get_img_path(self):
        paths = []

        for node in self.reference_nodes:
            paths.append(node.img_path)

        return paths

