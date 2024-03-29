import xmltodict

print("Welcome to the FSMD simulator! - Version 1 - Designed by Kris, Mads and Ben")

while True: # Test for interation input as int
    try:
        iteration_input = int(input("Insert Cycle: "))
        if iteration_input == 69:
            print("Nice.")
        break
    except ValueError:
        print("that was not a valid number.  Try again...")


while True: # Test for description file input
    try: 
        descr_path = input("Insert description XML: ")
        if descr_path == "uwu": # Don't Ask
            print("Heresy")
        elif descr_path == "description XML":
            print("Very funny")
        elif len(descr_path) != 0:
            with open(descr_path) as fd:
                fsmd_des = xmltodict.parse(fd.read())
            break 
    except FileNotFoundError: 
        print("No description file was found please try again")



while True: # Test for stimuli file, option to avoid stimuli input
    try: 
        stim_path = input("Insert stimuli XML. If no stimuli needed, write 'BREAK': ")
        if stim_path == "stimuli XML":
            print("Your'e a really clever guy, aren't you?")
        elif stim_path == "BREAK":
            break 
        elif len(stim_path) != 0:
            with open(stim_path) as fd:
                fsmd_stim = {}
                fsmd_stim = xmltodict.parse(fd.read())
            break 
    except FileNotFoundError: 
        print(" No stimuli file was found please try again")






print("\n--FSMD description" ) 
print(fsmd_des)
while True:  # Test incase BREAK was written in line 28
    try: 
        print(fsmd_stim)
        break 
    except NameError: 
        pass 
print ("Thank for using The FSDM designed by Kris, Mads and Ben")

# Description:
# The 'states' variable of type 'list' contains the list of all states names.

states = fsmd_des['fsmddescription']['statelist']['state']
print("States:")
for state in states:
    print('  ' + state)
#
# Description:
# The 'initial_state' variable of type 'string' contains the initial_state name.
#
initial_state = fsmd_des['fsmddescription']['initialstate']
print("Initial state:")
print('  ' + initial_state)

#
# Description:
# The 'inputs' variable of type 'dictionary' contains the list of all inputs
# names and value. The default value is 0.
#
inputs = {}
if(fsmd_des['fsmddescription']['inputlist'] is None):
    inputs = {}
    #No elements
else:
    if type(fsmd_des['fsmddescription']['inputlist']['input']) is str:
        # One element
        inputs[fsmd_des['fsmddescription']['inputlist']['input']] = 0
    else:
        # More elements
        for input_i in fsmd_des['fsmddescription']['inputlist']['input']:
            inputs[input_i] = 0
print("Inputs:")
for input_i in inputs:
    print('  ' + input_i)

#
# Description:
# The 'variables' variable of type 'dictionary' contains the list of all variables
# names and value. The default value is 0.
#
variables = {}
if(fsmd_des['fsmddescription']['variablelist'] is None):
    variables = {}
    #No elements
else:
    if type(fsmd_des['fsmddescription']['variablelist']['variable']) is str:
        # One element
        variables[fsmd_des['fsmddescription']['variablelist']['variable']] = 0
    else:
        # More elements
        for variable in fsmd_des['fsmddescription']['variablelist']['variable']:
            variables[variable] = 0
print("Variables:")
for variable in variables:
    print('  ' + variable)

#
# Description:
# The 'operations' variable of type 'dictionary' contains the list of all the
# defined operations names and expressions.
#
operations = {}
if(fsmd_des['fsmddescription']['operationlist'] is None):
    operations = {}
    #No elements
else:
    for operation in fsmd_des['fsmddescription']['operationlist']['operation']:
        if type(operation) is str:
            # Only one element
            operations[fsmd_des['fsmddescription']['operationlist']['operation']['name']] = \
                fsmd_des['fsmddescription']['operationlist']['operation']['expression']
            break
        else:
            # More than 1 element
            operations[operation['name']] = operation['expression']
print("Operations:")
for operation in operations:
    print('  ' + operation + ' : ' + operations[operation])

#
# Description:
# The 'conditions' variable of type 'dictionary' contains the list of all the
# defined conditions names and expressions.
#
conditions = {}
if(fsmd_des['fsmddescription']['conditionlist'] is None):
    conditions = {}
    #No elements
else:
    for condition in fsmd_des['fsmddescription']['conditionlist']['condition']:
        if type(condition) is str:
            #Only one element
            conditions[fsmd_des['fsmddescription']['conditionlist']['condition']['name']] = fsmd_des['fsmddescription']['conditionlist']['condition']['expression']
            break
        else:
            #More than 1 element
            conditions[condition['name']] = condition['expression']
print("Conditions:")
for condition in conditions:
    print('  ' + condition + ' : ' + conditions[condition])

#
# Description:
# The 'fsmd' variable of type 'dictionary' contains the list of dictionaries,
# one per state, with the fields 'condition', 'instruction', and 'nextstate'
# describing the FSMD transition table.
#
fsmd = {}
for state in states:
    fsmd[state] = []
    for transition in fsmd_des['fsmddescription']['fsmd'][state]['transition']:
        if type(transition) is str:
            #Only one element
            fsmd[state].append({'condition': fsmd_des['fsmddescription']['fsmd'][state]['transition']['condition'],
                                'instruction': fsmd_des['fsmddescription']['fsmd'][state]['transition']['instruction'],
                                'nextstate': fsmd_des['fsmddescription']['fsmd'][state]['transition']['nextstate']})
            break
        else:
            #More than 1 element
            fsmd[state].append({'condition' : transition['condition'],
                                'instruction' : transition['instruction'],
                                'nextstate' : transition['nextstate']})
print("FSMD transitions table:")
for state in fsmd:
    print('  ' + state)
    for transition in fsmd[state]:
        print('    ' + 'nextstate: ' + transition['nextstate'] + ', condition: ' + transition['condition'] + ', instruction: ' + transition['instruction'])


#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionary 'inputs'
#
def execute_setinput(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    inputs[target] = eval(expression, {'__builtins__': None}, inputs)
    return


#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionaries 'variables' and 'inputs'
#
def execute_operation(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    variables[target] = eval(expression, {'__builtins__': None}, merge_dicts(variables, inputs))
    return


#
# Description:
# This function executes a list of operations passed as string and spaced by
# a single space using the expression defined in the dictionary 'operations'
#
def execute_instruction(instruction):
    if instruction == 'NOP' or instruction == 'nop':
        return
    instruction_split = instruction.split(' ')
    for operation in instruction_split:
        execute_operation(operations[operation])
    return


#
# Description:
# This function evaluates a Python compatible boolean expressions of
# conditions passed as string using the conditions defined in the variable 'conditions'
# and using the operands stored in the dictionaries 'variables' and 'inputs
# It returns True or False
#
def evaluate_condition(condition):
    if condition == 'True' or condition=='true' or condition == 1:
        return True
    if condition == 'False' or condition=='false' or condition == 0:
        return False
    condition_explicit = condition
    for element in conditions:
        condition_explicit = condition_explicit.replace(element, conditions[element])
    #print('----' + condition_explicit)
    return eval(condition_explicit, {'__builtins__': None}, merge_dicts(variables, inputs))


#
# Description:
# Support function to merge two dictionaries.
#
def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


#######################################
# Start to simulate
cycle = 0
finishCycle = 0
state = initial_state
repeat = True


print('\n---Begin Simulation---')

#
# Description:
# Beginning of state table 
#
    
while ((cycle+1) < iteration_input) and (repeat == True):
    print("-----------------------------------------")
    print("Cycle Number: {}".format(cycle))
    print("Current State: " + state)
    print("Current Variables: {}".format(variables))
    try:
        if (not (fsmd_stim['fsmdstimulus']['setinput'] is None)):
            for setinput in fsmd_stim['fsmdstimulus']['setinput']:
                if type(setinput) is str:
                    cycle += 1
                    if int(fsmd_stim['fsmdstimulus']['setinput']['cycle']) == cycle:
                        execute_setinput(fsmd_stim['fsmdstimulus']['setinput']['expression'])
                    break
                else:
                    # More than 1 element
                    if int(setinput['cycle']) == cycle:
                        execute_setinput(setinput['expression'])
    except:
        pass
#
# Description:
# Iterate over current state operations, execute the required then change variable state
#
    try:
        for i in fsmd[state]:
            if evaluate_condition(i['condition']):
                execute_instruction(i['instruction'])
                print("Instruction to be Executed: {}".format(i['instruction']))
                state = i['nextstate']
                break
    except:
        pass

    cycle += 1

    try:
        if (not (fsmd_stim['fsmdstimulus']['endstate'] is None)):
            if state == fsmd_stim['fsmdstimulus']['endstate']:
                print('End-state reached.')
                repeat = False
    except:
        pass

print("\n-----------------------------------------\n")
print("Simulation Complete")
print("Final State: " + state)
print("Computed Cycles: {}".format(cycle + 1))
print("Final Variable Values: {}".format(variables))

######################################
######################################

print('\n---End Simulation---')