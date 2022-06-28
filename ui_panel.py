import bpy

from . draw_op import *

class MotionPathPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Gradient motion path" #Motion path
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        avs = bpy.context.object.animation_visualization
        mps = avs.motion_path     
        

        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Motion path frames range:")

        row = layout.row(align=True)
        col = layout.column(align=True)
        

        row.prop(mps, "frame_start", text="Frame Start")
        row.prop(mps, "frame_end", text="Frame End")
        
        
        
        
        # Create two columns, by using a split layout.
        split = layout.split()


        # Different sizes in a row
        #layout.label(text="Create motion path:")
        row = layout.row(align=True)
        layout.operator(OT_draw_operator.bl_idname, text='Create motion path')
        
            

def register():
    bpy.utils.register_class(MotionPathPanel)
    bpy.utils.register_class(OT_draw_operator)


def unregister():
    bpy.utils.unregister_class(MotionPathPanel)
    bpy.utils.unregister_class(OT_draw_operator)


if __name__ == "__main__":
    register()
