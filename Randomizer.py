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
from itertools import izip

# IMPORT LOCAL MODULES
import maya.cmds as cmds

def create_ui(p_window_title, p_apply_callback, p_restore_callback):
    """
        creating UI.
    """
    # each window has a unique identifier so only one would be opened at a time
    window_id = 'Mywindow_id' 
    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)

    cmds.window(window_id, title=p_window_title, sizeable=True, resizeToFitChildren=True)

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
                command=functools.partial(p_apply_callback, move_input_field,
                                          mcbx, mcby, mcbz,
                                          rotate_input_field,
                                          rcbx, rcby, rcbz,
                                          scale_input_field,
                                          scbx, scby, scbz,
                                          before_data,))  
    
    cmds.button(label="Restore", width=100,
                command=functools.partial(p_restore_callback, before_data))
    cmds.separator(h=25, style='none')
    
    cmds.showWindow()

def translater(sel, percent, chek_boxes, before_data):
    """
        Internal function that changes the transform attributes in the cahnel
        box based on user input.
    """
    axies = ['X', 'Y', 'Z']
    for item in sel:
        new_translate_values = []
        
        for old_translate_value in before_data[item]['pos']:
            new_translate_values.append(old_translate_value + random.uniform(-percent, percent))

         #if the user has cheked the box, we change to the new value
        for box, new_value, xyz in izip(chek_boxes, new_translate_values, axies):
            if box: 
                cmds.setAttr(item + '.translate'+ xyz, new_value)

def rotor(sel, percent, chek_boxes):
    """
        Internal function that changes the rotate attributes in the chnel
        box based on user input.
    """
    degree = (360.0*percent)/100
    axies = ['X', 'Y', 'Z']
    for item in sel:
        new_rotate_values = []

        for xyz in axies:
            new_rotate_values.append(random.uniform(0, degree))
        
        #if the user has cheked the box change to new value
        for box, new_value, xyz in izip(chek_boxes, new_rotate_values, axies):
            if box: 
                cmds.setAttr(item + '.rotate'+ xyz, new_value)
       
def scaler(sel, percent, chek_boxes, before_data):
    """
        Internal function that changes the scale attributes in the cahnel
        box based on user input.
    """
    axies = ['X', 'Y', 'Z']
    for item in sel: 
        new_scale_values = []

        for old_scale_value in before_data[item]['scl']:
            new_scale_values.append(old_scale_value + random.uniform(-percent, percent))

        #if the user has cheked the box change to new value
        for box, new_value, xyz in izip(chek_boxes, new_scale_values, axies):
            if box: 
                cmds.setAttr(item + '.scale'+ xyz, new_value)
            
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

def apply_callback(p_move_input_field, pmcbx, pmcby, pmcbz, p_rotate_input_field,
                   prcbx, prcby, prcbz, p_scale_input_field, pscbx, pscby, pscbz,
                   p_before_data, *pArgs):
    """
        applyCallback.
    """  
    input_translate = cmds.floatSliderGrp(p_move_input_field, query=True, value=True)
    
    input_mcbx = cmds.checkBox(pmcbx, query=True, value=True)
    input_mcby = cmds.checkBox(pmcby, query=True, value=True)
    input_mcbz = cmds.checkBox(pmcbz, query=True, value=True)
    
    input_translate_checkbox = [input_mcbx, input_mcby, input_mcbz]

    input_rotate = cmds.floatSliderGrp(p_rotate_input_field, query=True, value=True)
    
    input_rcbx = cmds.checkBox(prcbx, query=True, value=True)
    input_rcby = cmds.checkBox(prcby, query=True, value=True)
    input_rcbz = cmds.checkBox(prcbz, query=True, value=True)
    
    input_rotate_checkbox = [input_rcbx, input_rcby, input_rcbz]
   
    input_scale = cmds.floatSliderGrp(p_scale_input_field, query=True, value=True) 
    
    input_scbx = cmds.checkBox(pscbx, query=True, value=True)
    input_scby = cmds.checkBox(pscby, query=True, value=True)
    input_scbz = cmds.checkBox(pscbz, query=True, value=True)
    
    input_scale_checkbox = [input_scbx, input_scby, input_scbz]

    selection = cmds.ls(selection=True)
    sel = find_poly_obj(selection)

    #chek to see if anything is selected
    if not sel:
        cmds.warning('No polygonal objects selected!')

    # geting originals before we randomize it
    get_original_pos(sel, p_before_data)

    translater(sel, input_translate, input_translate_checkbox, p_before_data)
    rotor(sel, input_rotate, input_rotate_checkbox)
    scaler(sel, input_scale, input_scale_checkbox, p_before_data)

def restore_callback(p_before_data, *pArgs):
    """
        restoreCallback
    """
    # get the selection
    selection = cmds.ls(selection=True)

    # filter to just poly objects
    sel = find_poly_obj(selection)

    # restoring those we have moved
    restore_to_original_position(sel, p_before_data)

create_ui('Rand All The Things!!! 1.0', apply_callback, restore_callback)
