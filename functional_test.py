import unittest
import bd5lint as bl
import sys


class Testbd5lintFunction(unittest.TestCase):
    infilename = None
    valid_bd5file = "test/testbd5_dim_3D.h5"
    v = bl.bd5lint()
    filelist = [ 
        # 1. - invalid BD5 file with no data group.
        "test/testbd5_data1.h5",  
        # 2. - invalid BD5 file with missing element 
        "test/testbd5_data_01.h5",  
        # 3. - invalid BD5 file with object t1 which is not in objectDef.
        "test/testbd5_data_0_object_t1.h5",  
        # 4. - invalid BD5 file with dim 2D but it has z dimension.
        "test/testbd5_dim_2t_bd5.h5",  
        # 5. - valid BD5 file with dim 3D
        "test/testbd5_dim_3D.h5",  
        # 6. - invalid BD5 file - object entity is a line but it has radius
        "test/testbd5_line_radius.h5",  
        # 7. invalid BD5 file - it has object1 instead of the correct syntax object"
        "test/testbd5_object1.h5",  
        # 8. invalid BD5 file with no objectDef"
        "test/testbd5_objectDef1.h5",  
        # 9. - invalid BD5 file with dim as 3D, but with inconsistent entity 'line' at ID 1_47.
        "test/testbd5_object_0_1_47_points.h5",  
        # 10. - invalid BD5 file with no scaleUnit
        "test/testbd5_scaleUnit1.h5", 
        # 11. - invalid BD5 file with entity sphere but no radius"
        "test/testbd5_sphere_no_radius.h5",  
        # 12. - invalid BD5 file with dim as 3D, but with inconsistent entity 'line' at ID 1_41."
        "test/testbd5_dim_3D_I_41_line.h5",  
        # 13. - valid BD5 file"
        "test/testbd5_dim_3D_t1.h5", 
        # 14. - valid BD5 file with 0D+T dimension
        "test/testbd5_0seed_0D_bd5.h5"
    ]
    
    def testbd5file(self):
        if self.infilename == None:
            self.infilename = self.valid_bd5file
#            print("FAIL: no file name")
#            return(False)
        # check hdf5file for consistency.
        self.assertEqual(self.v.hdf5file(self.infilename), True) 
        
    def testscaleUnit(self):
        expected_ans = [False, True, True, True, True, True, True, True, True, False, True, True, True, True ]
        checkfiles = list(map(lambda x, y:[x, y], self.filelist, expected_ans))
        # check scaleUnit for consistency.
        for i in checkfiles:
            self.infilename = i[0]
            try:
                self.assertEqual(self.v.dataset(i[0], 'scaleUnit', ['dimension']), i[1]) 
                print("functional test: pass scaleUnit %s" % self.infilename)
            except: 
                (etype, evalue, etrace) = sys.exc_info()
                self.fail("Error on: %s" % i)
           
    def testobjectDef(self):
        # check objectDef for consistency.
        expected_ans = [False, True, True, True, True, True, True, False, True, False, True, True, True, True ]
        checkfiles = list(map(lambda x, y:[x, y], self.filelist, expected_ans))
        for i in checkfiles:
            self.infilename = i[0]
            try:
                self.assertEqual(self.v.dataset(i[0], 'objectDef', ['oID', 'name']), i[1])
                print("functional test: pass objectDef %s" % self.infilename)
            except: 
                (etype, evalue, etrace) = sys.exc_info()
                self.fail("Error on: %s" % i)
    
    def testdataGroup(self):
        expected_ans = [False, False, False, False, True, False, False, False, False, False, False, False, True, True ]
        checkfiles = list(map(lambda x, y:[x, y], self.filelist, expected_ans))
        for i in checkfiles:
            self.infilename = i[0]
            try:
                self.assertEqual(self.v.data_group(self.infilename), i[1]) 
                print("functional test: pass datagroup %s" % self.infilename)
            except: 
                (etype, evalue, etrace) = sys.exc_info()
                self.fail("Error on: %s" % i)
    
    def testtrackInfo(self):
        expected_ans = [False, False, False, False, False, True, False, False, False, False, False, False, False, True ]
        checkfiles = list(map(lambda x, y:[x, y], self.filelist, expected_ans))
        for i in checkfiles:
            self.infilename = i[0]
            try:
                self.assertEqual(self.v.dataset(self.infilename, 'trackInfo', ['from', 'to']), i[1])
                print("functional test: pass trackInfo %s" % self.infilename)
            except: 
                (etype, evalue, etrace) = sys.exc_info()
                self.fail("Error on: %s" % i)
        
if __name__ == '__main__':
    unittest.main()
    
