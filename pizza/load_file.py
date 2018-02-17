def load_file(filename):
    result = {}

    with open(filename) as f:
        lines = f.read().splitlines()

        config = lines[0]
        result["rows"] = config[0]
        result["columns"] = config[1]
        result["minimum_ingredient"] = config[2]
        result["max_cells"] = config[3]

        pizza = []
        for line in lines[1:]:
            pizza.append(list(line))

        result["pizza"] = pizza

    return result 
