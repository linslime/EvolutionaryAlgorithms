import math
import random
import copy
import time


x1_min = -3.0
x1_max = 12.1
x2_min = 4.1
x2_max = 5.8
precision = 4
iterations = 100000


def function(x1, x2):
    return 21.5 + x1 * math.sin(4 * math.pi * x1) + x2 * math.sin(20 * math.pi * x2)


def decimal_to_binary(decimal):
    decimal = math.pow(10, precision) * decimal
    decimal = int(decimal)
    binary = bin(decimal)
    binary = list(binary[2:])
    if binary[0] == 'b':
        binary = binary[1:]
    return binary


def binary_to_decimal(binary):
    return round(int(''.join(str(bit) for bit in binary), 2) / math.pow(10, precision), precision)


def crossover(individual1, individual2, size):
    def crossover_one_var(one, two, x_min, x_max):
        one = one - x_min
        two = two - x_min
        one = decimal_to_binary(one)
        two = decimal_to_binary(two)
        if len(one) == len(two):
            pass
        elif len(one) < len(two):
            for i in range(len(two) - len(one)):
                one.insert(0, 0)
        elif len(one) > len(two):
            for i in range(len(one) - len(two)):
                two.insert(0, 0)
        for i in range(100):
            temp_one = one[:]
            temp_two = two[:]
            start = random.randint(0, len(one) - 1)
            end = random.randint(0, len(one) - 1)
            start = min(start, end)
            end = max(start, end)

            temp = temp_one[start:end]
            temp_one[start:end] = two[start:end]
            temp_two[start:end] = temp
            temp_one = binary_to_decimal(temp_one)
            temp_two = binary_to_decimal(temp_two)
            temp_one = temp_one + x_min
            temp_two = temp_two + x_min
            if temp_one > x_min and temp_one < x_max and temp_two > x_min and temp_two < x_max:
                one = temp_one
                two = temp_two
                return one, two

        one = binary_to_decimal(one)
        two = binary_to_decimal(two)
        one = one + x_min
        two = two + x_min
        return one, two

    temp_individual1 = copy.deepcopy(individual1)
    temp_individual2 = copy.deepcopy(individual2)
    for i in range(len(individual1)):
        temp_individual1[i], temp_individual2[i] = crossover_one_var(individual1[i], individual2[i], size[i][0], size[i][1])
    return temp_individual1, temp_individual2


def variation(individual, size):
    def variation_one_var(data, x_min, x_max):
        data = data - x_min
        data = decimal_to_binary(data)
        for i in range(100):
            temp_data = data[:]
            index = [i for i in range(len(temp_data))]
            random.shuffle(index)
            index = index[:random.randint(0, len(index) - 1)]
            for i in index:
                if temp_data[i] == '0':
                    temp_data[i] = '1'
                else:
                    temp_data[i] = '0'
            temp_data = binary_to_decimal(temp_data)
            temp_data = temp_data + x_min
            if temp_data > x_min and temp_data < x_max:
                return temp_data

        data = binary_to_decimal(data)
        data = data + x_min
        return data

    temp_individual = copy.deepcopy(individual)
    for i in range(len(individual)):
        temp_individual[i] = variation_one_var(individual[i], size[i][0], size[i][1])
    return temp_individual


def init(number, size):
    population = [[round(random.uniform(data[0], data[1]), precision) for data in size] for i in range(number)]
    values = [function(*individual) for individual in population]
    return population, values


def select(population):
    index = [i for i in range(len(population))]
    random.shuffle(index)
    return index[0], index[1]


def get_min_index(value):
    value1 = value.index(min(value))
    return value1


def main():
    size = [[x1_min, x1_max], [x2_min, x2_max]]
    population, values = init(100, size)

    max_value_index = list()
    while True:
        individual1_index, individual2_index = select(population)
        if random.random() < 0.7:
            individual1, individual2 = crossover(population[individual1_index], population[individual2_index], size)
            value1, value2 = function(*individual1), function(*individual2)

            min_index = get_min_index(values)
            if values[min_index] < value1:
                population[min_index] = individual1
                values[min_index] = value1

            min_index = get_min_index(values)
            if values[min_index] < value2:
                population[min_index] = individual2
                values[min_index] = value2
        else:
            individual = variation(population[individual1_index], size)
            value = function(*individual)
            min_index = get_min_index(values)
            if values[min_index] < value:
                population[min_index] = individual
                values[min_index] = value

        max_index = values.index(max(values))
        max_value_index.append(max_index)
        if len(max_value_index) > iterations and max_value_index[-1] == max_value_index[-iterations]:
            break
    return population[max_index], values[max_index]


if __name__ == '__main__':
    start = time.time()
    [x1, x2], value = main()
    end = time.time()
    print(end - start)
    print(x1, x2, value)
