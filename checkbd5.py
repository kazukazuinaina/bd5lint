# checkbd5.py
import h5py
import numpy as np

def checkbd5group(datahandle):
    if isinstance(datahandle, h5py.Group) == False:
        errormsg = 'error: no data Group found'
        return False, errormsg
    else:
        errormsg = 'error: none'
        return True, errormsg
        
def checkbd5dataset(datahandle):
    if isinstance(datahandle, h5py.Dataset) == False:
        errormsg = 'error: no data set found'
        return False, errormsg
    else:
        errormsg = 'error: none'
        return True, errormsg
        
        
def checkbd5attribute(datahandle, attribute, typedef):
#    print("running checkbd5attribute")
    if isinstance(datahandle, h5py.Dataset) == False:
        errormsg = 'error: no Dataset found'
        return False, errormsg
    if (attribute in datahandle.dtype.names) == False:
        errormsg = 'error: '+attribute+'not found'
        return False, errormsg
    elif (attribute in datahandle.dtype.names) == True:
#        print(attribute+"is found!!!!")
        if (typedef == 'float'):
            if ((isinstance(datahandle[attribute][0], np.float32)) or isinstance(datahandle[attribute][0], np.float64)) == True:
#                print("checkingfloat      %s, %s" % (attribute, type(datahandle[attribute][0])))
#                errormsg = 'error: none'
#                return True, "float"
                return True, str(datahandle[attribute][0].dtype)
            else:
                errormsg = "error: not a float type"
#                print("      %s, %s" % (attribute, type(datahandle[attribute][0])))
                print(errormsg)
                return False, errormsg 
        elif (typedef == 'hybridfloatstring'):
            if ((isinstance(datahandle[attribute][0], np.float32)) or 
                isinstance(datahandle[attribute][0], np.float64) or 
                isinstance(datahandle[attribute][0], np.bytes_))  == True:
#                print("checkingfloat      %s, %s" % (attribute, type(datahandle[attribute][0])))
#                errormsg = 'error: none'
#                return True, "float"
                return True, str(datahandle[attribute][0].dtype)
            else:
                errormsg = "error: not a float or string type"
#                print("      %s, %s" % (attribute, type(datahandle[attribute][0])))
                print(errormsg)
                return False, errormsg 
 
        elif (typedef == 'string'):
#            print("checkbd5 - isinstance a np.string")
#            print("checkbd5 - the type of %s, %s" % (attribute, type(datahandle[attribute][0])))
#            print("isinstance np.bytes_ is %s" % (isinstance(datahandle[attribute][0], np.bytes_))) 
            if (isinstance(datahandle[attribute][0], np.bytes_)):
#                print("checkbd5 - isinstance is a np.bytes_")
#                print("Pass bytes      %s, %s" % (attribute, type(datahandle[attribute][0])))
#                errormsg = 'error: none'
#                return True, "string"
                return True, str(datahandle[attribute][0].dtype)
#                print("this shouldn't run!")
            elif (isinstance(datahandle[attribute][0], np.string_)) == True:
#                print("Pass string      %s, %s" % (attribute, type(datahandle[attribute][0])))
#                errormsg = 'error: none'
                return True, str(datahandle[attribute][0].dtype)
            else:
                errormsg = "error: not a string type"
#                print("error part!      %s, %s" % (attribute, type(datahandle[attribute][0])))
                print(errormsg)
                return False, errormsg 
        elif (typedef == 'integer'):
            if (isinstance(datahandle[attribute][0], np.integer)):
#                print("      %s, %s" % (attribute, type(datahandle[attribute][0])))
#                errormsg = 'error: none'
#                return True, "integer"
                return True, str(datahandle[attribute][0].dtype)
            else:
                errormsg = "error: not a integer type"
#                print("      %s, %s" % (attribute, type(datahandle[attribute][0])))
                print(errormsg)
                return False, errormsg 
        else:
                errormsg = "error: undefined type"
#                print("      %s, %s" % (attribute, type(datahandle[attribute][0])))
                print(errormsg)
                return False, errormsg 
    else:
        print(errormsg)
        return False, errormsg 

def checkbd5entity(datahandle, entity=None):            
    if isinstance(datahandle, h5py.Group) == False:
        errormsg = 'error: no Group found'
        return False, errormsg
    # check each entry on the validity of the entity tag. 
    if entity == None:
        # print("Checking whether entities are eligible")
        entitylist = ['point', 'line', 'face', 'circle', 'sphere']
    else:
    # check each entry and see whether it has the same entity tag. 
        entitylist = [entity]
    for i in datahandle: # for i in f['data/'+t+'/object/']
        if isinstance(datahandle[i], h5py.Dataset) == False:
            errormsg = 'error: no Dataset found'
            return False, errormsg
        for j in datahandle[i]:
            data_entity = np.char.decode(j['entity'])
            entity_check = False
            for k in entitylist:
                # check whether the entity is one that is allowed in the entitylist
                #print(k, data_entity)
                if  data_entity == k:
                    entity_check = True
            if entity_check == False:
                errormsg = "entity %s is not eligible or differ, ID=%s" % (data_entity,np.char.decode(j['ID']))
                return False, errormsg 
    return True       
            
def checkbd5file(filename):
    f = h5py.File(filename, "r")
    if isinstance(f, h5py.File) == False:
        errormsg = "error: cannot find h5file"
        print(errormsg)
        return False, errormsg
    else:
        return True, f