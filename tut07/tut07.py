import pandas as pd
import re

#Check if roll number is valid
def is_rno(rno):
	return re.match(r"\d\d\d\d\w\w\d\d",rno)

#Seperate L-T-P from a single string 
def get_ltp(string_ltp):
	ltp = string_ltp.split('-')
	return ltp

#Get all the expected feedbacks in a set
def get_full_list(course_taken):
	res_list = set()

	for index, row in course_taken.iterrows():
		course = row["subno"]
		if is_rno(row["rollno"]):
			if course_ltp[course][0] != "0":
				res_list.add((row["rollno"],row["subno"],"1"))
			if course_ltp[course][1] != "0":
				res_list.add((row["rollno"],row["subno"],"2"))
			if course_ltp[course][2] != "0":
				res_list.add((row["rollno"],row["subno"],"3"))

	return res_list

#Get all existing feedbacks in a set
def get_done_list (fb_info):
	res_list = set()
	for index, row in fb_info.iterrows():
		if is_rno(row["stud_roll"]):
			res_list.add((row["stud_roll"],row["course_code"],str(row["feedback_type"])))
	return res_list


#Get all files in dataframes
fb_info = pd.read_csv("course_feedback_submitted_by_students.csv")
course_master = pd.read_csv("course_master_dont_open_in_excel.csv")
student_info = pd.read_csv("studentinfo.csv")
course_taken = pd.read_csv("course_registered_by_all_students.csv")
output_file = pd.DataFrame(columns = ["Roll Number","Registered Sem","Scheduled Sem","Course Code","Name","Email","AEmail","Contact"])

# [Roll Number][Course] -> (Reg Sem, Sched Sem)
sch_sem = {}
for index,row in course_taken.iterrows():
	if is_rno(row["rollno"]):
		if row["rollno"] not in sch_sem:
			sch_sem[row["rollno"]] = {}

		sch_sem[row["rollno"]][row["subno"]] = (row["register_sem"],row["schedule_sem"])

# [Roll Number] -> All Student Info
stud_info = {}
for index,row in student_info.iterrows():
	stud_info[row["Roll No"]] = {}
	stud_info[row["Roll No"]] = row

# [Course] -> L-T-P
course_ltp = {}
for index, row in course_master.iterrows():
	course_ltp[row["subno"]] = get_ltp(row["ltp"])

full_list = get_full_list(course_taken)
done_list = get_done_list(fb_info)

#Manage any discrepancy, if any
full_list = full_list | done_list

#Rem List = Dif in done_list and full_list
rem_list = done_list ^ full_list

# Fill all the remaining feedback entries, 
# along with other info, in a dataframe
for entry in rem_list:
	rno = entry[0]
	course = entry[1]
	feed_type = entry[2]
	reg_sem = sch_sem[rno][course][0]
	sched_sem = sch_sem[rno][course][1]

	name = "NA_IN_STUDENTINFO"
	mail = "NA_IN_STUDENTINFO"
	amail = "NA_IN_STUDENTINFO"
	contact = "NA_IN_STUDENTINFO"
	if rno in stud_info:
		name = stud_info[rno]["Name"]
		mail = stud_info[rno]["email"]
		amail = stud_info[rno]["aemail"]
		contact = stud_info[rno]["contact"]
	new_row = {"Roll Number":rno, "Registered Sem":reg_sem,"Scheduled Sem":sched_sem,"Course Code":course,"Email":mail,"AEmail":amail,"Contact":contact,"Name":name};
		
	output_file = output_file.append(new_row,ignore_index=True)

#Put Dataframe in xlsx
output_file.to_excel("course_feedback_remaining.xlsx",index=False)