import random
import pandas as pd
import math
import copy
import time


data_path = 'gr48.txt'
iterations = 200000


def get_distance_matrix(path):
    data = pd.read_csv(path, header=None).values.tolist()[0]
    length = len(data)
    point_number = int(0.5 * (-1 + math.sqrt(1 + 8 * length)))
    distance_matrix = [[0 for i in range(point_number)] for j in range(point_number)]
    for i in range(point_number):
        for j in range(i + 1):
            distance_matrix[i][j] = data[int(i * (i + 1) / 2) + j]
            distance_matrix[j][i] = distance_matrix[i][j]
    return distance_matrix


def function(path, distance_matrix):
    distance = 0
    for i in range(len(path) - 1):
        distance += distance_matrix[path[i]][path[i + 1]]
    distance += distance_matrix[path[0]][path[-1]]
    if data_path == 'gr17.txt':
        distance -= 93
    else:
        distance -= 900
    return distance


def init(number, distance_matrix):
    point_number = len(distance_matrix)
    population = list()
    values = list()
    for i in range(number):
        individual = list()
        current_point = random.randint(0, point_number - 1)
        individual.append(current_point)
        for j in range(point_number - 1):
            residual_point = list(set([k for k in range(point_number)]) - set(individual))
            residual_point_distance = [distance_matrix[current_point][k] for k in residual_point]
            current_point = residual_point[residual_point_distance.index(min(residual_point_distance))]
            individual.append(current_point)
        value = function(individual, distance_matrix)
        values.append(value)
        population.append(individual)

    return population, values


def crossover(individual1, individual2):
    length = len(individual1)
    max_index = random.randint(0, length - 1)
    min_index = random.randint(0, length - 1)
    max_index = max(min_index, max_index)
    min_index = min(min_index, max_index)

    individual1 = copy.deepcopy(individual1)
    individual2 = copy.deepcopy(individual2)

    temp1 = individual1[min_index:max_index]
    temp2 = individual2[min_index:max_index]
    for i in temp2:
        individual1.remove(i)
    for i in temp1:
        individual2.remove(i)
    individual1 = individual1[:max_index - length] + temp2 + individual1[max_index - length:]
    individual2 = individual2[:max_index - length] + temp1 + individual2[max_index - length:]
    return individual1, individual2


def variation(individual):
    length = len(individual)
    max_index = random.randint(0, length - 1)
    min_index = random.randint(0, length - 1)
    max_index = max(min_index, max_index)
    min_index = min(min_index, max_index)

    individual = copy.deepcopy(individual)

    temp = individual[min_index:max_index]
    random.shuffle(temp)
    individual = individual[:min_index] + temp + individual[max_index:]
    return individual


def select(values):
    copy = values[:]
    max1 = values.index(min(values))
    copy.pop(max1)
    max2 = values.index(min(copy))
    return max1, max2


def main():
    distance_matrix = get_distance_matrix(data_path)
    population, values = init(5, distance_matrix)
    min_value_index = list()
    while True:
        individual1_index, individual2_index = select(values)
        if random.random() < 0.7:
            individual1, individual2 = crossover(population[individual1_index], population[individual2_index])

            value1, value2 = function(individual1, distance_matrix), function(individual2, distance_matrix)

            max_index = values.index(max(values))
            if values[max_index] > value1:
                population[max_index] = individual1
                values[max_index] = value1

            max_index = values.index(max(values))
            if values[max_index] < value2:
                population[max_index] = individual2
                values[max_index] = value2
        else:
            individual = variation(population[individual1_index])
            value = function(individual, distance_matrix)

            max_index = values.index(max(values))
            if values[max_index] < value:
                population[max_index] = individual
                values[max_index] = value
        min_index = values.index(min(values))
        min_value_index.append(min_index)
        if len(min_value_index) > iterations and min_value_index[-1] == min_value_index[-iterations]:
            break

    return population[min_index], values[min_index]


if __name__ == '__main__':
    start = time.time()
    individual, value = main()
    end = time.time()
    print(end - start)
    print(individual)
    print(value)
