#!/bin/bash
echo "python bd5lint.py -v testbd5_data1.h5 - invalid BD5 file with no data group."
python bd5lint.py -v test/testbd5_data1.h5
echo "python bd5lint.py -v testbd5_data_01.h5 - invalid BD5 file with missing element 0."
python bd5lint.py -v test/testbd5_data_01.h5
echo "python bd5lint.py -v testbd5_data_0_object_t1.h5 - invalid BD5 file with object t1 which is not in objectDef."
python bd5lint.py -v test/testbd5_data_0_object_t1.h5
echo "python bd5lint.py -v testbd5_dim_2t_bd5.h5 - invalid BD5 file with dim 2D but it has z dimension."
python bd5lint.py -v test/testbd5_dim_2t_bd5.h5
echo "python bd5lint.py -v testbd5_dim_3D.h5 - valid BD5 file with dim 3D"
python bd5lint.py -v test/testbd5_dim_3D.h5
echo "python bd5lint.py -v testbd5_line_radius.h5 - invalid BD5 file - object entity is a line but it has radius"
python bd5lint.py -v test/testbd5_line_radius.h5 
echo "python bd5lint.py -v testbd5_object1.h5 - invalid BD5 file - it has object1 instead of the correct syntax object"
python bd5lint.py -v test/testbd5_object1.h5 
echo "python bd5lint.py -v testbd5_objectDef1.h5 - invalid BD5 file with no objectDef"
python bd5lint.py -v test/testbd5_objectDef1.h5
echo "python bd5lint.py -v testbd5_object_0_1_47_points.h5 - invalid BD5 file with dim as 3D, but with inconsistent entity 'line' at ID 1_47."
python bd5lint.py -v test/testbd5_object_0_1_47_points.h5 
echo "python bd5lint.py -v testbd5_scaleUnit1.h5 - invalid BD5 file with no scaleUnit"
python bd5lint.py -v test/testbd5_scaleUnit1.h5
echo "python bd5lint.py -v testbd5_sphere_no_radius.h5 - invalid BD5 file with entity sphere but no radius"
python bd5lint.py -v test/testbd5_sphere_no_radius.h5 
echo "python bd5lint.py -v testbd5_dim_3D_I_41_line.h5 - invalid BD5 file with dim as 3D, but with inconsistent entity 'line' at ID 1_41."
python bd5lint.py -v test/testbd5_dim_3D_I_41_line.h5 
echo "python bdbd5lint.py -v testbd5_dim_3D_t1.h5 - valid BD5 file"
python bd5lint.py -v test/testbd5_dim_3D_t1.h5 
echo "python bd5lint.py -v test/testbd5_0seed_0D_bd5.h5 - valid BD5 file with 0D+T dimension"
python bd5lint.py -v test/testbd5_0seed_0D_bd5.h5 