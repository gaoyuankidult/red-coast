#!/usr/bin/env python
import sys
import timeit

show_output = True
num_of_nono_to_solve = 500

class ConstraintSolver():
    def permutate(self, seg, space):
        if not seg or seg == [[]]:
            return [['_'] * space]
        ret = []
        for x in xrange(1, space - len(seg) + 2):
            for last in self.permutate(seg[1:], space - x):
                ret.append(['_'] * x + seg[0] + last)
        return ret


    def propagate(self, a_list, size, count):
        done = False
        columns = a_list[size:]
        rows = a_list[:size]
        while not done:
            pre_col = list(columns)
            pre_row = list(rows)
            for row_index, row in enumerate(rows):
                if len(row) == 1:
                    for char_index, char in enumerate(row[0]):
                        tmp = []
                        for col in columns[char_index]:
                            if col[row_index] == char:
                                tmp.append(col)
                        if len(tmp) == 0:
                            return True
                        columns[char_index] = tmp
            for col_index, col in enumerate(columns):
                if len(col) == 1:
                    for char_index, char in enumerate(col[0]):
                        tmp = []
                        for row in rows[char_index]:
                            if row[col_index] == char:
                                tmp.append(row)
                        if len(tmp) == 0:
                            return True
                        rows[char_index] = tmp
            if rows == pre_row and columns == pre_col:
                break

        for index, var in enumerate(a_list):
            if index > size - 1:
                a_list[index] = columns[index - size]
            else:
                a_list[index] = rows[index]
        return False


    def csp(self, a_list, size, count):
        index = 0
        for i, v in enumerate(a_list):
            if len(v) > 1:
                index = i
                break
        flag = False
        for v in a_list[index]:
            a_list_copy = []
            for a_l in a_list:
                a_list_copy.append(list(a_l))
            a_list_copy[index] = [v]
            back_track = self.propagate(a_list_copy, size, count)
            if not back_track:
                unique = True
                for e, x in enumerate(a_list_copy):
                    if len(x) > 1 and e < size:
                        unique = False
                        break
                if unique:
                    if show_output:
                        self.nice_print(a_list_copy, size)
                    return True
                flag = self.csp(a_list_copy, size, count + 1)
                if flag:
                    break
        return flag


    def nice_print(self, board, size):
        for i, x in enumerate(board):
            if i < size:
                print ''.join(x[0])
            else:
                return


    def plain_print(self, nested):
        for row in nested:
            print row


    def solve(self, row_constrain, col_constrain, size):
        row = [map(int, row.split(' ')) for row in row_constrain]
        constrain = [map(int, col.split(' ')) for col in col_constrain]
        row_size, col_size = size.strip().split(' ')
        s = timeit.default_timer()
        try:
            a_list = []
            for r in row:
                l = self.permutate([['*'] * i for i in r],
                    int(col_size) + 1 - sum(r))
                a_list.append(map(lambda x: x[1:], l))
            for r in constrain:
                l = self.permutate([['*'] * i for i in r],
                    int(col_size) + 1 - sum(r))
                a_list.append(map(lambda x: x[1:], l))
            self.csp(a_list, int(row_size), 0)
            run_time = timeit.default_timer() - s
            if show_output:
                print 'run time:', run_time
            return run_time
        except KeyboardInterrupt:
            self.nice_print(tree, size)
            sys.exit()


    def read_board(self, config):
        size = next(config, None)
        count = 0
        run_times = []
        while size:
            count += 1
            row, col = size.strip().split(' ')
            row_constrain, col_constrain = [], []
            for i in range(int(row)):
                row_constrain.append(next(config).strip())
            for i in range(int(col)):
                col_constrain.append(next(config).strip())
            run_times.append(self.solve(row_constrain, col_constrain, size))
            if show_output:
                print '---line-split----'
            size = next(config, None)
            if size == '\n':
                size = next(config, None)
            if count == num_of_nono_to_solve:
                print 'solved: %d nonos' % num_of_nono_to_solve
                break
        print 'avg run time:', sum(run_times) / num_of_nono_to_solve



if __name__ == '__main__':
    solver = ConstraintSolver()
    data = ["16 16", "0","14","1 1","1 1","1 1","1 1 1 1 1","1 1","1 1","1 1","1 1 1 1 1","1 1","1 1","1 1","14","0","16","1","13 1","1 1 1","1 1 1","1 1 1 1","1 1 1","1 1 1 1 1","1 1 1","1 1 1 1","1 1 1","1 1 1","1 1 1 1 1","1 1 1","1 1 1","13 1","1"]
    solver.read_board(iter(data))
