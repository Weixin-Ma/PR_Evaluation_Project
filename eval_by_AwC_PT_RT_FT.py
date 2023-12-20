# Author:   Weixin MA               weixin.ma@connect.polyu.hk
# tool kit for calculating AwC-FT, AwC-RT, and AwC-PT proposed in our work: Evaluation of Range Sensing-based Place Recognition for Long-term Urban Localization 
import numpy as np
import os
from matplotlib import pyplot as plt
import argparse
import math


def fast_eval(revist_critira="4"):
    print("***********************Calculating for AwC-FT, PT, RT***********************")

    file = ["1","2","3","4","5"]    #you should modified this according to your loop detection results, we have only 5 query sequences one time
    Precision_s = []
    Recall_s =[]
    F1_score_s = []

    orginal_score_max = []
    orginal_score_min = []
    for file_name in file:
        loop_result_file_path = "./"+ file_name +"/loop_result.txt"
        loop_results = np.genfromtxt(loop_result_file_path, dtype='float64').reshape(-1, 3)
        distance  = loop_results[:, 2].reshape(-1, 1)   
        score = 1- distance

        orginal_score_max.append(np.max(score))
        orginal_score_min.append(np.min(score))

    thre_max = np.max(orginal_score_max)     #Eq(3), b
    thre_min = np.min(orginal_score_min)     #Eq(2), a

    thresholds = np.linspace(thre_min, thre_max, 3000)    #using 3000 threshols, other values are ok, it will be more precise using a larger number theoretically
    for file_name in file:
        loop_result_file_path = "./"+ file_name +"/loop_result.txt"
        loop_results = np.genfromtxt(loop_result_file_path, dtype='float64').reshape(-1, 3)

        query_pose_file_path = "./"+ file_name +"/que_frame_pose.txt"
        query_frame_poses  = np.genfromtxt(query_pose_file_path, dtype='float32').reshape(-1, 3)
        
        ref_pose_file_path = "./"+ file_name +"/ref_frame_pose.txt" 
        ref_frame_poses  = np.genfromtxt(ref_pose_file_path, dtype='float32').reshape(-1, 3)

        query_id  = loop_results[:, 0].reshape(-1, 1)    #query frame ID
        match_id  = loop_results[:, 1].reshape(-1, 1)    #matched frame ID 
        distance1 = loop_results[:, 2].reshape(-1, 1)    #cos dis 

        score = 1- distance1

        num_frames = query_id.shape[0]

        ##check isGloblalyRevisited, i.e., check whether there exists loop for the query frame
        num_ref_frames = ref_frame_poses.shape[0]
        isGlobalRevisit = np.zeros((num_frames), dtype=int)
        for i in range(num_frames):                         #find the frame in reference sequence, which is closest to the query frame (using pose)
            query_x = float(query_frame_poses[i][0])  
            query_y = float(query_frame_poses[i][1])

            min_dis = 1000000000000000

            for j in range(num_ref_frames):
                ref_x = float(ref_frame_poses[j][0])
                ref_y = float(ref_frame_poses[j][1])

                diff_x = query_x - ref_x
                diff_y = query_y - ref_y
                dis = math.sqrt(diff_x*diff_x + diff_y*diff_y)

                if dis<min_dis:
                    min_dis =dis
            
            if min_dis < float(revist_critira):             # <isGloblalyRevisited，loop exists
                isGlobalRevisit[i] = 1

        
        num_thres = thresholds.shape[0]
        num_TP = np.zeros((num_thres), dtype=int)        #for true positives counting, using different thresholds
        num_FP = np.zeros((num_thres), dtype=int)        #for false positives counting, using different thresholds
        num_TN = np.zeros((num_thres), dtype=int)        #for true negatives counting, using different thresholds
        num_FN = np.zeros((num_thres), dtype=int)        #for false negatives counting, using different thresholds

        for j in range(num_frames):
            query_ID = int(query_id[j])
            match_ID = int(match_id[j])

            diff_x = float(query_frame_poses[query_ID][0]) - float(ref_frame_poses[match_ID][0])
            diff_y = float(query_frame_poses[query_ID][1]) - float(ref_frame_poses[match_ID][1])

            dis = math.sqrt( diff_x*diff_x + diff_y*diff_y )  #xy-coordinates are dominate, since the data-collection vehicle travel the same route

     
            for thre_ith in range(num_thres):
                if float(score[j]) >= thresholds[thre_ith]:      #when the similarity between the query frame and the top-1 candidate is larger than thresholds[thre_ith]，the PR method determine the query and top-1 candidate as a loop 
                    if dis < float(revist_critira):              #true positive result
                        num_TP[thre_ith] = num_TP[thre_ith] +1
                    else:
                        num_FP[thre_ith] = num_FP[thre_ith] +1   #false positive result   

                else:    
                    if isGlobalRevisit[j]==1:                     #false negative result                                         
                        num_FN[thre_ith] = num_FN[thre_ith] +1    
                    elif isGlobalRevisit[j]==0:                   #true negative result
                        num_TN[thre_ith] = num_TN[thre_ith] +1    


        Precision = np.zeros((num_thres), dtype=np.float32)
        Recall    = np.zeros((num_thres), dtype=np.float32)
        for k in range(num_thres):
            if num_TP[k]==0:
                Precision[k] = 0
                Recall[k] = 0
            else:
                Precision[k] = num_TP[k]/(num_TP[k] + num_FP[k])
                Recall[k]    = num_TP[k]/(num_TP[k] + num_FN[k])
        
        F1_score = 2 * Precision * Recall / (Precision + Recall + 1e-15)   #for F1 score

        Precision_s.append(Precision)           #store calculated Precision, Recall, and F1-score for different query sequences
        Recall_s.append(Recall)
        F1_score_s.append(F1_score)


    recall_diffs = np.zeros((num_thres), dtype=np.float32)    
    precision_diffs = np.zeros((num_thres), dtype=np.float32)    
    F1_score_diffs = np.zeros((num_thres), dtype=np.float32) 

    #for l-th threshold ，calculate \Delta_i for Precision，Recall，and F1-score
    for l in range(num_thres):
        recall_max = -1000000000000000
        recall_min =  1000000000000000

        precision_max = -1000000000000000
        precision_min =  1000000000000000

        F1_score_max = -1000000000000000
        F1_score_min =  1000000000000000

        for m in range(len(file)):         #for l-th threshold，Max(S_i) and Min(S_i) for Precision, Recall, and F1-score
            recall = Recall_s[m][l]
            precision = Precision_s[m][l]
            f1_score = F1_score_s[m][l]

            if recall < recall_min:
                recall_min = recall
            if recall > recall_max:
                recall_max = recall
            
            if precision < precision_min:
                precision_min = precision
            if precision > precision_max:
                precision_max = precision

            if f1_score < F1_score_min:
                F1_score_min = f1_score
            if f1_score > F1_score_max:
                F1_score_max = f1_score


        recall_diffs[l] = recall_max - recall_min
        precision_diffs[l] = precision_max - precision_min
        F1_score_diffs[l] = F1_score_max - F1_score_min

    recall_diff_mean = np.mean(recall_diffs)        

    precision_diff_mean = np.mean(precision_diffs)  

    f1_score_diff_mean = np.mean(F1_score_diffs)    

    normalized_AwC_RT = recall_diff_mean - 0.5*(recall_diffs[0] + recall_diffs[num_thres-1])/num_thres            ##normalized AwC-RT
    normalized_AwC_PT = precision_diff_mean - 0.5*(precision_diffs[0] + precision_diffs[num_thres-1])/num_thres   ##normalized AwC-PT
    normalized_AwC_F1 = f1_score_diff_mean - 0.5*(F1_score_diffs[0] + F1_score_diffs[num_thres-1])/num_thres      ##normalized AwC-F1-T

    print("AwC-RT, normalized: ", normalized_AwC_RT)
    print("AwC-PT, normalized: ", normalized_AwC_PT)
    print("AwC-FT, normalized: ", normalized_AwC_F1)


    #draw curve
    if not os.path.exists('./results'):
        os.mkdir('./results')
    if not os.path.exists('./results/curves'):
        os.mkdir('./results/curves')

    plt.xlabel("Threshold")
    plt.ylabel("Recall")
    plt.title("Recall-Threshold")
    plt.axis([0, 1, 0, 1])
    plt.plot(thresholds,Recall_s[0],label="Que-1",color='r',lw=1.5)
    plt.plot(thresholds,Recall_s[1],label="Que-2",color='b',lw=1.5)
    plt.plot(thresholds,Recall_s[2],label="Que-3",color='g',lw=1.5)
    plt.plot(thresholds,Recall_s[3],label="Que-4",color='m',lw=1.5)
    plt.plot(thresholds,Recall_s[4],label="Que-5",color='c',lw=1.5)
    plt.legend(loc="best")
    plt.savefig('./results/curves/RT-curve.png')
    #plt.show()
    plt.clf()

    plt.xlabel("Threshold")
    plt.ylabel("Precision")
    plt.title("Precision-Threshold")
    plt.axis([0, 1, 0, 1])
    plt.plot(thresholds,Precision_s[0],label="Que-1",color='r',lw=1.5)
    plt.plot(thresholds,Precision_s[1],label="Que-2",color='b',lw=1.5)
    plt.plot(thresholds,Precision_s[2],label="Que-3",color='g',lw=1.5)
    plt.plot(thresholds,Precision_s[3],label="Que-4",color='m',lw=1.5)
    plt.plot(thresholds,Precision_s[4],label="Que-5",color='c',lw=1.5)
    plt.legend(loc="best")
    plt.savefig('./results/curves/PT-curve.png')
    #plt.show()
    plt.clf()

    plt.xlabel("Threshold")
    plt.ylabel("F1-score")
    plt.title("F1-score Threshold")
    plt.axis([0, 1, 0, 1])
    plt.plot(thresholds,F1_score_s[0],label="Que-1",color='r',lw=1.5)
    plt.plot(thresholds,F1_score_s[1],label="Que-2",color='b',lw=1.5)
    plt.plot(thresholds,F1_score_s[2],label="Que-3",color='g',lw=1.5)
    plt.plot(thresholds,F1_score_s[3],label="Que-4",color='m',lw=1.5)
    plt.plot(thresholds,F1_score_s[4],label="Que-5",color='c',lw=1.5)
    plt.legend(loc="best")
    plt.savefig('./results/curves/FT-curve.png')
    #plt.show()
    plt.clf()


    #save values
    if not os.path.exists('./results/PT_RT_FT_data'):
        os.mkdir('./results/PT_RT_FT_data')
    
    np.savetxt( "./results/PT_RT_FT_data/threshold.txt", thresholds , fmt = '%f', delimiter = ' ')   #save thresholds 

    for id in range(len(file)):   
        np.savetxt( "./results/PT_RT_FT_data/" + file[id] +"_precision.txt", Precision_s[id] , fmt = '%f', delimiter = ' ')   #save Precisions
        np.savetxt( "./results/PT_RT_FT_data/" + file[id] +"_recall.txt", Recall_s[id] , fmt = '%f', delimiter = ' ')         #save Recalls
        np.savetxt( "./results/PT_RT_FT_data/" + file[id] +"_f1_socre.txt", F1_score_s[id] , fmt = '%f', delimiter = ' ')     #save F1-socres

    print("Successfully saved!!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--revist_critira', default='4',
                        help='revist critira in distance. [default: 4]')        #revisit critira，default:4m
    cfg = parser.parse_args()
    fast_eval(revist_critira=cfg.revist_critira)

