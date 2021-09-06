import os.path

#On Github, output_by_subject and output_individual_roll folders already have the output files

#Function to create a comma-seperated string from string list
#[1901EE43, 5, CS384, Open-Elective] -> 1901EE43,5,CS384,Open-Elective
def create_string (row_items, relevant_cols):
    ans = ""
    for col in relevant_cols:
        ans += row_items[col] + ","
    ans = ans[:-1]
    return ans

#Function to output the row in the appropriate file
def output(output_file, col_headings, row_items, relevant_cols):

    row_items = create_string(row_items,relevant_cols)
    col_headings = create_string(col_headings,relevant_cols)
    if not os.path.isfile(output_file):                     #If a file doesn't exist, create it
        with open(output_file,'x') as target_file:
            target_file.write(col_headings)                 # Put column headings
    else:                                                   #Append the row items to the file
        with open(output_file,'a') as target_file:
            target_file.write(row_items)

    return

data_file = open("regtable_old.csv","r")                    #Open the file
col_headings = data_file.readline().split(',')              #Get the Top headings
relevant_cols = [0,1,3,8]                                   #Columns we care for

for curr_line in data_file:
    row_items = curr_line.split(',')
    output_file = "output_by_subject\\"+ row_items[3] + ".csv"
    output(output_file,col_headings,row_items,relevant_cols)
    output_file = "output_individual_roll\\" + row_items[0] + ".csv"
    output(output_file,col_headings,row_items,relevant_cols)

