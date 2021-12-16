import time
import random



start_time = time.time()


## SIMILARITY CALCULATOR ##

def similarity_calculator(each_slot_session,dist_information):


    similarity_score = 0.0

    if len(each_slot_session)<=1:
        return similarity_score

    i = 0
    while(i != len(each_slot_session)):
        j=i+1

        while(j != len(each_slot_session)):

            similarity_score += 1 - dist_information[each_slot_session[i]][each_slot_session[j]]
            j += 1

        i += 1
    
    return similarity_score 


## DISTANCE CALCULATOR ##

def distance_calculator(array_got,dist_information):



    def final_distance_answer(box1,box2,dist_inf):
    
        final_distance_result = 0.0

        if len(box1) == 0 or len(box2) == 0 :

            return final_distance_result
        
        b1_idx = 0
        while(b1_idx != (len(box1))):

            b2_idx = 0
            while(b2_idx != len(box2)):

                final_distance_result += dist_inf[box1[b1_idx]][box2[b2_idx]]

                b2_idx += 1

            b1_idx += 1


        return final_distance_result

        
        



    def helper_distance_calculator(got_array_2,dist_info):
        

        diatance_of_column = 0.0
        
        i = 0

        while(i != len(got_array_2)):
            j = i+1

            while(j != len(got_array_2)):

                diatance_of_column += final_distance_answer(got_array_2[i],got_array_2[j],dist_info)
                
                j += 1

            i += 1

        return diatance_of_column




    distance_calculating_column_wise = 0.0

    j = 0

    while(j != len(array_got[0])):
        
        column_array = []

        i = 0
        while(i != len(array_got)):

            column_array.append(array_got[i][j])
            i += 1

        distance_calculating_column_wise += helper_distance_calculator(column_array,dist_information)

        j += 1
    
    return distance_calculating_column_wise




## GOODNESS CALCULATOR ##



def GoodnessSchedule(C,distance_informing,goodness_to_be_calculated_on_array):
    

    finally_similarity = 0.0


    for i in range(len(goodness_to_be_calculated_on_array)):
        for block in goodness_to_be_calculated_on_array[i]:
            finally_similarity += similarity_calculator(block,distance_informing)


    finally_distance = distance_calculator(goodness_to_be_calculated_on_array,distance_informing)
    
    goodness = finally_similarity + (C * finally_distance)  
 

    return goodness



def ConfrenceSchedular(array_to_show,num_time_slots,num_parallel_sessions,n,C,num_papers_in_session,paper_number_nodes,distance_information):
   

  
    helper_solution = []
    

    p=0
    while(p != num_parallel_sessions):
        helper_solution.append([])
        
        t = 0
        while(t != num_time_slots):
            helper_solution[p].append([])

            t += 1

        p += 1



    local_maximum_goodness = 0.0


   
    bool_array = []

    i=0
    while(i != num_parallel_sessions):

        list1 = []

        j = 0
        while(j != num_time_slots):
            list1.append(0)

            j += 1
        
        bool_array.append(list1)
        i += 1

    

    
    t = 0

    while( t!= num_time_slots):


        for var in range(0,num_papers_in_session * num_parallel_sessions):

            #intialization

            if var == 0 and t == 0: #first slot to be randomly filled

                
                current_paper_number = random.choice(paper_number_nodes)
                current_time_slot = 0
                current_parallel_session = 0
                current_temporary_maximum_goodness = 0.0
            
            else:

                for _ in range(0,len(paper_number_nodes)):
                    paper_number = random.choice(paper_number_nodes)  

                    for p in range(0,num_parallel_sessions):
                        
                        if bool_array[p][t] == 1:
                            continue

                        else:
                            helper_solution[p][t].append(paper_number)
                            temporary_local_goodness = GoodnessSchedule(C,distance_information,helper_solution)
                            
                            helper_solution[p][t].remove(paper_number)

                            if temporary_local_goodness >= current_temporary_maximum_goodness:
                                
                                current_temporary_maximum_goodness,current_paper_number,current_parallel_session,current_time_slot = temporary_local_goodness,paper_number,p,t


            paper_number_nodes.remove(current_paper_number) 

            helper_solution[current_parallel_session][current_time_slot].append(current_paper_number)
            
            
            
            if time.time() - start_time >=1.8 and time.time() - start_time <= 2:
                
                array_to_show[current_parallel_session][current_time_slot].append(current_paper_number)
                
                for i in range(0,num_parallel_sessions):
                    for j in range(0,num_time_slots):
                        for k in range(0,num_papers_in_session):

                            if len(array_to_show[i][j]) != num_papers_in_session:
                                
                                
                                if len(array_to_show[i][j]) > 0:
                                    
                                    try:
                                        
                                        if (array_to_show[i][j][k] == 0 or (array_to_show[i][j][k] == True)):
                                            continue
                                            
                                    
                                    except:
                                        new_paper_number = random.choice(paper_number_nodes)                                       
                                        array_to_show[i][j].append(new_paper_number)
                                        paper_number_nodes.remove(new_paper_number)
                                  

                                elif len(array_to_show[i][j]) == 0:

                                        new_paper_number = random.choice(paper_number_nodes)
                                        array_to_show[i][j].append(new_paper_number)
                                        paper_number_nodes.remove(new_paper_number)

                                
                            if len(array_to_show[i][j]) == num_papers_in_session:
                                    bool_array[i][j]=1

                local_maximum_goodness =  GoodnessSchedule(C,distance_information,array_to_show)
                
                return array_to_show,local_maximum_goodness
            


            y=0
            while( y != num_parallel_sessions):
                z=0
                while( z != num_time_slots):

                    if len(helper_solution[y][z]) == num_papers_in_session:
                        bool_array[y][z] = 1

                    z += 1
                y += 1

  

            array_to_show[current_parallel_session][current_time_slot].append(current_paper_number)

        t += 1
            
    local_maximum_goodness =  GoodnessSchedule(C,distance_information,array_to_show)  
  
    
    return array_to_show,local_maximum_goodness        



##main##

def main(num_papers_in_session,num_time_slots,num_parallel_sessions,C,n,distance_collected_from_given_data):


    store_local_optima_goodness = []
    store_result_local_optimas = dict()

    number_of_epochs = 3

    for epoch in range(0,number_of_epochs):
        

        paper_number_nodes = []
        o = 0
        while(o != n):

            paper_number_nodes.append(o)
            o += 1
        

        array_to_show = []


        p = 0
        while(p != num_parallel_sessions):

            array_to_show.append([])

            t = 0

            while(t != num_time_slots):

                array_to_show[p].append([])

                t += 1
            
            p += 1
  

         

        array_to_show2, maximum_goodness = ConfrenceSchedular(array_to_show,num_time_slots,num_parallel_sessions,n,C,num_papers_in_session,paper_number_nodes,distance_collected_from_given_data)

        store_result_local_optimas[epoch] = array_to_show2
        store_local_optima_goodness.append(maximum_goodness)
    
    

    global_maximum_index = store_local_optima_goodness.index(max(store_local_optima_goodness))
    
    array_to_show1 = store_result_local_optimas[global_maximum_index]
    # print("store_local_optima_goodness:",store_local_optima_goodness)
    # print("store_result_local_optimas:",store_result_local_optimas)
    
    i = 0
    while(i != len(array_to_show)):
        
        j = 0
        while(j != len(array_to_show1[0])):

            k = 0
            while(k != len(array_to_show1[0][0])):

                array_to_show1[i][j][k] += 1
                k += 1

            j += 1
        i += 1
    


    for i in range(0,len(array_to_show1)):

        for j in range(0,len(array_to_show1[0])):  print(*array_to_show1[i][j]) if j == len(array_to_show1[0])-1 else print(*array_to_show1[i][j],end=" | ")
        



if __name__ == "__main__":


    num_papers_in_session = input()
    num_parallel_sessions = input()
    num_time_slots = input()
    C = input()

    num_papers_in_session = int(num_papers_in_session)
    num_parallel_sessions = int(num_parallel_sessions)
    num_time_slots = int(num_time_slots)
    C = float(C)
    
    
    n = num_papers_in_session * num_time_slots * num_parallel_sessions
    
    distance_collected_from_given_data = [] 
    
 
    for i in range(0,n):

        distance_collected_from_given_data.append([float(i) for i in input().split()])


    main(num_papers_in_session,num_time_slots,num_parallel_sessions,C,n,distance_collected_from_given_data)
    


    