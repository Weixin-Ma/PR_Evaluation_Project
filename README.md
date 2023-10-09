# PR_Evaluation_Project
A Comprehensive Evaluation on Range Sensor-based Long-term Place Recognition in Large-scale Urban Environment

## Obejctive
The performance of long-term place recognition can easily change with the variation of environmental conditions, especially the variation of weather and traffic condition. To have a deep understanding about this problem,we conducted a comprehensive evaluation of several SOTA range-sensor-based place recognition techniques on a long-term public dataset, Borease, which contains stark weather and traffic condition variation. We also proposed two new metrics to evaluate the effect of matching threshold setting on long-term place recognition performance

## Raw Data
All the results in the paper can be found in this repository.

### Details about the Downsampled Sequences
All the detailed files for the downsampled sequences used for testing can be found in floder `frame_info`. In each child folder, there are `lidar_frames.txt` and `radar_frames.txt`as shown as following:

```text
boreas-YYYY-MM-DD-HH-MM
|--- lidar_frames.txt
|     |--- 1606417097502930 0.814389404 -0.580309922 -0.003208223 -0.001453277 0.580209436 0.814116180 0.023913492 -0.002786294 -0.011265371 -0.021336336 0.999708884 0.129992412 0.000000000 0.000000000 0.000000000 1.000000000 
|          ...
|--- radar_frames.txt
|     |--- 1606417097528152 0.979843754 0.199175060 0.015346467 -0.005591902 0.199444473 -0.979731467 -0.018658891 -0.010576910 0.011319031 0.021343566 -0.999708123 0.494885921 0.000000000 0.000000000 0.000000000 1.000000000 
           ...
```

`lidar_frames.txt` records details about the LiDAR frames of the sequence `boreas-YYYY-MM-DD-HH-MM`. The $1^{th}$ column is the timestamp of the LiDAR frame. Column 2-17 is the $4 \times 4$ pose matrix of the LiDAR frame.

`radar_frames.txt` records details about the Radar frames of the sequence `boreas-YYYY-MM-DD-HH-MM`. The $1^{th}$ column is the timestamp of the Radar frame. Column 2-17 is the $4 \times 4$ pose matrix of the Radar frame.

### Data Organization for Matching Results

All the matching results are stored in folder `results`. Matching results for each { $\{< k, j >}$ } $_j$ is compressed as `.rar` file. The data organization of each `.rar` file is as shown as following: 

```text
boreas-YYYY-MM-DD-HH-MM
|---LiDAR-Iris
|   |--1
|      -loop_result.txt
|      -que_frame_pose.txt
|      -query_ref_id.txt
|      -ref_frame_pose.txt
|   |--2
|      - ...
|   |--3
|      - ...
|   |--4
|      - ...
|   |--5
|      - ...
|---LiDAR-Iris-radar
|   |-- ...
|---MinkLoc3Dv2
|   |-- ...
|---OverlapTransformer
|   |-- ...
|---Scan Context
|   |-- ...
|---Scan Context-radar
|   |-- ...
```

`loop_result.txt` is the top-1 matching results for each query frame of the query sequence. The $1^{th}$ column is the ID of frame in query sequence. The $2^{nd}$ column is the ID of the matching frame in reference sequence. The $3^{th}$ column is the cosine distance between the query frame and matching frame.
```text
loop_result.txt
|-- 0 3304 0.181415737
    ...
```

`que_frame_pose.txt` is the ground-truth pose of the query frame. The $1^{th}$ column refers to `x` coordinate. The $2^{nd}$ column refers to `y` coordinate. The $3^{th}$ column refers to `z` coordinate. 
```text
que_frame_pose.txt
|-- -4.318759337 0.052690267 0.025194207
    ...
```

`ref_frame_pose.txt` is the ground-truth pose of the reference frame. The $1^{th}$ column refers to `x` coordinate. The $2^{nd}$ column refers to `y` coordinate. The $3^{th}$ column refers to `z` coordinate. 
```text
ref_frame_pose.txt
|-- -0.001453277 -0.002786294 0.129992412
    ...
```

`query_ref_id.txt` records the sequence IDs for query sequence and reference sequence used for the current folder. 
```text
ref_frame_pose.txt
|-- -0.001453277 -0.002786294 0.129992412
    ...
```
