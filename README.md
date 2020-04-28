Copyright (C) 2020 RIKEN

## Synopsis
* This repository contains the source codes for bd5lint, a tool that analyzes BD5 file format and flag syntactic errors and suspicious constructs.

## Usage
usage: bd5lint.py [-h] [-v] FILE

Validation of BD5 formatted files.

positional arguments:
  FILE           BD5 formatted filename

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  verbose mode (default: False)

For example: 
    python3 bd5lint.py -v test/testbd5_dim_3D_t1.h

## Detailed description
Detailed description can be found on the link below.
https://docs.google.com/document/d/1x6oTgNifqhn9RXEuFVs2J4ByT_mDJ-Pzp0RLT3cwibw/edit?usp=sharing

## Test

* Functional Test

  python3 functional_test.py

1. - invalid BD5 file with no data group.
        "test/testbd5_data1.h5",  
2. - invalid BD5 file with missing element 
        "test/testbd5_data_01.h5",  
3. - invalid BD5 file with object t1 which is not in objectDef.
        "test/testbd5_data_0_object_t1.h5",  
4. - invalid BD5 file with dim 2D but it has z dimension.
        "test/testbd5_dim_2t_bd5.h5",  
5. - valid BD5 file with dim 3D
        "test/testbd5_dim_3D.h5",  
6. - invalid BD5 file - object entity is a line but it has radius
        "test/testbd5_line_radius.h5",  
7. invalid BD5 file - it has object1 instead of the correct syntax object
        "test/testbd5_object1.h5",  
8. invalid BD5 file with no objectDef
        "test/testbd5_objectDef1.h5",  
9. - invalid BD5 file with dim as 3D, but with inconsistent entity 'line' at ID 1_47.
        "test/testbd5_object_0_1_47_points.h5",  
10. - invalid BD5 file with no scaleUnit
        "test/testbd5_scaleUnit1.h5", 
11. - invalid BD5 file with entity sphere but no radius
        "test/testbd5_sphere_no_radius.h5",  
12. - invalid BD5 file with dim as 3D, but with inconsistent entity 'line' at ID 1_41.
        "test/testbd5_dim_3D_I_41_line.h5",  
13. - valid BD5 file
        "test/testbd5_dim_3D_t1.h5" 
14. - valid BD5 file with 0D+T dimension
        "test/testbd5_0seed_0D_bd5.h5" 
