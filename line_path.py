class LinePath:
    class LinePathIterator:
        def __init__(self, lp):
            # Team object reference
            self.__lp = lp
            # member variable to keep track of current index
            self.__index = 0

        def __next__(self):
            if self.__index < len(self.__lp.get_path_list()):
                result = self.__lp.get_path_list()[self.__index]
                self.__index += 1
                return result
            # End of Iteration
            raise StopIteration

    def __init__(self):
        self.__path_list = []
        self.__cur_path = None

    def add(self, line_seg):
        if self.__cur_path is None:
            self.__path_list.append([])
            self.__cur_path = self.__path_list[0]
            self.__cur_path.append(line_seg[0])
        elif (self.__cur_path[len(self.__cur_path) - 1][0] != line_seg[0][0] or
              self.__cur_path[len(self.__cur_path) - 1][1] != line_seg[0][1]):
            self.__path_list.append([])
            self.__cur_path = self.__path_list[len(self.__path_list) - 1]
            self.__cur_path.append(line_seg[0])
        self.__cur_path.append(line_seg[1])

    def update(self, point):
        if self.__cur_path is None:
            self.add([point.copy(), point])
        else:
            self.__cur_path[len(self.__cur_path) - 1][0] = point[0]
            self.__cur_path[len(self.__cur_path) - 1][1] = point[1]

    def clear(self):
        self.__path_list = []
        self.__cur_path = None

    def is_empty(self):
        return self.__cur_path is None

    def get_path_list(self):
        return self.__path_list

    def __iter__(self):
        return self.LinePathIterator(self)
