import random
import itertools
import copy


############################ Find row no. and exact location of missing values ##################
def missing_values(samples, no_of_nodes, no_of_samples):
    location_missing_value = [[1 for i in range(no_of_nodes)] for j in range(no_of_samples)]
    row_with_missing_value = [0 for i in range(no_of_samples)]
    k = 0
    for i in range(no_of_samples):
        for j in range(no_of_nodes):
            if(samples[i][j]=='?'):
                row_with_missing_value[i] = 1
                location_missing_value[i][j] = 0
            else:
                location_missing_value[i][j] = 1
        k+=1
    return location_missing_value, row_with_missing_value



def number_of_entries_in_complete_sample_list(no_of_samples,no_of_nodes,location_missing_value,possible_node_values,no_of_rows_with_no_mis_val):
  count = 0
  for i in range(no_of_samples):
    for j in range(no_of_nodes):
      if(location_missing_value[i][j]==0):
        count+=len(possible_node_values[j])
  count+=no_of_rows_with_no_mis_val

  return count



def add_weight_col_in_sample_list(no_of_samples,no_of_nodes,samples,row_with_missing_value):
  
  data_dict = dict()
  for i in range(no_of_samples):
      di = dict()
      k = 0
      #sam = np.array((no_of_nodes,1), dtype="object")
      sam = [None] * (no_of_nodes+2)
      #print(sam.shape)
      for j in range(no_of_nodes):
          sam[k] = samples[i][j]
          k+=1
      if(row_with_missing_value[i]==0):
        sam[k] =  "s"+str(i)
        k+=1
        sam[k] = 1
      else:
        sam[k] =  "s"+str(i)
        k+=1
        sam[k] = -1
      #di["data_point"] = sam
      data_dict[i] = sam
  sample_list = []
  for i in range(len(data_dict)):
    sample_list.append(data_dict[i])
  return sample_list



def make_complete_sample_list(no_of_samples,no_of_nodes,possible_node_values,samples,row_with_missing_value,location_missing_value,no_of_rows_with_no_mis_val):
  c=0
  count = number_of_entries_in_complete_sample_list(no_of_samples,no_of_nodes,location_missing_value,possible_node_values,no_of_rows_with_no_mis_val)
  sample_list = add_weight_col_in_sample_list(no_of_samples,no_of_nodes,samples,row_with_missing_value)
  sample_list_complete = [None] * count
  for i in range(no_of_samples): 
      flag = 0
      for j in range(no_of_nodes): 
          if(sample_list[i][j] == "?"):
              flag = 1
              for x in range(len(possible_node_values[j])):
                  sample_list_complete[c] = copy.deepcopy(sample_list[i])
                  sample_list_complete[c][j] = possible_node_values[j][x]
                  c+=1
              break
      if(flag == 0):
          sample_list_complete[c] = sample_list[i]
          c+=1

  return sample_list_complete



def find_parent_nodes(dependencies,no_of_nodes):
  dep = [[row[i] for row in dependencies] for i in range(len(dependencies[0]))]
  dependency_list_for_each_node = []

  no_of_depen_for_each_node = []  
  for i in range(no_of_nodes):
      parents = []
      count = 0
      for j in range(no_of_nodes):
          if  dep[i][j]== 1:
              count+=1
              parents.append(j)
      no_of_depen_for_each_node.append(count) 
      dependency_list_for_each_node.append(parents)       



  return dependency_list_for_each_node, no_of_depen_for_each_node



### random initialization ###
def generate_random_prob(mistaken_var , n):  
    values = [0.0, 1.0] + [random.random() for _ in range(n - 1)]
    values.sort()
    return [values[i+1] - values[i] for i in range(n)]



def cal_node_prob_ditri(node, dep_list,possible_node_values):
  #returns dict of prob dis
  pd = []
  total_evidences = 1
  d = dict()
  if(len(dep_list)==0):
    pd = generate_random_prob(1,len(possible_node_values[node]))    
    for i in range(len(pd)):
      d[possible_node_values[node][i]] = round(pd[i], 4)
  else:
    pd.append(possible_node_values[node])
    for i in range(len(dep_list)):
      pd.append(possible_node_values[dep_list[i]])
      total_evidences *= len(possible_node_values[dep_list[i]])

    res = list(itertools.product(*pd))
    for combi in res:
      d[combi] = -1


    ctrl = 0
    for i in d.keys(): 
        probabilities_sum_1 = generate_random_prob(1,len(possible_node_values[node]))
        probabilities_sum_1_ctr = -1
        for j in d.keys(): 
          if list(j)[1:] == list(i)[1:]:
            probabilities_sum_1_ctr+=1
            d[j] = probabilities_sum_1[probabilities_sum_1_ctr]

        ctrl+=1
        if ctrl == total_evidences:
          break

  return d


def make_dict_for_each_node_cpt(no_of_nodes,possible_node_values,dependency_list_for_each_node):
  prob_ditri_for_each_node = dict()
  for i in range(no_of_nodes):
    prob_ditri_for_each_node[i] = cal_node_prob_ditri(i, dependency_list_for_each_node[i],possible_node_values)


  return prob_ditri_for_each_node


## geprobabilities ## 
def get_prob(temp,prob_ditri_for_each_node,no_of_depen_for_each_node,dependency_list_for_each_node):
  k = 1

  for key in temp:
    if(no_of_depen_for_each_node[key]==0):
      k*=prob_ditri_for_each_node[key][str(temp[key])]
    else:
      li = dependency_list_for_each_node[key]   
      li1 = []
      li1.append(str(temp[key]))
      for i in li:
        li1.append(str(temp[i]))
      k*=prob_ditri_for_each_node[key][tuple(li1)]
  return k


### find row with missing values ###
def row_with_missing(location_missing_value):
  mis_ind = []
  for i in range(no_of_samples):
    flag = 0
    for j in range(no_of_nodes):
      if(location_missing_value[i][j]==0):
        flag = 1
        mis_ind.append(j)
        break
    if(flag==0):
      mis_ind.append(-100)
  return mis_ind




######################## E STEP ###########################
def E_Step(location_missing_value,possible_node_values,samples,no_of_nodes,sample_list_complete,prob_ditri_for_each_node,no_of_depen_for_each_node,dependency_list_for_each_node):
  k = -1
  counter = -1
  mis_ind = row_with_missing(location_missing_value)
  for i in mis_ind:
    k+=1
    if(i!=-100):
      tup = []
      dic = dict()
      combi = []
      for j in possible_node_values[i]:
        t = []
        a = [j]+samples[k]
        a.remove('?')
        t.append(tuple(a))
        dic[i] = j
        for y in range(no_of_nodes):
          if(samples[k][y]!='?'):
            dic[y] = samples[k][y]
        xx = copy.deepcopy(dic)
        combi.append(xx)
      numm = 0
      for num in combi:
        denn = 0
        numm = get_prob(num,prob_ditri_for_each_node,no_of_depen_for_each_node,dependency_list_for_each_node)
        for den in combi:
          denn+=get_prob(den,prob_ditri_for_each_node,no_of_depen_for_each_node,dependency_list_for_each_node)
        counter += 1
        sample_list_complete[counter][-1] = round(numm/denn,4)

    else:
      counter+=1
      prob_of_ques_mark_sample = 1
      sample_list_complete[counter][-1] = round(prob_of_ques_mark_sample, 4)
  
  return sample_list_complete

      

############################### M STEP ###################################

def get_m_step_prob_dep_nodes(t, ind,sample_list_complete,dependency_list_for_each_node):

  numerator_store_number_of_samples = dict()
  denominator_store_number_of_samples = dict()
  numerator_store_number_of_samples_values = dict()
  denominator_store_number_of_samples_values = dict()

  #### calculating numerator ###
  
  var = [t]
  for k in var:
   
    wt_list = 0
    den_count = 0
    for s in sample_list_complete:
      found = 0
      counter = 0
      ctr = 0
      
      for i in dependency_list_for_each_node[ind]:
        if(counter==0):
          if(s[ind] == k[0]):
            found = 1
            counter = 1
            ctr += 1

          elif(s[ind]!=k[0]):
            found = 0
            break


        if(s[i]==k[ctr]):
          found = 1
          ctr+=1

        elif(s[i]!=k[ctr]):
          found = 0
          break


      if(found==1):
        wt_list = s[-1] 
        found=0
        
        if s[-2] not in numerator_store_number_of_samples and s[-1] != 0:
          numerator_store_number_of_samples[s[-2]] = 1 
          numerator_store_number_of_samples_values[s[-2]] = wt_list 

        elif s[-2] in numerator_store_number_of_samples and s[-1] != 0:
          numerator_store_number_of_samples[s[-2]] += 1
          numerator_store_number_of_samples_values[s[-2]] += wt_list 

 


    final_numerator_value = 0
    for kei in numerator_store_number_of_samples:
      if numerator_store_number_of_samples[kei] > 1:
        final_numerator_value += 1
      elif numerator_store_number_of_samples[kei] == 1:
        final_numerator_value += numerator_store_number_of_samples_values[kei]




  #### calculating denominator ###
  var = [t]                
  for k in var:
    wt_list = 0
    den_count = 0
    for s in sample_list_complete:
      found = 0
      counter = 0
      ctr = 0
      ctr+=1
      for i in dependency_list_for_each_node[ind]:

        if(s[i]==k[ctr]):
          found = 1
          ctr+=1

        elif(s[i]!=k[ctr]):
          found = 0
          break


      if(found==1):
        # wt_list_denom += s[-1]
        if s[-1] == 0:
          den_count = 0
        elif s[-1] != 0:
          den_count = 1 # den_count += 1

        found=0

        if s[-2] not in denominator_store_number_of_samples and s[-1] != 0:
          denominator_store_number_of_samples[s[-2]] = 1
          denominator_store_number_of_samples_values[s[-2]] = den_count

        elif s[-2] in denominator_store_number_of_samples and s[-1] != 0:

          denominator_store_number_of_samples[s[-2]] += 1
          denominator_store_number_of_samples_values[s[-2]] += den_count


    final_denominator_value = 0
    for keis in denominator_store_number_of_samples:
      if denominator_store_number_of_samples[keis] > 1:
        final_denominator_value += 1
      elif denominator_store_number_of_samples[keis] == 1:
        final_denominator_value += denominator_store_number_of_samples_values[keis]


    if final_numerator_value == 0:
      updated_prob = 0

    elif final_numerator_value != 0:
      updated_prob = final_numerator_value / final_denominator_value  #/den_count


  return updated_prob 
 

def get_m_step_prob_indep_nodes(t,ind,sample_list_complete):
  numerator_store_number_of_samples_values_indep = dict()
  numerator_store_number_of_samples_indep = dict()
  denominator_store_number_of_samples_values_indep = dict()
  denominator_store_number_of_samples_indep = dict()

  numerator_weight = 0
  for s in sample_list_complete:
    if s[ind] == t:
      numerator_weight = s[-1]
      if s[-2] not in numerator_store_number_of_samples_indep and s[-1] != 0:
        numerator_store_number_of_samples_indep[s[-2]] = 1
        numerator_store_number_of_samples_values_indep = numerator_weight
      elif s[-2] in numerator_store_number_of_samples_indep and s[-1] != 0:
        numerator_store_number_of_samples_indep[s[-2]] += 1
        numerator_store_number_of_samples_values_indep += numerator_weight

  final_indep_numer_val = 0
  for keys in numerator_store_number_of_samples_indep:
    if numerator_store_number_of_samples_indep[keys] > 1:
      final_indep_numer_val += 1
    elif numerator_store_number_of_samples_indep[keys] == 1:
      final_indep_numer_val += numerator_store_number_of_samples_indep[keys]
  
  # if denominator_ctr == 0 or numerator_weight == 0:
  if final_indep_numer_val == 0:
    updated_ind_prob = 0 
  else:
    updated_ind_prob = final_indep_numer_val / len(samples)

    
  return updated_ind_prob

def check_convergence(prev_cpt,prob_ditri_for_each_node):

  dictionary_containing_convergent_values_for_each_node=dict()
  stopping_convergence_criteria = dict()
  for key in prev_cpt:
    
    dict1 = prev_cpt[key]
    dict2 = prob_ditri_for_each_node[key]

    res = dict()
    temporary_stopping_res = dict()
    for key1 in dict2.keys():
      value = abs(dict2[key1] - dict1[key1])
      res[key1] = value
      if value == 0:
        temporary_stopping_res[key1] = 0
      elif value != 0:
        temporary_stopping_res[key1] = 1

    stopping_convergence_criteria[key] = temporary_stopping_res
    dictionary_containing_convergent_values_for_each_node[key] = res
    # print(res)
  
  check_value = 0
  stop = 0
  for sc_key in stopping_convergence_criteria:
    check_value += sum(stopping_convergence_criteria[sc_key].values())

  if check_value == 0:
    stop = 0

  elif check_value != 0:
    stop = 1
  
  return stop





def bayesian_network(no_of_nodes,possible_node_values,samples,no_of_samples,dependencies):

  location_missing_value, row_with_missing_value = missing_values(samples, no_of_nodes, no_of_samples)

  
  no_of_rows_with_no_mis_val = row_with_missing_value.count(0)

  sample_list_complete = make_complete_sample_list(no_of_samples,no_of_nodes,possible_node_values,samples,row_with_missing_value,location_missing_value,no_of_rows_with_no_mis_val)
  dependency_list_for_each_node, no_of_depen_for_each_node = find_parent_nodes(dependencies,no_of_nodes)

  prob_ditri_for_each_node = make_dict_for_each_node_cpt(no_of_nodes,possible_node_values,dependency_list_for_each_node) 

  stoppage = 1

  while(stoppage == 1):

    prob_ditri_for_each_node = prob_ditri_for_each_node
    sample_list_complete = E_Step(location_missing_value,possible_node_values,samples,no_of_nodes,sample_list_complete,prob_ditri_for_each_node,no_of_depen_for_each_node,dependency_list_for_each_node)


    prev_cpt = copy.deepcopy(prob_ditri_for_each_node)

    for key in prob_ditri_for_each_node:
      no_of_parents = no_of_depen_for_each_node[key]
      if(no_of_parents==0):
        for i in prob_ditri_for_each_node[key]:
          prob_ditri_for_each_node[key][i] = get_m_step_prob_indep_nodes(i, key,sample_list_complete)

      else:
        for i in prob_ditri_for_each_node[key]:
          prob_ditri_for_each_node[key][i] = get_m_step_prob_dep_nodes(i, key,sample_list_complete,dependency_list_for_each_node)

    stoppage = check_convergence(prev_cpt,prob_ditri_for_each_node)  

    if stoppage == 0:
      break

    elif stoppage ==1:

      location_missing_value, row_with_missing_value = missing_values(samples, no_of_nodes, no_of_samples)

      no_of_rows_with_no_mis_val = row_with_missing_value.count(0)

      dependency_list_for_each_node, no_of_depen_for_each_node = find_parent_nodes(dependencies,no_of_nodes)


#   print("\nFINAL prob_ditri_for_each_node:\n",prob_ditri_for_each_node)
  return prob_ditri_for_each_node
  
      

    


if __name__ == "__main__":

    
    ########################## INPUT ############################
    
    no_of_nodes = int(input())
    values_n_variables_can_take = dict()
    for i in range(0,no_of_nodes):
        values_n_variables_can_take[str(i)] = input().split(", ")

    number_of_values_each_variable_take = copy.deepcopy(values_n_variables_can_take)

    for key in values_n_variables_can_take:
        number_of_values_each_variable_take[key] = len(values_n_variables_can_take[key])
    ## {'0':3,'1':2,'2':4}

    dependencies = []
    for i in range(0,no_of_nodes):
        dependencies.append([int(j) for j in input().split()])

    no_of_samples = int(input())
    samples_list_old = []
    for i in range(0,no_of_samples):
        samples_list_old.append(input().split(","))


    samples = copy.deepcopy(samples_list_old)
    for col_s in range(0,no_of_nodes):
        for row_s in range(0,no_of_samples):

            if samples[row_s][col_s] in values_n_variables_can_take[str(col_s)]:
                samples[row_s][col_s] = str(values_n_variables_can_take[str(col_s)].index(samples[row_s][col_s]))


    possible_node_values = []
    for keys in values_n_variables_can_take.keys():
        temp_list = []
        for h in range(0,len(values_n_variables_can_take[keys])):
            temp_list.append(str(h))
        
        possible_node_values.append(temp_list)


    prob_ditri_for_each_node = bayesian_network(no_of_nodes,possible_node_values,samples,no_of_samples,dependencies) ## calling overall structure
    
    for final_key in prob_ditri_for_each_node.keys():
        final_list1 = list(prob_ditri_for_each_node[final_key].values())
        final_list1 = [format(f,'.4f') for f in final_list1]
        print(*final_list1,sep=" ")