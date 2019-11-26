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
        node.get(fields=['TREE_ID', 'EXTENSION', 'NODE_ID', 'EXT_KEY', 'NODE_TYPE', 'PARENT_ID'], node_id=node_id)

        return node

    def _get_reference_node(self, node_id):
        """
        Returns reference node from the IMG table reference by reference node id.
        :param node_id: node id
        :return: IMG-node
        """

        node = IMGNode(self._connection)
        node.get(fields=['TREE_ID', 'EXTENSION', 'NODE_ID', 'EXT_KEY', 'NODE_TYPE', 'PARENT_ID'], refnode_id=node_id)

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
        img_nodes = [node]

        while True:
            # Loop is running while parent id can be identified.
            # If it cannot then it means that the root has been reached and loop must be stopped.

            # Get parent node by PARENT_ID
            parent = self._get_parent_node(node.PARENT_ID)
            img_nodes.insert(0, parent)

            if parent.PARENT_ID:
                node = parent
            else:
                parent = self._get_reference_node(parent.NODE_ID)
                if parent.PARENT_ID:
                    node = parent
                else:
                    break

        return ' -> '.join([node.text for node in img_nodes])
