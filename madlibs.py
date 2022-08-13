import random
import pickle
    
    
def capitalize_sentences(sentence):
    ''' (str) -> str
    Returns sentence with the first letter of each sentence capitalized.
    '''
    sentence_list = sentence.split(" ") 
    
    for index, element in enumerate(sentence_list):
        if sentence_list[index-1][len(sentence_list[index-1])-1] in ".?!": #Checks if the previous word ends with a . or ! or ? 
            temp_new_string = element[0].upper() + element[1:] #Capitalizes the word in the current index
            sentence_list[index] = temp_new_string #Replaces the old word with the new capitalized word
        else: 
            continue
    
    capital_sentence = " ".join(sentence_list)
    return capital_sentence



def capitalize_sentence_grid(grid):
    ''' (list) -> list
    Returns the nested list with the first word of a new sentence capitalized. 
    '''
    new_grid = [] #Makes a new list to ensure the old nested list remains unmodified
    
    for element in grid: #Creates a deep copy of the original nested list
        new_element = [] #Saves the nested elements into a new inner list 
        for inner_element in element:
            new_element.append(inner_element) #Appends the nested elements to the inner list
        new_grid.append(new_element) #Appends the inner lists to the outer list

    for grid_index, grid_list in enumerate(new_grid): #Iterates through the elements of the list
        for list_index, element in enumerate(grid_list): #Iterates through the inner elements of the nested list
            if element[len(element)-1] in ".!?": #Checks if the last character of the string is a . or ! or ? 
                
                if (grid_index <= len(new_grid)-1) and (list_index < len(grid_list)-1): #If the word with the punctuation is not the last word in the inner list
                    temp_new_string = grid_list[list_index+1][0].upper() + grid_list[list_index+1][1:] #Capitalize next element of the inner list
                    grid_list[list_index+1] = temp_new_string #Modify the list with the capitalized word
                
                elif grid_index == len(new_grid)-1 and list_index == len(grid_list)-1: #Checks if the last word in the entire list ends with . or ! or ?
                    temp_new_string = new_grid[0][0][0].upper() + new_grid[0][0][1:] #Capitalize the first word in the whole list and saves it to a variable
                    new_grid[0][0] = temp_new_string #Adds the capitalized first word to the new list
                
                else: #If the punctuated word is the last word in the inner list
                    temp_new_string = new_grid[grid_index+1][0][0].upper() + new_grid[grid_index+1][0][1:] #Move onto the next inner list and capitalize the first word
                    new_grid[grid_index+1][0] = temp_new_string #Modify the list with the capitalized word
            else: 
                continue
    return new_grid



def fill_in_madlib(madlib, dictionary):
    ''' (str, dict) -> str
    Returns the filled madlib string with words from dictionary.
    '''
    if type(madlib) != str or type(dictionary) != dict: #If the inputs are not valid types, raise an error
        raise AssertionError("Argument parameters not valid. Input a string for madlib and a dictionary for dictionary.")
    
    string_no_punc = "" 
    for char in madlib: #Removes all the punctuation from the madlibs string
        if char in ",.!?":
            continue
        else:
            string_no_punc += char
    
    madlib_no_punc_list = string_no_punc.split(" ") 
    
    num_word_replacement_needed = {} 

    for key in dictionary:
        num_word_replacement_needed[key] = [] #Create a dictionary with the keys as the category of words to fill the blank spaces 

    for element in madlib_no_punc_list: 
        for key in dictionary:
            if "[" in element and "]" in element and key in element: #If the empty space is found in the dictionary of word replacements
                if element not in num_word_replacement_needed[key]: #If the empty space has not been counted, add the specific space to the dictionary
                    num_word_replacement_needed[key] += [element]
                else: #If the empty space is in the dictionary, which means it is a repeat, continue onto the next element
                    continue
    
    for key in num_word_replacement_needed:
        if len(num_word_replacement_needed[key]) > len(dictionary[key]):
        #If the number of blank spaces is greater than the sufficient number of words to fill them, raise an error
            raise AssertionError("Not enough word replacement options in dictionary for blank spaces.")
    
    madlib_list = madlib.split(" ")
    word_replaced_dict = {} #Creates a dictionary to stores the words assigned to specific blanks
    used_words = [] #Creates an empty list to store all the words that have been used
    
    for index, element in enumerate(madlib_list):
        start_index = 0
        end_index = 0
        
        bracket_counter = 0 #Keeps count of the number of brackets in the element
        if "[" in element and "]" in element: 
            for char_index, char in enumerate(element): #Iterate through each index of the string to find the index of '[' and of ']'
                if char == "[":
                    start_index += char_index
                    bracket_counter += 1
                if char == "]":
                    end_index += char_index
                    bracket_counter += 1
            
            if bracket_counter % 2 != 0: #If there's an odd number of brackets, that means there is a bracket that is not closed and an error is raised
                raise AssertionError("Unclosed bracket for blank space.")
            
            for key in dictionary:
                if key in element and element[start_index:end_index+1] not in word_replaced_dict: #The annotated blank word is not found in the dictionary
                    replaced_word = random.choice(dictionary[key]) #Choose a random word from its specified list to fill the blank
                    
                    
                    while replaced_word in used_words: #If the word used to fill the blank has been used before, generate another word
                        replaced_word = random.choice(dictionary[key])
                    
                    madlib_list[index] = madlib_list[index].replace(element[start_index:end_index+1], replaced_word) #Replace the blank space with the new word
                    word_replaced_dict[element[start_index:end_index+1]] = replaced_word #Store the word and the annotated blank space word into the dictionary as a key-value pair
                    used_words.append(replaced_word) #Store the used word into a list
                
                elif key in element and element[start_index:end_index+1] in word_replaced_dict: #The annotated blank word is found in the dictionary
                    #Find the value for the annotated blank word (key) in the dictoinary and fill the blank with that word
                    madlib_list[index] = madlib_list[index].replace(element[start_index:end_index+1], word_replaced_dict[element[start_index:end_index+1]])
                
                else:
                    continue
                
    madlib_string = capitalize_sentences(" ".join(madlib_list)) #Join the list of words into a string and add proper capitalization 
    
    if "[" in madlib_string and "]" in madlib_string: #If in the end, there are still '[' and ']' around a annotated blank space in the string, raise an error.
        raise AssertionError("Specified replacement word not found in word replacement dictionary.")
    
    if "[" in madlib_string or "]" in madlib_string: #If there is '[' or ']' in the string, raise an error
        raise AssertionError("Bracket placement error around blank space.")
    
    return madlib_string



def load_and_process_madlib(madlib_filename):
    ''' (str) -> None
    Appends a filled madlib string to a new file that has the original madlib_filename with '_filled' appended to the end.
    '''
    madlib_file = open(madlib_filename, "r") #Open the file and use the read function to obtain a string
    madlib_content = madlib_file.read()
    madlib_file.close()
    
    dictionary_file = open("word_dict.pkl", "rb") #Open the pickle file to access the load function to obtain a word dictionary
    dictionary_content = pickle.load(dictionary_file)
    dictionary_file.close()
    
    filled_madlib = fill_in_madlib(madlib_content, dictionary_content) #Fill the string with words from the word dictionary
    new_file_name = madlib_filename.replace(".", "_filled.") #Create a new file name that has '_filled' at the end
    
    filled_madlib_file = open(new_file_name, "w") #Open the new file name and write the filled madlib string
    filled_madlib_file.write(filled_madlib)
    filled_madlib_file.close()
    
    
    
def generate_comment():
    ''' () -> str
    Chooses a random number from 1-10 and returns a filled madlib string from the file number.
    '''
    k = random.randint(1,10) #Generate a random number that corresponds to the file number to be accessed
    file_name = "madlib" + str(k) + ".txt" #Create a file name that is specific to the number that was generated
    load_and_process_madlib(file_name) #Fill in the string obtained from the specific text file number with the madlib words
    new_file_name = file_name.replace(".", "_filled.")
    
    filled_madlib_file = open(new_file_name, "r") #Open the new text file to obtain the filled madlib string
    filled_madlib_content = filled_madlib_file.read()
    filled_madlib_file.close()
    
    return filled_madlib_content