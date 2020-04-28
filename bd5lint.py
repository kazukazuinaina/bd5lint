from __future__ import print_function
import sys
import argparse
import h5py
import numpy as np
from checkbd5 import *


class bd5lint(object):
    object_entity = {}
    """Tests for BD5 format `validateBD5.py`. """
    def hdf5file(self, testfile):
        """ test only HDF5 files and not BD5 file!"""
        try:
            result, fhandle = checkbd5file(testfile)
        except IOError as e:
            opt_print("Checking HDF file format: %s\n" % e)
            return False
        else: 
            opt_print("PASS: found HDF5 file %s" % testfile)
            return True
        
    def group(self, testfile, groupname):
        """ test BD5 file for generic group, given groupname!"""
        try:
            r, f = checkbd5file(testfile)
        except IOError as e:
            print("ERROR: opening BD5 file %s - %s\n" % (groupname, f))
            return False
        try:
            r1, msg1 = checkbd5group(f[groupname])
        except KeyError as e:
            print("ERROR: cannot find group %s - %s\n" % (groupname, msg1))
            return False
        else:
            opt_print("PASS: found group %s" % groupname)
            sizeofgroup = len(f[groupname])
            opt_print("PASS: found %d time pt elements" % sizeofgroup)
            return True
    
    def data_timeseries(self, f): # f is a filehandle
        """ testing whether the timeseries in /data is continuous """
        # Finding the number of group elements in filehandle["data"]
        maxgroup = len(list(filter((lambda x: isinstance(f["data/"+x], h5py.Group)==True), f["data"])))
        #print("maxgroup:", maxgroup)
        # get the time series list tslist for all the elements in the f["data"] which is a h5py.Group
        tslist = list(filter((lambda x: isinstance(f["data/"+x], h5py.Group)==True), f["data"]))
        #print(tslist)
        # From 0 to maxgroup, find the missing element in a timeseries list
        r1 = list(filter(lambda x: str(x) not in tslist, range(0,maxgroup))) 
        # finding extra elements in timeseries tslist that are not between 0 and maxgroup
        r2 = list(filter(lambda x: x not in list(map(str, range(0,maxgroup))), tslist))
        if r1 == [] and r2 == []: # Pass if only both conditions are true
            opt_print("PASS: No missing or extra element")
            return True
        if r1 != []:
            print("FAIL: Missing element", *r1)
        if r2 != []:
            print("FAIL: Found extra element", *r2)
        return False

    def checkbd5Obj(self, timept_objlst, objlst):
        resultlst = list(filter(lambda x: x not in list(map(str, objlst)), timept_objlst)) 
        if resultlst == []:
            opt_print("PASS: found object in objectDef")
            return True
        else:
            print('FAIL: object/s not found in objectDef:', *resultlst)
# The following usage is more desirable. However, this won't work unless python version is > Python3.5
#            print('FAIL: ', *resultlst, 'not found in objectDef')
            return False

    def data_group(self, testfile):
        """ test BD5 file for group!"""
        try:
            r, f = checkbd5file(testfile)
        except IOError as e:
            print("ERROR: opening BD5 file %s - %s\n" % (testfile, f))
            return False
        try:
            r1, msg1 = checkbd5group(f['data'])
        except KeyError as e:
            print("ERROR: cannot find group %s - %s\n" % ('data', e))
            return False
        opt_print("PASS: found group %s" % 'data')
        if self.data_timeseries(f) == False:
            print("ERROR: time series in group data is inconsistent")
            return False
        else:
            tslist = list(filter((lambda x: isinstance(f["data/"+x], h5py.Group)==True), f["data"]))
            for i in tslist:
                try: 
                    opt_print("PASS: found datagroup "+i)
                    for j in f['data/'+i]: # for j in f['data'].keys():
                        sizeofgroup_i = len(f['data/'+i])
                        if sizeofgroup_i <1:
                            print("ERROR: group data/%s does not have any data - %d\n" % (i, sizeofgroup_i))
                        else:
                            opt_print("PASS: found %d elements" % sizeofgroup_i)
                            if (str(j) == 'object'):
                                opt_print("PASS: found "+j)
                                # need to test whether k is an element in objectDef
                                if self.checkbd5Obj(f['data/'+i+'/object/'], f['data/objectDef']['oID']):
                                    #dim = np.char.decode(f['data/scaleUnit']["dimension"]) 
                                # check if dim is 0D, if it is not, continue, else skip
                                    #print("checking scaleUnit/dimension")
                                    if checkbd5dataset(f['/data/scaleUnit']) == False:
                                        print("ERROR: cannot find scaleUnit")
                                        return False
                                    else:
                                        opt_print("PASS: found scaleunit, checking dimension")
                                    if checkbd5attribute(f['/data/scaleUnit'], 'dimension', 'string') == False:
                                        print("ERROR: cannot find dimension in scaleUnit")
                                        return False
                                    else:
                                        opt_print("PASS: found scaleUnit/dimension %s" % np.char.decode(f['data/scaleUnit']['dimension'][0]))
                                    if (np.char.decode(f['data/scaleUnit']['dimension'][0])) != "0D" and (np.char.decode(f['data/scaleUnit']['dimension'][0])) != "0D+T": # 0D or 0D+T  
                                        #print("not 0D or 0D+T but ", f['data/scaleUnit']['dimension'])
                                        for k in f['data/'+i+'/'+j]:
                                        # check whether the entity in f['data/0/object/0/] has valid values
                                            try:
                                                self.object_entity[k] = np.char.decode(f['data/'+i+'/'+j+'/'+k]['entity'][0])
                                                #print("Checking whether the entity %s in data/%s/%s/%s is valid" % (self.object_entity[k], i, j, k))
                                                r11 = checkbd5entity(f['data/'+i+'/'+j+'/'], self.object_entity[k]) 
                                                if r11 != True:
                                                    print("ERROR: %s" % r11[1])
                                                    return False
                                                else:
                                                    opt_print("PASS: entity %s is valid" % self.object_entity[k])
                                            except KeyError as e: 
                                                print("ERROR: %s" % msg11)
                                                return False
                                            try:
                                            # check whether the entity in f['data/0/object/0/] are the same
                                                if checkbd5entity(f['data/'+i+'/'+j+'/']) == True:
                                                    opt_print("PASS: entities in data/%s/%s/%s are all the same" % (i, j, k))
                                                else:
                                                    print("ERROR: entities in data/%s/%s/%s'" % (i, j, k))
                                                    return False
                                            except KeyError as e: 
                                                return msg12
                                            attriblist = f['data/'+i+'/'+j+'/'+k].dtype.names
                                            # opt_print(attriblist)
                                            if self.dataset(testfile, i+'/'+j+'/'+k, attriblist) == False:
                                                print("ERROR: dimension is not consistent %s %s" % (j, i))
                                                return False
                                            else:
                                                #return True
                                                opt_print("PASS: finsih checking "+j)
                                        else:
                                            print("It has 0 Dimension")
                                else:
                                    print("ERROR: %s not found in objectDef" % j)
                                    return False
                            elif (str(j) == 'feature'):
                                opt_print("PASS: found "+j)
                                for k in f['data/'+i+'/'+j]:
                                    self.dataset(testfile, i+'/'+j+'/'+k, ('ID', 'fID', 'value'))
                                    opt_print("PASS: finsih checking "+j)
                                #return True
                            else:
                                print("ERROR: found %s instead of object or feature" % j)
                                return False
                except KeyError as e:
                    print("ERROR: ts cannot find group %s - %s\n" % ('data', e))
                    return False
            return True


 
    def dataset(self, testfile, setname, attributeList):
        """ test BD5 file for dataset attribute list and see whether they conform to BD5 types!"""
        mandatoryobjectlist_3DT_r = ['ID', 'entity', 'x', 'y', 'z', 't', 'radius']
        mandatoryobjectlist_3DT = ['ID', 'entity', 'x', 'y', 'z', 't']
        mandatoryobjectlist_3D_r = ['ID', 'entity', 'x', 'y', 'z', 'radius']
        mandatoryobjectlist_3D = ['ID', 'entity', 'x', 'y', 'z']
        mandatoryobjectlist_2DT_r = ['ID', 'entity', 'x', 'y', 't', 'radius']
        mandatoryobjectlist_2DT = ['ID', 'entity', 'x', 'y', 't']
        mandatoryobjectlist_2D = ['ID', 'entity', 'x', 'y']
        mandatoryobjectlist_2D_r = ['ID', 'entity', 'x', 'y', 'radius']
        mandatoryobjectlist_1DT = ['ID', 'entity', 'x', 't']
        mandatoryobjectlist_1D = ['ID', 'entity', 'x']
        mandatoryobjectlist_0DT = ['ID', 'entity', 't']
        mandatoryobjectlist_0D = ['ID', 'entity']
        # hybridtypelist contains a list of attributes that can allows various types, float and string.
        hybridtypelist_3DT_r = ['x', 'y', 'z', 't', 'radius', 'xScale', 'yScale', 'zScale', 'tScale']
        hybridtypelist_3DT = ['x', 'y', 'z', 't', 'xScale', 'yScale', 'zScale', 'tScale']
        hybridtypelist_2DT_r = ['x', 'y', 't', 'radius', 'xScale', 'yScale']
        hybridtypelist_2DT = ['x', 'y', 't', 'xScale', 'yScale']
        hybridtypelist_1DT = ['x', 't', 'xScale']
        hybridtypelist_0DT = ['t']
        # floattypelist test those attributes whether they are float 
        #floattypelist = ('x', 'y', 'z', 't', 'xScale', 'yScale', 'zScale', 'tScale', 'radius')
        #floattypelist = ('xScale', 'yScale', 'zScale', 'tScale')
        floattypelist = []
        strtypelist_xDT = ['name', 'ID', 'label', 'entity', 'dimension', 'sUnit', 'tUnit', 'from', 'to']
        strtypelist_xD = ['name', 'ID', 'label', 'entity', 'dimension', 'sUnit', 'from', 'to']
        strtypelist_0D = ['name', 'ID', 'label', 'entity', 'dimension', 'from', 'to']
        inttypelist = ['oID', 'sID']
        try: 
            r, f = checkbd5file(testfile)
        except IOError as e:
            print("ERROR: cannot open file %s : %s\n" % (testfile, e))
            return False
        try:
            r0, msg0 = checkbd5dataset(f['data/scaleUnit'])
            if r0 == False:
#                opt_print("Warnning: cannot find scaleUnit\n")
                return False
        except KeyError as e1:
            opt_print("Warning: cannot find scaleUnit")
            return False
        opt_print("PASS: found scaleUnit")
        dim = np.char.decode(f['data/scaleUnit']['dimension'])
        try:
            r1, msg1 = checkbd5dataset(f['data/'+setname])
            if r1 == False:
#                opt_print("Warnning: cannot find dataset %s\n" % (setname))
                return False
            else:
                opt_print("PASS: found dataset "+setname)
        except KeyError as e1:
#            opt_print("Warning: cannot find dataset %s : %s \n" % (setname, e1))
            opt_print("Warning: cannot find dataset %s \n" % (setname))
            return False
#        if checkbd5attribute(f['data/'+setname], 'entity', 'string') == True:
#            entity = f['data/'+setname]['entity']
#        else:
#                print("ERROR: cannot find dataset %s entity\n" % (setname))
#                return False
        if setname != 'scaleUnit' and setname != 'objectDef' and setname != 'trackInfo' and setname.find('feature') == -1:
            #print("setname= %s" % setname) 
            entity0 = np.char.decode(f['data/'+setname]['entity'][0])
            #print("entity0= %s" % entity0) 
            if dim == '0D':
                hybridtypelist = hybridtypelist_0DT
                strtypelist = strtypelist_0D
                mandatoryobjectlist = mandatoryobjectlist_0D
            elif dim == '0D+T':
                hybridtypelist = hybridtypelist_0DT
                strtypelist = strtypelist_0D
                mandatoryobjectlist = mandatoryobjectlist_0DT
            elif dim == '1D': 
                hybridtypelist = hybridtypelist_1DT
                strtypelist = strtypelist_xD
                mandatoryobjectlist = mandatoryobjectlist_1D
            elif dim == '1D+T': 
                hybridtypelist = hybridtypelist_1DT
                strtypelist = strtypelist_xDT
                mandatoryobjectlist = mandatoryobjectlist_1DT
            elif dim == '2D' and (entity0 == 'line' or entity0 == 'point' or entity0 == 'face'):
                hybridtypelist = hybridtypelist_2DT
                strtypelist = strtypelist_xD
                mandatoryobjectlist = mandatoryobjectlist_2D
            elif dim == '2D' and entity0 == 'circle':
                hybridtypelist = hybridtypelist_2DT_r
                strtypelist = strtypelist_xD
                mandatoryobjectlist = mandatoryobjectlist_2D_r
            elif dim == '2D+T'and (entity0 == 'line' or entity0 == 'point' or entity0 == 'face'): 
                hybridtypelist = hybridtypelist_2DT
                strtypelist = strtypelist_xDT
                mandatoryobjectlist = mandatoryobjectlist_2DT
            elif dim == '2D+T'and entity0 == 'circle':
                hybridtypelist = hybridtypelist_2DT_r
                strtypelist = strtypelist_xDT
            elif dim == '3D' and (entity0 == 'line' or entity0 == 'point' or entity0 == 'face'):  
                hybridtypelist = hybridtypelist_3DT
                strtypelist = strtypelist_xD
                mandatoryobjectlist = mandatoryobjectlist_3D
            elif dim == '3D' and (entity0 == 'sphere' or entity0 == 'circle'):  
                hybridtypelist = hybridtypelist_3DT_r
                strtypelist = strtypelist_xD
                mandatoryobjectlist = mandatoryobjectlist_3D_r
            elif dim == '3D+T' and (entity0 == 'line' or entity0 == 'point' or entity0 == 'face'):  
                hybridtypelist = hybridtypelist_3DT
                strtypelist = strtypelist_xDT
                mandatoryobjectlist = mandatoryobjectlist_3DT
            elif dim == '3D+T' and (entity0 == 'sphere' or entity0 == 'circle'):  
                hybridtypelist = hybridtypelist_3DT_r
                strtypelist = strtypelist_xD
                mandatoryobjectlist = mandatoryobjectlist_3DT_r
            else:
                print("ERROR: not recognised dimension %s " % dim)
                return False
            # Checking whether the attributelist include all the members in the mandatoryobjectlist
            missing_members = list(set(mandatoryobjectlist)-set(attributeList))
            if missing_members != []:
                print("ERROR: missing mandatory attributes %s" % missing_members)
                return False
            for i in attributeList:
                msg2 = "the attribute "+i+" does not have a type defined or inconsistent with the defined dimension " 
                try:
                    if i in floattypelist:
                        r2, msg2 = checkbd5attribute(f['data/'+setname], i, 'float')
                    elif i in hybridtypelist:
                        r2, msg2 = checkbd5attribute(f['data/'+setname], i, 'hybridfloatstring')
                    elif i in strtypelist:
                        r2, msg2 = checkbd5attribute(f['data/'+setname], i, 'string')
                    elif i in inttypelist:
                        r2, msg2 = checkbd5attribute(f['data/'+setname], i, 'integer')
                    else:
                        print("ERROR: %s - %s" % (setname, msg2))
                        return False
                except IOError as e:
                    print("ERROR: cannot find dataset %s : - %s\n" % (setname, e))
                    return False
                except KeyError as e1:
                    opt_print("Warning: cannot find dataset %s attribute  %s - %s\n" % (setname, i, e1))
                    return False
                finally:
                    if (r2 == True):
                        opt_print("PASS: found attribute "+setname+"/"+i+" "+msg2)
                    elif (r2 == False):
                        opt_print("Warning: no attribute "+setname+"/"+i)
        return True
              
   
verbose = False           
def opt_print(text):
    if verbose==True:
        print(text)
    else:
        pass

# Supressing Trace back in exception case            
# ref: https://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set    
#def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
#    if _your_debug_flag_here:
#        debug_hook(exception_type, exception, traceback)
#    else:
#        print("%s: %s" % (exception_type.__name__, exception))


def printusage():
	    print("usage: python bd5lint.py <input filename>")        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validation of BD5 formatted files.')
#    parser.add_argument('-f', '--file', dest="infilename", help='BD5 formatted filename', metavar="FILE")
    parser.add_argument("-v", "--verbose", action='store_true', help='verbose mode (default: False)')
    parser.add_argument(dest='infilename', help='BD5 formatted filename', metavar="FILE")
    args = parser.parse_args()
    infilename = args.infilename
    if args.verbose:
        verbose = True
        print("verbosity turned on")
#    print(args.infilename)
#    print(args.verbose)

    try: 
        v = bd5lint()
        if infilename == None:
            print("FAIL: no file name")
            quit() 
        # check hdf5file for consistency.
        if v.hdf5file(infilename) == False:
            print("FAIL: cannot open hdf5 file")
            quit()
        if v.data_group(infilename) == False:
            print("FAIL: data_group")
            quit()
        # check scaleUnit for consistency.
#        if v.dataset(infilename, 'scaleUnit', ['xScale', 'yScale', 'zScale', 'tScale', 'dimension', 'sUnit', 'tUnit']) == False:
        if v.dataset(infilename, 'scaleUnit', ['dimension']) == False:
            print("FAIL: cannot find dataset scaleUnit")
            quit()
        # check objectDef for consistency.
        if v.dataset(infilename, 'objectDef', ['oID', 'name']) == False:
            print("FAIL: cannot find dataset objectDef")
            quit()
        else:
            opt_print("Finished testing data_group")
        if v.dataset(infilename, 'trackInfo', ['from', 'to']) == False:
#            opt_print("WARNING: cannot find dataset trackInfo")
            pass
    except RuntimeError as e:
        print("Runtime error: %s" % e)
    else:
        print("Finish checking file %s" % infilename)