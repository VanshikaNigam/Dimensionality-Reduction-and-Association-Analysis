import numpy as np
import pandas as pd
from collections import Counter
#import itertools;
from itertools import chain, combinations

file_name= np.loadtxt('associationruletestdata.txt', delimiter="\t",dtype='str')
row,col= (file_name.shape)
#print(file_name)

#Begin :Values to be changed #
support=50; #setting the support to calculate the various the frequent item sets
confidence=0.60 #setting confidence
template_type=3
#End : Values to be changed #

valid_rules=[]
all_rules=[]
d={}
result=set()



#Function to get the count of each item
def get_count_single(transaction, items):
   #print("inside get_count_single")
   c=Counter();

   for i in items:
   	  
   	 c[i]=c[i]+1
   	 d[i]=c[i]
   
   #print (d)   
   return d


#Function to check the itemsets which are greater than and equal to given support
def support_check(items, sup):
	set_single=set()
	for key, value in d.items():
		if value>=sup:
			set_single.add(frozenset([key]))
	return set_single

# Function for calculating support of various combinations
def get_count(transaction, items,sup): 
   
   #counter=0;
   temp=set()
   transaction=pd.DataFrame.as_matrix(transaction)
   
   for s in items:
   	counter=0;
   	for i in range(0,row):
   		transaction_set= set(transaction[i])
   		#print(transaction_set)
   		
   		if(s.intersection(transaction_set)== s):
   			#print("Get Count Function-If Condition")

   			counter=counter+1

   	if(counter>=sup):
   		temp.add(s);
   #print(len(temp))
   return temp

 
#Function to generate combinations
def combine(set_1,set_2,k):
 
   #print(list_1)
   new_set=set()
   for a in  set_1:
      for b in set_2:
        if len(set(a | b))  == k and (str(b)+','+str(a)) not in new_set:
  
           new_set.add(a|b)

   #print(new_set)
   return new_set

print("*************Count of Various length Frequent Item set****************") 

print("Running for the Support :",support)
df= pd.DataFrame(file_name) 
for i in range (0, col-1):
   df[i]= 'G'+str(i+1)+'_'+df[i].astype(str)

#print(df)

####################### PRINT SINGLE #############

#print("Single count")

st=[]
for i in range (0, col):
   s=get_count_single(df,df[i])
   
   st.append(s)

#print(st)
candidate_set=support_check(st,support)
single_len=len(candidate_set)
print("Number of 1 length frequent item set =", len(candidate_set))

#print(len(result))
#print(one_set)
###################### PRINT SINGLE #############

###################### PRINT OVERALL #############
count=0
candidate_len=2
result_set=set(candidate_set)

while candidate_set:
   candidate_set=combine(candidate_set,candidate_set,candidate_len)
   candidate_set_sup=get_count(df,candidate_set,support)
   if len(candidate_set_sup)!=0:
      print("Number of", candidate_len, "length frequent itemset = ", len(candidate_set_sup))
   candidate_len=candidate_len+1
   candidate_set=candidate_set_sup
   count=count+len(candidate_set_sup)
   result_set.update(candidate_set)
   #result_set.append(candidate_set)

print("Total number of frequent sets = ", count+single_len)
#print (result_set)


#************************************************** Generate Rules  ****************************

print("****************Generating Rules For Templates****************")

def powerset(iterable):

   xs= list(iterable)
   return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def generateSet(result_set):
   
   for s in result_set:

      list_p_set=[]
      if len(s)>1 :
        p_set= powerset(s)
        list_p_set= list(p_set)
        list_p_set=list(filter (None, list_p_set))
        RuleGen(list_p_set,s)
        #print(len(list_p_set))


def RuleGen(list_p_set,s):
   list_rule=[]
   #print("Print list p set")
   #print(list_p_set)
   s=set(s)
   set_list=set(list_p_set)
   #print("Printing s")
   counter=0
   for i in set_list:
      #print("Inside For Loop")
      #print(list_p_set[i])
      list_bd_hd=[]
      s1=set()
      body=s.difference(i)
      if(len(body)!=0):
         
         list_bd_hd.append(list(body)) #body
         list_bd_hd.append(list(i)) #head
         all_rules.append(list_bd_hd)
      if(len(list_bd_hd)!=0):
         state1="RULE"
         state2="BODY"
         x_combine=Support_Head_Body(df,list_bd_hd,support,state1)
         x_body=Support_Head_Body(df,list(body),support,state2)
         

         confidence_item=x_combine/x_body
         if confidence_item >= confidence:
               #valid_rules.append(list(body))
               #valid_rules.append(list(i))
            valid_rules.append(list_bd_hd)

         
def Support_Head_Body(transaction,items,sup,state):

   transaction=pd.DataFrame.as_matrix(transaction)
   #print(set(items))
   #print(items)
   #print(len(items))
   length=len(items)
   counter=0;
   if(length==1 and state=="BODY"):
      #print("inside one body condition")
      for i in range(0,row):
         if pd.Series(items).isin(transaction[i]).all():
            counter=counter+1
     
   elif(length==2 )and state=="RULE":
      #print("inside rule condition")
      temp=[]
      for k in range(0,len(items)):
         temp+=items[k]
      for i in range(0,row):
         if pd.Series(temp).isin(transaction[i]).all():
            counter=counter+1
      #print("CHECK TIME")
      #print(temp)



   if(length>=2 and state=="BODY"):
      #print("inside body condition")
      temp=[]
      for j in range(0,len(items)):
         temp+=[items[j]]
      #print("temp is")
      #print(temp)
      for i in range(0,row):
         if pd.Series(temp).isin(transaction[i]).all():
            counter=counter+1

   return counter


generateSet(result_set)

####################### Template Answering #######################

print("******************Template Answering***********************")

def query_template1(valid_rules,state,count,item):
	#print("inside template 1")
	#print("Template 1 answer")	
	c=0
	template_ans=[]
	#print (item)
	#item=list([item])
	print(item)
	if state=="RULE" and count=="ANY":
		#print("inside rule and any 1")

		for i in range(0,len(valid_rules)):
			#print(valid_rules)
			#print(valid_rules[i])
			check=[]
			for j in range(0,len(item)):

				if pd.Series(item[j]).isin(valid_rules[i][0]).all() or pd.Series(item[j]).isin(valid_rules[i][1]).all():
						check.append(item[j])
				#print(check)
			if len(check)>=1:
				c=c+1
				template_ans.append(valid_rules[i])

			
		#print(c)
	if state=="RULE" and count=="NONE":
		for i in range(0,len(valid_rules)):
			check=[]
			for j in range(0,len(item)):
				if pd.Series(item[j]).isin(valid_rules[i][0]).all()==False and pd.Series(item[j]).isin(valid_rules[i][1]).all()==False:
			
					check.append(item[j])
				#print(check)
			if len(check)==len(item):
				#c=c+1
				template_ans.append(valid_rules[i])


			
		#print(c)
	if state=="BODY" and count=="NONE":
		for i in range(0,len(valid_rules)):

			check=[]
			for j in range(0,len(item)):

				if pd.Series(item[j]).isin(valid_rules[i][0]).all()==False:
					check.append(item[j])
				#print(check)
			if len(check)==len(item):
				#c=c+1
				template_ans.append(valid_rules[i])


			
		#print(c)
	if state=="BODY" and count=="ANY":
		#print("inside rule and any 1")
		for i in range(0,len(valid_rules)):
			#print(valid_rules)
			#print(valid_rules[i])
			check=[]
			for j in range(0,len(item)):

				if pd.Series(item[j]).isin(valid_rules[i][0]).all():
					check.append(item[j])
				#print(check)
			if len(check)>=1:
				c=c+1
				template_ans.append(valid_rules[i])


			
		#print(c)
	if state=="HEAD" and count=="NONE":
		for i in range(0,len(valid_rules)):
			check=[]
			for j in range(0,len(item)):
				if pd.Series(item[j]).isin(valid_rules[i][1]).all()==False:
					check.append(item[j])
				#print(check)
			if len(check)==len(item):
				#c=c+1
				template_ans.append(valid_rules[i])


			
		#print(c)
	if state=="HEAD" and count=="ANY":
		#print("inside rule and any 1")
		for i in range(0,len(valid_rules)):
			#print(valid_rules)
			#print(valid_rules[i])
			check=[]
			for j in range(0,len(item)):
				if pd.Series(item[j]).isin(valid_rules[i][1]).all():
					check.append(item[j])
				#print(check)
			if len(check)>=1:
				c=c+1
				template_ans.append(valid_rules[i])

			
		#print(c)
	if state=="BODY" and count==1:
		
			for i in range(0,len(valid_rules)):
				check=[]
				for j in range(0,len(item)):

					if pd.Series(item[j]).isin(valid_rules[i][0]).all():
						check.append(item[j])
				#print(check)
				if len(check)==1:
					c=c+1
					template_ans.append(valid_rules[i])

			#print(c)
	if state=="HEAD" and count==1:
		
			for i in range(0,len(valid_rules)):
				check=[]
				for j in range(0,len(item)):

					if pd.Series(item[j]).isin(valid_rules[i][1]).all():
						check.append(item[j])
				#print(check)
				if len(check)==1:
					c=c+1
					template_ans.append(valid_rules[i])

			#print(c)
	if state=="RULE" and count==1:
		
			for i in range(0,len(valid_rules)):
				check=[]
				for j in range(0,len(item)):

					if pd.Series(item[j]).isin(valid_rules[i][0]).all() or pd.Series(item[j]).isin(valid_rules[i][1]).all():
						check.append(item[j])
				
				if len(check)==1:
					c=c+1
					template_ans.append(valid_rules[i])

			#print(c)
	
		
	return template_ans


def query_template2(valid_rules,state,count):
	#print("Template 2 answer")
	c=0;
	template_ans=[]
	if state=="RULE":
		#print(valid_rules)
		for i in range(0,len(valid_rules)):

			#print("RULES")
			len_of_rules=len(valid_rules[i][0])+len(valid_rules[i][1])
			if(len_of_rules>=count):
				c=c+1;
				template_ans.append(valid_rules[i])
		#print(template_ans)
				#print(len_of_rules)
		#print(c)
	elif state=="BODY":
		#print("Inside Body If")
		for i in range(0,len(valid_rules)):
			len_of_body=len(valid_rules[i][0])
			if(len_of_body>=count):
				c=c+1
				template_ans.append(valid_rules[i])
		#print(template_ans)
				#print(len_of_body)
		#print(c)
	elif state=="HEAD":
		#print("Inside Head If")
		for i in range(0,len(valid_rules)):
			len_of_head=len(valid_rules[i][1])
			if(len_of_head>=count):
				c=c+1
				template_ans.append(valid_rules[i])
				#print(valid_rules[i])
				#print(len_of_head)
		#print(c)
	
	return template_ans


def query_template3(query_array):
	
	
	if len(query_array)==7: #1 and 1 ; 1 or 1
		if query_array[0]=="1and1":
			print("1 and 1")
			x=query_template1(valid_rules,query_array[1],query_array[2],query_array[3])
			y=query_template1(valid_rules,query_array[4],query_array[5],query_array[6])
		
			intersect_x_y=[a for a in x if a in y]
			#print(intersect_x_y)
			#print(len(intersect_x_y))
			return intersect_x_y

		if query_array[0]=="1or1":
			print("1 or 1")
			x=query_template1(valid_rules,query_array[1],query_array[2],query_array[3])
			y=query_template1(valid_rules,query_array[4],query_array[5],query_array[6])
		
			
			union_x_y=[]
			for i in x:
				union_x_y.append(i)
			for z in y:
				if z not in x:
					union_x_y.append(z)

			
			#print(union_x_y)
			#print(len(union_x_y))
			return union_x_y


		
	if len(query_array)==6:
		
		if query_array[0]=="1or2":
			print("1 or 2")
			x=query_template1(valid_rules,query_array[1],query_array[2],query_array[3])
			y=query_template2(valid_rules,query_array[4],query_array[5])
			
			
			union_x_y=[]

			for i in x:
				union_x_y.append(i)
			for z in y:
				if z not in x:
					union_x_y.append(z)

			#print(union_x_y)
			#print(len(union_x_y))

			return union_x_y

		if query_array[0]=="1and2":
			print("1 and 2")
			x=query_template1(valid_rules,query_array[1],query_array[2],query_array[3])
			y=query_template2(valid_rules,query_array[4],query_array[5])
			

			intersect_x_y=[a for a in x if a in y]
			#print(intersect_x_y)
			#print(len(intersect_x_y))
			return intersect_x_y


	if len(query_array)==5:
		print("2 and 2")
		if query_array[0]=="2and2":
			x=query_template2(valid_rules,query_array[1],query_array[2])
			y=query_template2(valid_rules,query_array[3],query_array[4])
			

			intersect_x_y=[]
			if len(x) < len(y):
				for e in x:
					if e in y:	
						intersect_x_y.append(e)
			else:
				for e in y:
					if e in x:
						intersect_x_y.append(e)

		#print(intersect_x_y)			
		#print(len(intersect_x_y))
			return intersect_x_y

		if query_array[0]=="2or2":
			print("2 or 2")
			x=query_template2(valid_rules,query_array[1],query_array[2])
			y=query_template2(valid_rules,query_array[3],query_array[4])
			union_x_y=[]

			for i in x:
				union_x_y.append(i)
			for z in y:
				if z not in x:
					union_x_y.append(z)
			
			#print(union_x_y)		
			#print(len(union_x_y))
			return union_x_y 


if template_type==1:
	state_1="HEAD" #"BODY", "HEAD"
	count_appearance=1
	item_1=["G59_Up","G10_Down"]
	result=query_template1(valid_rules,state_1,count_appearance,item_1)
	


elif template_type==2:
	state_2="RULE" #"BODY", "HEAD"
	count_occurences=3
	result=query_template2(valid_rules,state_2,count_occurences)

else:
	query_array=["2and2", "BODY", 1, "HEAD", 2]
	result=query_template3(query_array)

for i in result:
	print(i)

print("Total Number of Rules: " + str(len(result)))












