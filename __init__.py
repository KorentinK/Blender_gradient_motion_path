bl_info = {
	"name" : "Gradient motion path",
	"author" : "Corentin",
	"description" : "",
	"blender" : (3, 2, 0),
	"location" : "",
	"warning" : "",
	"category" : "Animation",
}
	
    
    
import bpy

from . ui_panel import *

from . draw_op import OT_draw_operator

addon_keymaps = []


def register(): # That was inspired from a script of Jayanam, here is a keyboard shortcut "ctrl maj F" that you can also use for display the motion path ;)
    bpy.utils.register_class(OT_draw_operator)
    bpy.utils.register_class(MotionPathPanel)
    
    frame_num = bpy
    kcfg = bpy.context.window_manager.keyconfigs.addon
    if kcfg:
        km = kcfg.keymaps.new(name='3D View', space_type='VIEW_3D')
        
        kmi = km.keymap_items.new("object.draw_op", 'F', 'PRESS', shift= True, ctrl=True)
        
        addon_keymaps.append((km, kmi))
        
    

        
def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(OT_draw_operator)
    bpy.utils.unregister_class(MotionPathPanel)
    
    



    
if __name__ == "__main__":
    register()