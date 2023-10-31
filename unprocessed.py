from datetime import datetime
import typing
import json

class UnprocessedModel:

    """Model containing initial data structures - node set, asset map, switch
    map, terminal map, and connectivity map. Loads the structures upon
    initialization.

    Args: json string holding the CIM model, e.g. curl-exported from the PowerCIM database query
    """

    def __init__(self,
                 jsonfile):
        self._node_set = None
        self._asset_map = None
        self._switch_map = None
        self._terminal_map = None
        self._connectivity_map = None
        self._load_data_structures(jsonfile)

    @property
    def node_set(self):
        """Node set"""
        return self._node_set

    @property
    def asset_map(self):
        """Asset map"""
        return self._asset_map

    @property
    def switch_map(self):
        """Switch map"""
        return self._switch_map

    @property
    def terminal_map(self):
        """Terminal map"""
        return self._switch_map
        return self._terminal_map

    @property
    def connectivity_map(self):
        """Connectivity map"""
        return self._connectivity_map

    def _load_data_structures(self, jsonfile, branch, commit, valid_time):

        node_set = []
        asset_map = {}
        switch_map = {}
        terminal_map = {}
        connectivity_map = {}

        json_cim = json.loads(jsonfile)
        for record in json_cim:
            record['mrid'] = str(record['mrid'])
            record = dict(record, **record['fullobject'])
            del record['fullobject']

            mrid = str(record['mrid'])
            asset_map[mrid] = record
            if record['cimclass'] == 'cim:ConnectivityNode':
                node_set.append(record)
            elif record['cimclass'] in ('cim:Breaker', 'cim:Disconnector'):
                switch_map[mrid] = True  
                #if mrid in snapshot:
                #    print(snapshot.get(mrid))
            elif record['cimclass'] == 'cim:Terminal':
                element_mrid = str(record['cim:Terminal.ConductingEquipment'])
                terminal_map.setdefault(element_mrid, [])
                terminal_map[element_mrid].append(mrid)

                cn_mrid = str(record['cim:Terminal.ConnectivityNode'])
                connectivity_map.setdefault(cn_mrid, [])
                connectivity_map[cn_mrid].append(mrid)

        self._node_set = node_set
        self._asset_map = asset_map
        self._switch_map = switch_map
        self._terminal_map = terminal_map
        self._connectivity_map = connectivity_map
