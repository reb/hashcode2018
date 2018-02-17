import util

def solve(problem):
    return [[0,1,2,3], [1,2,3,4]]





if __name__ == "__main__":
    datasets = ['example', 'small', 'medium', 'big']

    for dataset in datasets:
        
        problem = util.load_file(dataset + '.in')
        solution = solve(problem)
        util.export(dataset, solution)

