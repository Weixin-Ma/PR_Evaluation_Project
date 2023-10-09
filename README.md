# PR_Evaluation_Project
A Comprehensive Evaluation on Range Sensor-based Long-term Place Recognition in Large-scale Urban Environment

## Obejctive
The performance of long-term place recognition can easily change with the variation of environmental conditions, especially the variation of weather and traffic condition. To have a deep understanding about this problem,we conducted a comprehensive evaluation of several SOTA range-sensor-based place recognition techniques on a long-term public dataset, Borease, which contains stark weather and traffic condition variation. We also proposed two new metrics to evaluate the effect of matching threshold setting on long-term place recognition performance

## Raw Data
All the results in the paper can be found in this repository.

### Data Organization for Matching Results

All the matching results are stored in folder `results`. Matching results for each $\{<k , j>\}_j$ is compressed as `.rar` file. The data organization of each `.rar` file is as shown as following: 

```text
boreas-YYYY-MM-DD-HH-MM
	LiDAR-Iris
		1
			loop_result.txt
			que_frame_pose.txt
			query_ref_id.txt
			ref_frame_pose.txt
		2
			...
		3
			...
		4
			...
		5
			...
	LiDAR-Iris-radar
		...
	MinkLoc3Dv2
		...
	OverlapTransformer
		...
	Scan Context
		...
	Scan Context-radar
		...
```
