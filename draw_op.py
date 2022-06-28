import bpy

import bgl

import gpu

from gpu_extras.batch import batch_for_shader

from bpy.types import Operator

from . ui_panel import * 

from math import *



class OT_draw_operator(Operator):
    bl_idname = "object.draw_op"
    bl_label = "Draw operator"
    bl_description = "Operator for drawing"
    bl_options = {'REGISTER'}

    
    
    
    
    def __init__(self):
        self.draw_handle = None
        self.draw_event = None
        
        self.widgets = []
        
    def invoke(self, context, event):
    
        self.create_batch()
        
        args = (self, context)
        self.register_handlers(args, context)
        
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
              
        
    def register_handlers(self, args, context): 
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, args, "WINDOW", "POST_VIEW") 
            
        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)
        
    def unregister_handlers(self, context):
    
        context.window_manager.event_timer_remove(self.draw_event)
        
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")
        
        self.draw_handle = None
        self.draw_event = None
        
    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()
            
        if event.type in {"ESC"}:
            self.unregister_handlers(context)
            return {'CANCELLED'}
            
        return {"PASS_THROUGH"}
        

    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}
        
          
      
    def create_batch(self):
        
        
            avs = bpy.context.object.animation_visualization
            mps = avs.motion_path
        
            liste = []
            vertices = []
            speedinfo_brt = []
            speedinfo = []
            col = []
            col2 = []
            k = 0
            l = 3
            jiter = 0
            start_frame = mps.frame_start 
            framesetnum = start_frame 
            end_frame = mps.frame_end + 1
            segments = (end_frame - start_frame) - 1
            extremities = segments * 2
            frame_reset = bpy.context.scene.frame_current
            # pour une version qui marche avec une armature : bpy.data.objects[armature].location + context.active_pose_bone.tail
            
            for i in range(end_frame - start_frame):
                bpy.context.scene.frame_set(framesetnum) #creation de liste[] et de speedinfo_brute[]
                current_mode = bpy.context.object.mode
                
                if current_mode == 'POSE' : 
                    posb = bpy.context.active_pose_bone
                    objt = bpy.context.active_object 
                    globalboneloc = objt.matrix_world @ posb.matrix
                    liste.extend(((globalboneloc[0][3]), (globalboneloc[1][3]), (globalboneloc[2][3])))
                else : 
                    liste.extend((bpy.context.active_object.matrix_world.translation))  #bpy.context.active_object.location
                
                bpy.context.scene.frame_set(framesetnum+1)
                framesetnum = framesetnum + 1
                
                if current_mode == 'POSE' :
                    posb = bpy.context.active_pose_bone
                    objt = bpy.context.active_object 
                    globalboneloc = objt.matrix_world @ posb.matrix
                    #liste.extend(((globalboneloc[0][3]), (globalboneloc[1][3]), (globalboneloc[2][3])))
                    xs = (globalboneloc[0][3]) - liste[0+3*i]
                    ys = (globalboneloc[1][3]) - liste[1+3*i]
                    zs = (globalboneloc[2][3]) - liste[2+3*i]
                    dist = sqrt(xs*xs + ys*ys + zs*zs)
                    speedinfo_brt.append(dist)
                else :
                    xs = bpy.context.active_object.matrix_world.translation.x - liste[0+3*i] #bpy.context.active_object.location.x
                    ys = bpy.context.active_object.matrix_world.translation.y - liste[1+3*i]
                    zs = bpy.context.active_object.matrix_world.translation.z - liste[2+3*i]
                    dist = sqrt(xs*xs + ys*ys + zs*zs)
                    speedinfo_brt.append(dist)
     
            
            
            maxspeed = max(speedinfo_brt)
            if max(speedinfo_brt) == 0 :
                maxspeed = 0.000001
                                                  
                                        
            for j in range(segments):
            
                remapspd = speedinfo_brt[j] * (1 / maxspeed)
                speedinfo.append(remapspd)
            
                vertices.append(liste[k:l])
                jiter = jiter + 1
                k = 0 + 3*jiter
                l = 3 + 3*jiter
                vertices.append(liste[k:l])
                                              
            self.shader = gpu.shader.from_builtin('3D_SMOOTH_COLOR')
            
            for m in range(segments):

                    
                xc = speedinfo[m]
                rc = sin((xc-0.5)*pi)
                if rc < 0 :
                    rc = 0
                vc = sin(xc*pi)
                if vc < 0 :
                    vc = 0
                bc = cos(xc*pi)
                if bc < 0 :
                    bc = 0
                
                col.append((rc,vc,bc,1))#Color for the lines (note that there is two assignment, because the list of the vertex requires it)                 
                col.append((rc,vc,bc,1))
                col2.append((1,1,1,1))#Optionnal color for the points
                col2.append((1,1,1,1))
            
            self.batch1 = batch_for_shader(self.shader, 'POINTS', {"pos": vertices, "color": col})
            self.batch2 = batch_for_shader(self.shader, 'LINES', {"pos": vertices, "color": col})
            bpy.context.scene.frame_set(frame_reset)
            
     

    #Draw handler to paint onto the screen
    def draw_callback_px(self, op, context):
    
         #Draw Lines 
            bgl.glPointSize(3)
            bgl.glLineWidth(1)
            self.shader.bind()
            self.batch1.draw(self.shader)
            self.batch2.draw(self.shader)

            
            
    
