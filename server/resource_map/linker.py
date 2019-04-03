import queue
from collections import deque
import copy

allowed_linker_map = {
    'bed': ['matrix'],
    'matrix': ['bed', 'model_3d'],
    'model_3d': ['matrix'],
}


class Resource_Map_Linker(object):
    """Documentation for Resource_Map_Linker

    """

    def __init__(self):
        super(Resource_Map_Linker, self).__init__()

    @classmethod
    def domain_type_to_linker_type(self, domain_type):
        linker_type = ''
        for i in range(allowed_linker_map.keys()):
            if i in domain_type:
                linker_type = i
        return linker_type

    @classmethod
    def infer_link_method(cls, d1_type, d2_type, test=False):
        linker_type_to_func = {
            ('bed', 'matrix'): cls.linker_bed_to_matrix,
            ('matrix', 'bed'): cls.linker_matrix_to_bed,
            ('matrix', 'model_3d'): cls.linker_matrix_to_model_3d,
            ('model_3d', 'matrix'): cls.linker_model_3d_to_matrix,
        }
        linker_type_to_func_test = {
            ('bed', 'matrix'): 'linker_bed_to_matrix',
            ('matrix', 'bed'): 'linker_matrix_to_bed',
            ('matrix', 'model_3d'): 'linker_matrix_to_model_3d',
            ('model_3d', 'matrix'): 'linker_model_3d_to_matrix',
        }
        if test:
            linker_type_to_func = linker_type_to_func_test
        link_queue = deque()
        if d2_type in allowed_linker_map[d1_type]:
            link_queue.append(linker_type_to_func[(d1_type, d2_type)])
        else:
            ###################################################################
            #                BFS With Stack: Search link rules                #
            ###################################################################
            search_queue = deque()
            searched_queue = deque()
            search_flag = False

            # Init push
            search_queue.append([d1_type])
            searched_queue.append([d1_type])
            while not len(search_queue) == 0:
                # pop the first stack in search queue
                
                # print('search queue', search_queue)
                # print('searched queue', searched_queue)
                pop_stack = search_queue.pop()
                # if the top of the stack is not searched
                if pop_stack[-1] not in searched_queue:
                    # if the top of the stack == target
                    if d2_type in allowed_linker_map[pop_stack[-1]]:
                        # Bingo! Generate link queue according to the stack
                        pop_stack.append(d2_type)
                        for j in range(len(pop_stack) - 1):
                            link_queue.append(
                                linker_type_to_func[(pop_stack[j],
                                                     pop_stack[j + 1])])
                        return link_queue
                    # if the top of the stack is not in searched queue
                    else:
                        # push the child node of the stack top
                        for i in allowed_linker_map[pop_stack[-1]]:
                            # only push the non searched node
                            if i not in searched_queue:
                                _new_pop_stack = copy.deepcopy(pop_stack)
                                _new_pop_stack.append(i)
                                search_queue.append(_new_pop_stack)
                            # mark the stack top as searched
                            searched_queue.append(pop_stack[-1])
        if link_queue:
            return link_queue
        else:
            return None

    @classmethod
    def linker_bed_to_matrix(cls, bed, *args):
        return bed[3]

    @classmethod
    def linker_matrix_to_bed(cls, matrix, *args):
        return matrix[0]

    @classmethod
    def linker_matrix_to_model_3d(cls, matrix, *args):
        return matrix[0]

    @classmethod
    def linker_model_3d_to_matrix(cls, model_3d, *args):
        return model_3d
    
    @classmethod
    def convert_index(cls, data, d1_type, d2_type):
        methods = cls.infer_link_method(d1_type, d2_type)
        out_data = data.deepcopy()
        for f in methods:
            out_data = f(out_data)
        return out_data
