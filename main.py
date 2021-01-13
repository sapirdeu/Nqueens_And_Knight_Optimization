from algorithm import HillClimbing

"""
Create dictionary of chess pieces.
input: file name
output: dictionary of chess pieces. For example: {'KNIGHT': 2, 'QUEEN': 6}
"""
def file_handler(file_name):
    with open(file_name) as fin:
        file = []
        for line in fin.readlines():
            file.append(line.split('\n')[0])

    file_encoded = [x.split() for x in file]

    result_dict = {}
    for line in file_encoded:
        result_dict[line[0]] = int(line[1])

    return result_dict

# Main.
file_name = raw_input("Enter the file name: ")
request = file_handler(file_name)

print("Choose your desired algorithm:")
print("1. First Choice Hill Climbing")
print("2. Stochastic Hill Climbing")

choice = int(raw_input("your choice: "))

if choice == 1: # First choice hill climbing
    maxIter = int(raw_input("Insert max iterations: "))
    HillClimbing(request, 1, maxIter)
elif choice == 2: # Stochastic choice hill climbing
    maxIter = int(raw_input("Insert max iterations: "))
    HillClimbing(request, 2, maxIter)