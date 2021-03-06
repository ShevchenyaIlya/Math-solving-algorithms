import numpy


class SystemOfEquations:
    """Class for manipulate with basic operation with matrix to computing system and solve her answers."""

    def __init__(self):
        self.matrix_of_coefficients = []  # list of tuples, where first element - float value, second - variable
        self.value_vector = []  # values after equal mark
        self.equations_count = 4
        self.variables = []  # hole list of variables using in system
        self.answers = []  # results of solving system
        self.changed_matrix = []
        self.absolute_error = 1e-3  # Value from task condition
        self.absolute_decision_error = 0
        self.relative_decision_error = 0

    def input_system_of_equations(self):
        """Method for input system, based on transforming strings in format easy for computing and solving,
        include some transformation like deleting whitespace, separating values and variables.
        """

        system_rows = []
        print("Enter system for solving it using Gauss method: ")
        for num in range(self.equations_count):
            system_rows.append(input())

        counter = 0
        for row in system_rows:
            temp = row.split("=")
            self.value_vector.append(float(temp[1].strip(" ")))
            system_rows[counter] = temp[0].strip(" ")
            counter += 1

        list_of_rows = []
        for system_row in system_rows:
            num_and_variable = system_row.split("+")
            counter = 0
            for symbol in num_and_variable:
                num_and_variable[counter] = symbol.strip(" ")
                counter += 1
            list_of_rows.append(num_and_variable)

        for row in list_of_rows:
            list_of_tuples = []
            for element in row:
                parts = element.split("*")
                if not parts[1].strip(" ") in self.variables:
                    self.variables.append(parts[1].strip(" "))
                list_of_tuples.append((float(parts[0].strip(" ")), parts[1].strip(" ")))
            self.matrix_of_coefficients.append(list_of_tuples)

    def transform_matrix(self):
        counter = 0
        for row in self.matrix_of_coefficients:
            changed_row = []
            for element in row:
                changed_row.append(element[0])
            changed_row.append(self.value_vector[counter])
            self.changed_matrix.append(changed_row)
            counter += 1
        print("Matrix of coefficients: ")
        for row in self.changed_matrix:
            print(row)

    def computing(self, first, second):
        for iterator in range(first, second):
            subtraction_by = self.changed_matrix[iterator][first - 1] / self.changed_matrix[first - 1][first - 1]
            for element in range(first - 1, second + 1):
                self.changed_matrix[iterator][element] -= subtraction_by * self.changed_matrix[first - 1][element]

    def find_answers(self):
        self.answers.append((self.changed_matrix[-1][-1] / self.changed_matrix[-1][-2], self.variables[-1]))
        self.answers.append(((self.changed_matrix[-2][-1] - self.changed_matrix[-2][-2] * self.answers[0][0]) /
                             self.changed_matrix[-2][-3], self.variables[-2]))
        self.answers.append(((self.changed_matrix[-3][-1] - self.changed_matrix[-3][-2]
                              * self.answers[0][0] - self.changed_matrix[-3][-3] * self.answers[1][0])
                             / self.changed_matrix[-3][-4], self.variables[-3]))
        self.answers.append(((self.changed_matrix[-4][-1] - self.changed_matrix[-4][-2]
                              * self.answers[0][0] - self.changed_matrix[-4][-3]
                              * self.answers[1][0] - self.changed_matrix[-4][-4]
                              * self.answers[2][0]) / self.changed_matrix[-4][-5], self.variables[-4]))

    def output_result(self):
        print("Results of computing, we get such answers:")
        for number in range(3, -1, -1):
            print(self.answers[number][1], "=", self.answers[number][0])

    def result(self):
        for computing_step in range(self.equations_count - 1):
            self.computing(computing_step + 1, self.equations_count)
        self.find_answers()
        self.output_result()

    def coefficient_matrix(self):
        """Transforming primary data storage into matrix of float values."""

        value_matrix = []
        for row in self.matrix_of_coefficients:
            value_row = []
            for tuple_ in row:
                value_row.append(tuple_[0])
            value_matrix.append(value_row)
        return value_matrix

    def approve_answers(self):
        """Function for approving answers that we get from our solving. Use numpy module and his solve function."""

        value_matrix = self.coefficient_matrix()
        print("Vector of answers using numpy: ", numpy.linalg.solve(value_matrix, self.value_vector))

    def reverse_matrix(self):
        value_matrix = self.coefficient_matrix()
        result_matrix = [list(numpy.linalg.solve(value_matrix, [1, 0, 0, 0])),
                         list(numpy.linalg.solve(value_matrix, [0, 1, 0, 0])),
                         list(numpy.linalg.solve(value_matrix, [0, 0, 1, 0])),
                         list(numpy.linalg.solve(value_matrix, [0, 0, 0, 1]))]
        result_matrix = numpy.transpose(result_matrix)
        print("Reversed matrix: ", result_matrix, sep="\n")

    def reverse_matrix_numpy(self):
        value_matrix = self.coefficient_matrix()
        result = numpy.linalg.inv(value_matrix)
        return result

    def max_sum_of_element_in_collection(self, reverse):
        if reverse:
            value_matrix = self.reverse_matrix_numpy()
        else:
            value_matrix = self.coefficient_matrix()
        for row in value_matrix:
            counter = 0
            for element in row:
                row[counter] = abs(element)
                counter += 1
        vector_of_sum = []
        for row in value_matrix:
            vector_of_sum.append(sum(row))
        return max(vector_of_sum)

    def error_rating(self):
        matrix_rate = self.max_sum_of_element_in_collection(False)
        reverse_matrix_rate = self.max_sum_of_element_in_collection(True)
        max_free_value = max(self.value_vector)
        relative_error = self.absolute_error / max_free_value
        self.absolute_decision_error = self.absolute_error * reverse_matrix_rate
        self.relative_decision_error = matrix_rate * reverse_matrix_rate * relative_error
        print("Absolute decision error:", self.absolute_decision_error)
        print("Relative decision error:", self.relative_decision_error)


if __name__ == "__main__":
    system = SystemOfEquations()
    system.input_system_of_equations()
    system.transform_matrix()
    system.result()
    system.approve_answers()
    system.reverse_matrix()
    system.error_rating()