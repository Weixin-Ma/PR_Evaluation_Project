# PR_Evaluation_Project
A Comprehensive Evaluation on Range Sensor-based Long-term Place Recognition in Large-scale Urban Environment

## Obejctive
The performance of long-term place recognition can easily change with the variation of environmental conditions, especially the variation of weather and traffic condition. To have a deep understanding about this problem,we conducted a comprehensive evaluation of several SOTA range-sensor-based place recognition techniques on a long-term public dataset, Borease, which contains stark weather and traffic condition variation. We also proposed two new metrics to evaluate the effect of matching threshold setting on long-term place recognition performance

## Raw Data
All the results in the paper can be found in this repository.

### Data Organization for Matching Results

All the matching results are stored in folder `results`.

```text
boreas-YYYY-MM-DD-HH-MM
	applanix
		camera_poses.csv
		gps_post_process.csv
		lidar_poses.csv
		radar_poses.csv
	calib
		camera0_intrinsics.yaml
		P_camera.txt
		T_applanix_lidar.txt
		T_camera_lidar.txt
		T_radar_lidar.txt
	camera
		<timestamp>.png
	lidar
		<timestamp>.bin
	radar
		<timestamp>.png
	route.html
	video.mp4
```
