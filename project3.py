import numpy 
import json


#function to import json dictionaries from external txt files
def import_dict_from_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            dictionary = json.loads(data)
            return dictionary
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{file_path}'.")
        return None

def calculate_probabilities(parameters, data, utilities):
    """
    args:
    parameters:A dictionary containing the β coefficients.
    data:A dictionary containing the β coefficients.
    utilities:A list of functions that define the deterministic utilities for each alternative based on the given parameters and data.
    
    output:
    dictionary containing probabilities for each class

    """
    probabilities = {}
    utility = []
    # """iterating through the utility function list and passing values and storing them"""
    for alt in utilities:
        utility.append(alt(data, parameters))
    """calculating the denominator term"""
    sigma = (data['AV1']*numpy.exp(utility[0]) + data['AV2']*numpy.exp(utility[1]) + data['AV3']*numpy.exp(utility[2]))
    """"calculating the probability and storing in dictionary"""
    for i in range(len(utility)):
        probability = (data['AV'+str(i+1)]*numpy.exp(utility[i])) /sigma
        # Add the probability to the dictionary
        probabilities['probability'+str(i+1)] = probability
    
    return probabilities

# """calculating deterministic utility"""
def utility1(data, params):
    return params['beta01'] + params['beta1'] * data['X1'] + params['betaS1_13'] * data['S1']
def utility2(data, params):
    return params['beta02'] + params['beta2'] * data['X2'] + params['betaS1_23'] * data['S1']
def utility3(data, params):
    return params['beta03'] + params['beta1'] * data['Sero'] + params['beta2'] * data['Sero']



#importing datafiles
data = import_dict_from_txt("data.txt")
parameters = import_dict_from_txt("parameters.txt")
if data:
    print("data imported successfully:")
if parameters:
    print("parameter imported successfully:")
# """"converting to numpy arrays"""
for key in data:
    data[key]=numpy.array(data[key])
# print(data)
# print(parameters)
# """function call"""
probabilities = calculate_probabilities(parameters, data, [utility1, utility2, utility3])
print(probabilities)
# """writing to txt file"""
with open('probabilities.txt', 'w') as f:
    for alt, prob in probabilities.items():
        f.write(f"{alt}: {prob.tolist()}\n")






