#! /usr/bin/env python
#This is free software
"""
Rotates and translates user selected polygonal meshes randomly.
.. module:: `Randomizer`
   :platform: Unix, Windows
   :synopsis: Rotates and translates user selected polygonal meshes randomly.
.. moduleauthor:: Jelena Jovanovic <djurovic.jelena@gmail.com>
"""

# IMPORT STANDARD MODULES
import random
import functools

# IMPORT LOCAL MODULES
import maya.cmds as cmds

def create_ui(pWindowTitle, pApplyCallback, pRestoreCallback):
    """
        creating UI.
    """
    # each window has a unique identifier so only one would be opened at a time
    window_id = 'Mywindow_id' 
    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)

    cmds.window(window_id, title=pWindowTitle, sizeable=True, 
                resizeToFitChildren=True)

    cmds.columnLayout(adjustableColumn=True)

    cmds.separator(h=10, style='none')

    cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 240), (2, 40)],
                         columnOffset=[(1, 'left', 3), (2, 'left', 10),
                                       (3, 'left', 3), (4, 'left', 3),
                                       (5, 'right', 3)])
    
    # Move controls
    move_input_field = cmds.floatSliderGrp(label='move:', field=True,
                                           fieldMinValue=0, fieldMaxValue=5, 
                                           minValue=0, maxValue=10, precision=2,
                                           value=0.01, step=.01,
                                           columnWidth3=[40, 50, 150],
                                           columnAlign3=['left', 'both', 'left'])

    mcbx = cmds.checkBox(label='X', value=True)
    mcby = cmds.checkBox(label='Y', value=True)
    mcbz = cmds.checkBox(label='Z', value=True)
    cmds.separator(h=20, style='none')
   
    # Rotate controls
    rotate_input_field = cmds.floatSliderGrp(label='rotate:', field=True,
                                             fieldMinValue=0, fieldMaxValue=100,
                                             minValue=0, maxValue=100, precision=2,
                                             step=.01, value=5,
                                             columnWidth3=[40, 50, 150],
                                             columnAlign3=['left', 'both', 'left'])

    rcbx = cmds.checkBox(label='X', value=True)
    rcby = cmds.checkBox(label='Y', value=True)
    rcbz = cmds.checkBox(label='Z', value=True)
    cmds.separator(h=20, style='none')

    # Scale controls
    scale_input_field = cmds.floatSliderGrp(label='scale:', field=True, 
                                            fieldMinValue=0, fieldMaxValue=1, 
                                            minValue=0, maxValue=1, precision=2, 
                                            value=0.01, step=.01,
                                            columnWidth3=[40, 50, 150],
                                            columnAlign3=['left', 'both', 'left'])
    scbx = cmds.checkBox(label='X', value=True)
    scby = cmds.checkBox(label='Y', value=True)
    scbz = cmds.checkBox(label='Z', value=True)
    
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    # new dictionary to hold original positons..
    before_data = {}

    # Buttons 
    cmds.button(label="Randomize", width=240,
                command=functools.partial(pApplyCallback, move_input_field,
                                          mcbx, mcby, mcbz,
                                          rotate_input_field,
                                          rcbx, rcby, rcbz,
                                          scale_input_field,
                                          scbx, scby, scbz,
                                          before_data,))  
    
    cmds.button(label="Restore", width=100,
                command=functools.partial(pRestoreCallback, before_data))
    cmds.separator(h=25, style='none')
    
    cmds.showWindow()

def translater(sel, percent, chek_boxes):
    """
        Internal function that changes the transform attributes in the cahnel
        box based on user input.
    """
    for item in sel:
        #constructig the atribute names for each object that is selected
        my_trans_x = item + '.translateX'
        my_trans_y = item + '.translateY'
        my_trans_z = item + '.translateZ'        
        
        #geting what is already in the chanell box
        old_trans_x = cmds.getAttr(my_trans_x)
        old_trans_y = cmds.getAttr(my_trans_y)
        old_trans_z = cmds.getAttr(my_trans_z)
        
        #adding or subtracting a random value from original value
        new_trans_x = old_trans_x + random.uniform(-percent, percent)
        new_trans_y = old_trans_y + random.uniform(-percent, percent)
        new_trans_z = old_trans_z + random.uniform(-percent, percent)   
       
        #seting the new values to the attributes that the user has marked
        if chek_boxes[0]:
            cmds.setAttr(my_trans_x, new_trans_x)
        if chek_boxes[1]:
            cmds.setAttr(my_trans_y, new_trans_y)
        if chek_boxes[2]:
            cmds.setAttr(my_trans_z, new_trans_z)

def rotor(sel, percent, chek_boxes):
    """
        Internal function that changes the rotate attributes in the cahnel
        box based on user input.
    """
    degree = (360.0*percent)/100

    for item in sel:
        #constructig the atribute names for each object that is selected
        my_rotate_x = item + '.rotateX'
        my_rotate_y = item + '.rotateY'
        my_rotate_z = item + '.rotateZ'
       
        new_rotate_x = random.uniform(0, degree)
        new_rotate_y = random.uniform(0, degree)
        new_rotate_z = random.uniform(0, degree)

        if chek_boxes[0]:
            cmds.setAttr(my_rotate_x, new_rotate_x)
        if chek_boxes[1]:
            cmds.setAttr(my_rotate_y, new_rotate_y)
        if chek_boxes[2]:
            cmds.setAttr(my_rotate_z, new_rotate_z)

def scaler(sel, percent, chek_boxes):
    """
        Internal function that changes the scale attributes in the cahnel
        box based on user input.
    """
    for item in sel:
        #constructig the atribute names for each object that is selected
        my_scale_x = item + '.scaleX'
        my_scale_y = item + '.scaleY'
        my_scale_z = item + '.scaleZ'
        
        #geting what is already in the chanell box
        old_scale_x = cmds.getAttr(my_scale_x)
        old_scale_y = cmds.getAttr(my_scale_y)
        old_scale_z = cmds.getAttr(my_scale_z)

        new_scale_x = old_scale_x + random.uniform(-percent, percent)
        new_scale_y = old_scale_y + random.uniform(-percent, percent)
        new_scale_z = old_scale_z + random.uniform(-percent, percent)
        
        if chek_boxes[0]:
            cmds.setAttr(my_scale_x, new_scale_x)
        if chek_boxes[1]:
            cmds.setAttr(my_scale_y, new_scale_y)
        if chek_boxes[2]:
            cmds.setAttr(my_scale_z, new_scale_z)

def find_poly_obj(sel):
    """
        Finds only poly objects in a selection.
    """
    poly_obj = []
  
    for item in sel:
        shapes = cmds.listRelatives(item, shapes=True)
    
        if cmds.nodeType(shapes[0]) == 'mesh':
            poly_obj.append(item)

    return poly_obj

def get_original_pos(polys, before_data):
    """
        Gets original positions poly objects in a selection.
    """
    for item in polys:
        if item not in before_data:
            pos = cmds.getAttr(item +'.translate')[0]
            rot = cmds.getAttr(item +'.rotate')[0]
            scl = cmds.getAttr(item +'.scale')[0]

            current_dict = {
                'pos': pos,
                'rot': rot,
                'scl': scl
                }
            before_data[item] = current_dict

    return before_data

def restore_to_original_position(sel, poly_data):
    """
        restores to orginal chanell box values.
    """
    for item in sel:
        if item in poly_data:
            pos = poly_data[item]['pos']
            cmds.setAttr(item + '.translate', pos[0], pos[1], pos[2])
            rot = poly_data[item]['rot']
            cmds.setAttr(item + '.rotate', rot[0], rot[1], rot[2])
            scl = poly_data[item]['scl']
            cmds.setAttr(item + '.scale', scl[0], scl[1], scl[2])
        else:
            print item +' skiping restore..'

def apply_callback(pMoveInputField, pmcbx, pmcby, pmcbz, pRotateInputField,
                   prcbx, prcby, prcbz, pScaleInputField, pscbx, pscby, pscbz,
                   pBeforeData, *pArgs):
    """
        applyCallback.
    """  
    input_translate = cmds.floatSliderGrp(pMoveInputField, query=True, value=True)
    
    inputMcbx = cmds.checkBox(pmcbx, query=True, value=True)
    inputMcby = cmds.checkBox(pmcby, query=True, value=True)
    inputMcbz = cmds.checkBox(pmcbz, query=True, value=True)
    
    input_translate_checkbox = [inputMcbx, inputMcby, inputMcbz]

    input_rotate = cmds.floatSliderGrp(pRotateInputField, query=True, value=True)
    
    inputRcbx = cmds.checkBox(prcbx, query=True, value=True)
    inputRcby = cmds.checkBox(prcby, query=True, value=True)
    inputRcbz = cmds.checkBox(prcbz, query=True, value=True)
    
    input_rotate_checkbox = [inputRcbx, inputRcby, inputRcbz]
   
    input_scale = cmds.floatSliderGrp(pScaleInputField, query=True, value=True) 
    
    inputScbx = cmds.checkBox(pscbx, query=True, value=True)
    inputScby = cmds.checkBox(pscby, query=True, value=True)
    inputScbz = cmds.checkBox(pscbz, query=True, value=True)
    
    input_scale_checkbox = [inputScbx, inputScby, inputScbz]

    selection = cmds.ls(selection=True)
    sel = find_poly_obj(selection)

    #chek to see if anything is selected
    if not sel:
        cmds.warning('No polygonal objects selected!')

    # geting originals before we randomize it
    get_original_pos(sel, pBeforeData)

    translater(sel, input_translate, input_translate_checkbox)
    rotor(sel, input_rotate, input_rotate_checkbox)
    scaler(sel, input_scale, input_scale_checkbox)


def restore_callback(pBeforeData, *pArgs):
    """
        restoreCallback
    """
    # get the selection
    selection = cmds.ls(selection=True)

    # filter to just poly objects
    sel = find_poly_obj(selection)

    # restoring those we have moved
    restore_to_original_position(sel, pBeforeData)

create_ui('Rand All The Things!!! 1.0', apply_callback, restore_callback)
