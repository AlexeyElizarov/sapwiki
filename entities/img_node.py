from entities import Entity


class IMGNode(Entity):
    """
    IMG-Node
    """
    _query_table = 'TNODEIMG'
    _key_field = 'NODE_ID'
    _img_tree = []

    @property
    def text(self):
        if self.NODE_TYPE == 'IMG':
            return self.reference_activities[0].text
        else:
            return self._get_text()

    @property
    def reference_activities(self):
        from entities import IMGActivity
        activities = []
        query_table = 'TNODEIMGR'
        options = f'NODE_ID = "{self.name}" AND REF_TYPE = "COBJ"'
        data, _ = self._read_table(query_table=query_table, options=options, rowcount=1)

        if data:
            for item in data:
                activity = IMGActivity(self._connection)
                activity.get(activity=item['REF_OBJECT'])
                activities.append(activity)

        return activities

    def _get_parent_node(self, node_id):
        """
        Returns parent node from the IMG table reference by parent id.
        :param node_id: node id
        :return: IMG-node
        """

        node = IMGNode(self._connection)
        node.get(fields=['TREE_ID', 'EXTENSION', 'NODE_ID', 'EXT_KEY', 'NODE_TYPE', 'PARENT_ID', 'REFNODE_ID'], node_id=node_id)

        return node

    def _get_reference_node(self, node_id, tree_id, extension):
        """
        Returns reference node from the IMG table reference by reference node id.
        :param node_id: node id
        :return: IMG-node
        """

        node = IMGNode(self._connection)

        node.get(fields=['TREE_ID', 'EXTENSION', 'NODE_ID', 'EXT_KEY', 'NODE_TYPE', 'PARENT_ID', 'REFNODE_ID'],
                 refnode_id='', reftree_id=tree_id, extension=extension)

        if not node.name:
            node.get(fields=['TREE_ID', 'EXTENSION', 'NODE_ID', 'EXT_KEY', 'NODE_TYPE', 'PARENT_ID', 'REFNODE_ID'],
                     refnode_id=node_id, reftree_id=tree_id, extension=extension)

        if not node.name:
            node.get(fields=['TREE_ID', 'EXTENSION', 'NODE_ID', 'EXT_KEY', 'NODE_TYPE', 'PARENT_ID', 'REFNODE_ID'],
                     refnode_id='', reftree_id=tree_id)

        if not node.name:
            node.get(fields=['TREE_ID', 'EXTENSION', 'NODE_ID', 'EXT_KEY', 'NODE_TYPE', 'PARENT_ID', 'REFNODE_ID'],
                     refnode_id=node_id, reftree_id=tree_id)

        return node

    @property
    def img_path(self):
        """
        Returns IMG-path of the node.
        :return: IMG-path
        """

        # First seed is self
        node = self

        # IMG Nodes
        # img_nodes = [node]
        img_nodes = []

        while node.name:
            # Loop is running while parent id can be identified.
            # If it cannot then it means that the root has been reached and loop must be stopped.

            # print(node.NODE_ID, node.NODE_TYPE, node.text)

            if node.NODE_TYPE == 'IMG':
                img_nodes.insert(0, node)
                node = self._get_parent_node(node.PARENT_ID)
            elif node.NODE_TYPE == 'IMG0':
                if node.PARENT_ID:
                    img_nodes.insert(0, node)
                    node = self._get_parent_node(node.PARENT_ID)
                else:
                    ref_node = self._get_reference_node(node.NODE_ID, node.TREE_ID, node.EXTENSION)
                    if not ref_node.name:
                        img_nodes.insert(0, node)
                    node = ref_node
            elif node.NODE_TYPE == 'REF':
                img_nodes.insert(0, node)
                if node.PARENT_ID:
                    node = self._get_parent_node(node.PARENT_ID)

        # Check if root is New SAP IMG.
        # If it is not, return None.
        root = img_nodes[0]

        if root.NODE_ID not in ('368DDFAC3AB96CCFE10000009B38F976', '61B34417DD1FD311930100A0C9A384CE'):
            return None

        path = ' → '.join([node.text for node in img_nodes])
        # path = ' → '.join([node.name + ' ' + node.text + '\n' for node in img_nodes])

        return path
