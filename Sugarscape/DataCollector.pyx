import numpy
cimport numpy as cnp
import cython

@cython.wraparound(False)
@cython.nonecheck(False)
@cython.boundscheck(False)

cdef class DataCollector:
    cdef public list agent_attributes
    cdef public list model_attributes
    cdef public dict agent_dict
    cdef public dict data_dict
    cdef public dict plots_dict

    @cython.cdivision(True)
    cdef collectData(self, int period):
        cdef dict temp_dict
        cdef dict temp_dict_2
        cdef int ID
        cdef int attribute
        cdef int i
        cdef int num_agents = len(self.agent_dict)

        temp_dict = {}
        for attribute in self.agent_attributes:
            temp_dict[attribute] = cnp.empty(num_agents, dtype=cnp.float)
        
        for i, (ID, agent) in enumerate(self.agent_dict.items()):
            for attribute in self.agent_attributes:
                temp_dict[attribute][i] = getattr(agent, attribute)

        for attribute, val in temp_dict.items():
            self.data_dict[attribute][period] = cnp.mean(val)

        for attribute in self.model_attributes:
            self.data_dict[attribute][period] = getattr(self, attribute)
            self.plots_dict[attribute].append(getattr(self, attribute))