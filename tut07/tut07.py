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
def get_expected_fb(course_taken):
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
def get_recieved_fb (fb_info):
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

expected_fb = get_expected_fb(course_taken)
recieved_fb = get_recieved_fb(fb_info)

#Manage any discrepancy, if any
expected_fb = expected_fb | recieved_fb

#Rem List = Dif in recieved_fb and expected_fb
remaining_fb = recieved_fb ^ expected_fb

# Fill all the remaining feedback entries, 
# along with other info, in a dataframe
reported = set()
# Set for avoiding repetitions
for entry in remaining_fb:
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
		
	new_row = {"Roll Number":rno, 
			   "Registered Sem":reg_sem,
			   "Scheduled Sem":sched_sem,
			   "Course Code":course,
			   "Email":mail,
			   "AEmail":amail,
			   "Contact":contact,
			   "Name":name};
		
	if (rno,course) not in reported:
		output_file = output_file.append(new_row,ignore_index=True)
	reported.add((rno,course))

#Put Dataframe in xlsx
output_file.to_excel("course_feedback_remaining.xlsx",index=False)