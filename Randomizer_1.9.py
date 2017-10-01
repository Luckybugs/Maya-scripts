# 
# Author: Jelena Jovanovic
# Date: sep 2017
# 
# 

# Randomizer script
# 
# Rotates and translates user selected polygonal meshes randomly
# 
# 
# 
# 
# 
import maya.cmds as cmds
import random
import functools


def createUI(pWindowTitle, pApplyCallback, pRestoreCallback):

    windowID = 'MyWindowID' #svaki prozor ima unique identifier da bi samo jedan bio otvoren at a time
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)


    cmds.window(windowID, title=pWindowTitle, sizeable=True, resizeToFitChildren=True)

    cmds.columnLayout(adjustableColumn=True)
    
    
    cmds.separator( h=10, style='none' )
    cmds.text('nameHere', label='Olgic lovi misa, pomeri slajdere da joj pomognes!')
    cmds.separator( h=10, style='none' )
    
    
    cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1,240), (2,40)], columnOffset=[(1,'left',3), (2,'left',10), (3,'left',3), (4,'left',3),  (5,'right',3)]) 

    
    # Move controls
    moveInputField = cmds.floatSliderGrp( label='move:', field=True, fieldMinValue=0, fieldMaxValue=5, minValue=0, maxValue=10, precision=2, value=0.01, step=.01,
                                                                                        columnWidth3= [40,50,150], columnAlign3=['left','both','left'])
    mcbx = cmds.checkBox(label='X', value=True)
    mcby = cmds.checkBox(label='Y', value=True)
    mcbz = cmds.checkBox(label='Z', value=True)
    cmds.separator( h=20, style='none' )
   
    # Rotate controls
    rotateInputField = cmds.floatSliderGrp(label='rotate:', field=True, fieldMinValue=0, fieldMaxValue=100, minValue=0, maxValue=100, precision=2, step=.01, value=5, 
                                                                                       columnWidth3= [40,50,150], columnAlign3=['left','both','left'] )
    rcbx = cmds.checkBox(label='X', value=True)
    rcby = cmds.checkBox(label='Y', value=True)
    rcbz = cmds.checkBox(label='Z', value=True)
    cmds.separator( h=20, style='none' )

    # Scale controls
    scaleInputField = cmds.floatSliderGrp(label='scale:', field=True, fieldMinValue=0, fieldMaxValue=1, minValue=0, maxValue=1, precision=2, value=0.01, step=.01, 
                                                                                       columnWidth3= [40,50,150], columnAlign3=['left','both','left'],  )
    scbx = cmds.checkBox(label='X', value=True)
    scby = cmds.checkBox(label='Y', value=True)
    scbz = cmds.checkBox(label='Z', value=True)
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )



    # new dictionary to hold original positons..
    beforeData = {}



    # Buttons 
 
    cmds.button(label="Randomise", width=240, command=functools.partial(pApplyCallback,
                                                                moveInputField,
                                                                mcbx,mcby,mcbz,
                                                                rotateInputField,
                                                                rcbx,rcby,rcbz,
                                                                scaleInputField,
                                                                scbx,scby,scbz,
                                                                beforeData,))  
    
    cmds.button(label="Restore", width=100, command=functools.partial(pRestoreCallback, beforeData))
    cmds.separator( h=25, style='none' )
    
    
    cmds.showWindow()


def translater(sel, procenat, chekBoxes):
    # Translate selekcije

    for item in sel:
        myTransX = item + '.translateX'
        myTransY = item +'.translateY'
        myTransZ = item + '.translateZ'
        
        
        oldTransX = cmds.getAttr(myTransX)
        oldTransY = cmds.getAttr(myTransY)
        oldTransZ = cmds.getAttr(item+'.translateZ')
        
        #print 'Old transform is:', oldTransX, oldTransY, oldTransZ

        transX = oldTransX + random.uniform(-procenat, procenat)
        transY = oldTransY + random.uniform(-procenat, procenat)
        transZ = oldTransZ + random.uniform(-procenat, procenat)
        #print transX, transY,transZ
        
        if chekBoxes[0]:
          cmds.setAttr(myTransX, transX)
        if chekBoxes[1]:
          cmds.setAttr(myTransY, transY)
        if chekBoxes[2]:
          cmds.setAttr(myTransZ, transZ)


def rotor(sel, procenat, chekBoxes):
    # Rotacija selekcije
  
    razmera = (360.0*procenat)/100


    for item in sel:

        myRotateX = item + '.rotateX'
        myRotateY = item + '.rotateY'
        myRotateZ = item + '.rotateZ'
       
        xosa = random.uniform(0, razmera)
        yosa = random.uniform(0, razmera)
        zosa = random.uniform(0, razmera)

        if chekBoxes[0]:
            cmds.setAttr(myRotateX, xosa )
        if chekBoxes[1]:
            cmds.setAttr(myRotateY, yosa )
        if chekBoxes[2]:
            cmds.setAttr(myRotateZ, zosa )


def scaler(sel, procenat, chekBoxes):
     # Scale selekcije
   
     for item in sel:
        myScaleX = item + '.scaleX'
        myScaleY = item + '.scaleY'
        myScaleZ = item + '.scaleZ'
        
        oldScaleX = cmds.getAttr(myScaleX)
        oldScaleY = cmds.getAttr(myScaleY)
        oldScaleZ = cmds.getAttr(myScaleZ)
        #print 'Old scale is:', oldScaleX, oldScaleY, oldScaleZ

        scaleX = oldScaleX + random.uniform(-procenat, procenat)
        scaleY = oldScaleX + random.uniform(-procenat, procenat)
        scaleZ = oldScaleX + random.uniform(-procenat, procenat)
        
        if chekBoxes[0]:
          cmds.setAttr(myScaleX, scaleX)
        if chekBoxes[1]:
          cmds.setAttr(myScaleY, scaleY)
        if chekBoxes[2]:
          cmds.setAttr(myScaleZ, scaleZ)


def find_poly_obj(sel):
    # Finds only poly objects in a selection
    poly_obj = []
  
    for item in sel:
        shapes = cmds.listRelatives(item, shapes=True)
    
        if (cmds.nodeType(shapes[0]) == 'mesh'):
            poly_obj.append(item)

    return poly_obj


def get_original_pos(polys, beforeData):
    
    for item in polys:
        
        if item not in beforeData:

            pos = cmds.getAttr(item +'.translate')[0]
            rot = cmds.getAttr(item +'.rotate')[0]
            scl = cmds.getAttr(item +'.scale')[0]

            currentDict = {
                         'pos': pos,
                         'rot': rot,
                         'scl': scl
                         }
            beforeData[item] = currentDict

    return beforeData


def restore_to_original_position(sel, polyData):

    for item in sel:
        if item in polyData:
            pos = polyData[item]['pos']
            cmds.setAttr(item + '.translate', pos[0], pos[1], pos[2])
            rot = polyData[item]['rot']
            cmds.setAttr(item + '.rotate', rot[0], rot[1], rot[2])
            scl = polyData[item]['scl']
            cmds.setAttr(item + '.scale', scl[0], scl[1], scl[2])
        else:
            print item +' skiping restore..'


def applyCallback(pMoveInputField, pmcbx,pmcby,pmcbz, pRotateInputField, prcbx,prcby,prcbz, pScaleInputField, pscbx,pscby,pscbz, pBeforeData, *pArgs):

    print 'Randomize button presed!'
    
    inputTranslate = cmds.floatSliderGrp( pMoveInputField, query=True, value=True)

    
    inputMcbx = cmds.checkBox( pmcbx, query=True, value=True)
    inputMcby = cmds.checkBox( pmcby, query=True, value=True)
    inputMcbz = cmds.checkBox( pmcbz, query=True, value=True)
    
    inputTranslateCheckBox = [inputMcbx, inputMcby, inputMcbz]
    

    inputRotate = cmds.floatSliderGrp( pRotateInputField, query=True, value=True)
    
    inputRcbx = cmds.checkBox( prcbx, query=True, value=True)
    inputRcby = cmds.checkBox( prcby, query=True, value=True)
    inputRcbz = cmds.checkBox( prcbz, query=True, value=True)
    
    inputRotateCheckBox = [inputRcbx, inputRcby, inputRcbz]
    
   
    inputScale = cmds.floatSliderGrp( pScaleInputField, query=True, value=True)
    
    
    inputScbx = cmds.checkBox( pscbx, query=True, value=True)
    inputScby = cmds.checkBox( pscby, query=True, value=True)
    inputScbz = cmds.checkBox( pscbz, query=True, value=True)
    
    inputScaleCheckBox = [inputScbx, inputScby, inputScbz]
    



    selection = cmds.ls(selection = True)
    sel = find_poly_obj(selection)

    if len(sel) == 0:
        cmds.warning('No polygonal objects selected!')

    # geting originals before we randomize it
    get_original_pos(sel, pBeforeData)

    translater(sel, inputTranslate,inputTranslateCheckBox)
    rotor(sel, inputRotate, inputRotateCheckBox)
    scaler(sel, inputScale, inputScaleCheckBox)


def restoreCallback(pBeforeData, *pArgs):

    print 'Restore button presed!'

    selection = cmds.ls(selection = True)
    sel = find_poly_obj(selection)

    # restoring those we have moved
    restore_to_original_position(sel, pBeforeData)






createUI('Rand All The Things!!! 1.0', applyCallback, restoreCallback)
