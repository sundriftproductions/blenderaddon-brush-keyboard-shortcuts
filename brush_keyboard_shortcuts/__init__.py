#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

import bpy

# Version History
# 1.0.1 - 2020-07-03: Made it so if you don't have Add or Subtract selected (say, Mix) it'll try to set the brush to Add.
# 1.0.2 - 2020-11-11: This now affects texture painting brushes, not just weight painting brushes. Changed the name of this from "Toggle Weight Painting Brush Blend" to "Toggle Add Subtract Brush Blend" since it's no longer exclusively for weight painting.
# 1.0.3 - 2020-12-16: Sends back an INFO message when launched. I needed to see some user feedback to make sure this was actually being launched.
# 1.0.4 - 2020-12-17: Figured out how to switch ONLY the current brush, rather than all brushes.
# 1.0.5 - 2020-12-24: Changed the name of this from "Toggle Add Subtract Brush Blend" to "Brush Keyboard Shortcuts".
# 1.0.6 - 2020-12-30: Only change blend mode if the selected brush is the Draw tool (or also the Fill tool for texture painting).
# 1.0.7 - 2021-01-05: Added WM_OT_brush_keyboard_shortcuts_iterate_value_brush_strength
# 1.0.8 - 2021-01-14: For value painting, made it so .125 is one of the options. Also made it so that it looks at your current value and then picks the "next" one to go up. (e.g. if you're on 0.3, it'll know to pick .5 next.)
# 1.0.9 - 2021-06-27: Added support for sculpt brushes. Added the ability to change the radius of brushes as well.
# 1.0.10 - 2022-08-07: Misc formatting cleanup before uploading to GitHub.

bl_info = {
    "name": "Brush Keyboard Shortcuts",
    "author": "Jeff Boller",
    "version": (1, 0, 10),
    "blender": (2, 93, 0),
    "location": "",
    "description": "This add-on creates various labor-saving keyboard shortcuts for brushes. "\
                   "To run this, make a keyboard shortcut and put in one of the following commands: " \
                   "wm.brush_keyboard_shortcuts_add_subtract_brush_blend (for Texture Paint or Weight Paint mode) " \
                   "wm.brush_keyboard_shortcuts_toggle_brush_strength (for Particle Edit, Texture Paint, or Weight Paint mode) " \
                   "wm.brush_keyboard_shortcuts_iterate_value_brush_strength (for Weight Paint mode) " \
                   "If you want to call this manually from Python, use one of the following commands: " \
                   "bpy.ops.wm.brush_keyboard_shortcuts_add_subtract_brush_blend() " \
                   "bpy.ops.wm.brush_keyboard_shortcuts_toggle_brush_strength()" \
                   "bpy.ops.wm.brush_keyboard_shortcuts_iterate_value_brush_strength().",
    "wiki_url": "https://github.com/sundriftproductions/blenderaddon-brush-keyboard-shortcuts/wiki",
    "tracker_url": "https://github.com/sundriftproductions/blenderaddon-brush-keyboard-shortcuts",
    "category": "System"}

def refresh_tool_header(): # Necessary for seeing the new value(s) in the tool header; otherwise, you have to hover with the mouse to see the update.
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'TOOL_HEADER':
                    region.tag_redraw()

class WM_OT_brush_keyboard_shortcuts_toggle_add_subtract_brush_blend(bpy.types.Operator):
    bl_idname = 'wm.brush_keyboard_shortcuts_add_subtract_brush_blend'
    bl_label = 'Toggle between add/subtract brush blend'
    bl_description = 'Call bpy.ops.wm.brush_keyboard_shortcuts_add_subtract_brush_blend()'
    bl_options = {'UNDO'}

    def execute(self, context):
        if bpy.context.active_object.mode == 'WEIGHT_PAINT':
            brush = bpy.context.tool_settings.weight_paint.brush
            if brush.weight_tool != 'DRAW':
                return {'FINISHED'}
            if bpy.context.tool_settings.weight_paint.brush.blend == 'ADD':
                bpy.context.tool_settings.weight_paint.brush.blend = 'SUB'
                self.report({'INFO'}, "Switched brush blend to 'Subtract'")
            elif bpy.context.tool_settings.weight_paint.brush.blend == 'SUB':
                bpy.context.tool_settings.weight_paint.brush.blend = 'ADD'
                self.report({'INFO'}, "Switched brush blend to 'Add'")
            else:
                try:
                    bpy.context.tool_settings.weight_paint.brush.blend = 'ADD'
                    self.report({'INFO'}, "Switched brush blend to 'Add'")
                except:
                    placeholder = 0 # Oh well, we tried to change the brush.
        elif bpy.context.active_object.mode == 'TEXTURE_PAINT':
            brush = bpy.context.tool_settings.image_paint.brush
            if brush.image_tool not in ('DRAW', 'FILL'):
                return {'FINISHED'}
            if bpy.context.tool_settings.image_paint.brush.blend == 'ADD':
                bpy.context.tool_settings.image_paint.brush.blend = 'SUB'
                self.report({'INFO'}, "Switched brush blend to 'Subtract'")
            elif bpy.context.tool_settings.image_paint.brush.blend == 'SUB':
                bpy.context.tool_settings.image_paint.brush.blend = 'ADD'
                self.report({'INFO'}, "Switched brush blend to 'Add'")
            else:
                try:
                    bpy.context.tool_settings.image_paint.brush.blend = 'ADD'
                    self.report({'INFO'}, "Switched brush blend to 'Add'")
                except:
                    placeholder = 0 # Oh well, we tried to change the brush.

        return {'FINISHED'}

class WM_OT_brush_keyboard_shortcuts_toggle_brush_strength(bpy.types.Operator):
    bl_idname = 'wm.brush_keyboard_shortcuts_toggle_brush_strength'
    bl_label = 'Toggle between 0.5 and 1.0 for brush strength'
    bl_description = 'Call bpy.ops.wm.brush_keyboard_shortcuts_toggle_brush_strength()'
    bl_options = {'UNDO'}

    def execute(self, context):
        if bpy.context.active_object.mode == 'PARTICLE_EDIT':
            if bpy.context.scene.tool_settings.particle_edit.brush.strength == 1:
                bpy.context.scene.tool_settings.particle_edit.brush.strength = 0.5
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 0.5")
            else:
                bpy.context.scene.tool_settings.particle_edit.brush.strength = 1
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 1")
        elif bpy.context.active_object.mode == 'WEIGHT_PAINT':
            if bpy.context.scene.tool_settings.weight_paint.brush.strength == 1:
                bpy.context.scene.tool_settings.weight_paint.brush.strength = 0.5
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 0.5")
            else:
                bpy.context.scene.tool_settings.weight_paint.brush.strength = 1
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 1")
        elif bpy.context.active_object.mode == 'TEXTURE_PAINT':
            if bpy.context.scene.tool_settings.image_paint.brush.strength == 1:
                bpy.context.scene.tool_settings.image_paint.brush.strength = 0.5
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 0.5")
            else:
                bpy.context.scene.tool_settings.image_paint.brush.strength = 1
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 1")
        elif bpy.context.active_object.mode == 'SCULPT':
            if bpy.context.scene.tool_settings.sculpt.brush.strength == 1:
                bpy.context.scene.tool_settings.sculpt.brush.strength = 0.5
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 0.5")
            else:
                bpy.context.scene.tool_settings.sculpt.brush.strength = 1
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 1")

        return {'FINISHED'}

class WM_OT_brush_keyboard_shortcuts_iterate_value_brush_strength(bpy.types.Operator):
    bl_idname = 'wm.brush_keyboard_shortcuts_iterate_value_brush_strength'
    bl_label = 'Set brush to Value and iterate through strengths'
    bl_description = 'Call bpy.ops.wm.brush_keyboard_shortcuts_iterate_value_brush_strength()'
    bl_options = {'UNDO'}

    def execute(self, context):
        if bpy.context.active_object.mode == 'WEIGHT_PAINT':
            brush = bpy.context.tool_settings.weight_paint.brush
            if brush.weight_tool != 'DRAW':
                return {'FINISHED'}
            msg = "Switched "
            if (bpy.context.tool_settings.weight_paint.brush.blend != 'LUMINOSITY'):
                bpy.context.tool_settings.weight_paint.brush.blend = 'LUMINOSITY'
                msg = "brush blend='Value', "

            if bpy.context.scene.tool_settings.weight_paint.brush.strength != 1:
                bpy.context.scene.tool_settings.weight_paint.brush.strength = 1
                msg = msg + "strength=1, "

            if bpy.context.scene.tool_settings.unified_paint_settings.weight < 0.125:
                bpy.context.scene.tool_settings.unified_paint_settings.weight = 0.125
            elif bpy.context.scene.tool_settings.unified_paint_settings.weight < 0.25:
                bpy.context.scene.tool_settings.unified_paint_settings.weight = 0.25
            elif bpy.context.scene.tool_settings.unified_paint_settings.weight < 0.5:
                bpy.context.scene.tool_settings.unified_paint_settings.weight = 0.5
            elif bpy.context.scene.tool_settings.unified_paint_settings.weight < 0.75:
                bpy.context.scene.tool_settings.unified_paint_settings.weight = 0.75
            elif bpy.context.scene.tool_settings.unified_paint_settings.weight < 1:
                bpy.context.scene.tool_settings.unified_paint_settings.weight = 1
            elif bpy.context.scene.tool_settings.unified_paint_settings.weight == 1:
                bpy.context.scene.tool_settings.unified_paint_settings.weight = 0

            refresh_tool_header()
            msg = msg + "weight=" + str(bpy.context.scene.tool_settings.unified_paint_settings.weight)
            self.report({'INFO'}, msg)
        return {'FINISHED'}

class WM_OT_brush_keyboard_shortcuts_iterate_radius(bpy.types.Operator):
    bl_idname = 'wm.brush_keyboard_shortcuts_iterate_radius'
    bl_label = 'Iterate through radiuses'
    bl_description = 'Call bpy.ops.wm.brush_keyboard_shortcuts_iterate_radius()'
    bl_options = {'UNDO'}

    def execute(self, context):
        if bpy.context.active_object.mode == 'PARTICLE_EDIT' or \
                bpy.context.active_object.mode == 'WEIGHT_PAINT' or \
                bpy.context.active_object.mode == 'TEXTURE_PAINT' or \
                bpy.context.active_object.mode == 'SCULPT':
            if bpy.context.scene.tool_settings.unified_paint_settings.size < 10:
                bpy.context.scene.tool_settings.unified_paint_settings.size = 10
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 10")
            elif bpy.context.scene.tool_settings.unified_paint_settings.size < 50:
                bpy.context.scene.tool_settings.unified_paint_settings.size = 50
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 50")
            elif bpy.context.scene.tool_settings.unified_paint_settings.size < 100:
                bpy.context.scene.tool_settings.unified_paint_settings.size = 100
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 100")
            elif bpy.context.scene.tool_settings.unified_paint_settings.size < 150:
                bpy.context.scene.tool_settings.unified_paint_settings.size = 150
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 150")
            elif bpy.context.scene.tool_settings.unified_paint_settings.size < 200:
                bpy.context.scene.tool_settings.unified_paint_settings.size = 200
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 200")
            elif bpy.context.scene.tool_settings.unified_paint_settings.size < 300:
                bpy.context.scene.tool_settings.unified_paint_settings.size = 300
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 300")
            elif bpy.context.scene.tool_settings.unified_paint_settings.size < 400:
                bpy.context.scene.tool_settings.unified_paint_settings.size = 400
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 400")
            elif bpy.context.scene.tool_settings.unified_paint_settings.size < 500:
                bpy.context.scene.tool_settings.unified_paint_settings.size = 500
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 500")
            else:
                bpy.context.scene.tool_settings.unified_paint_settings.size = 1
                refresh_tool_header()
                self.report({'INFO'}, "Switched brush strength to 1")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(WM_OT_brush_keyboard_shortcuts_toggle_add_subtract_brush_blend)
    bpy.utils.register_class(WM_OT_brush_keyboard_shortcuts_toggle_brush_strength)
    bpy.utils.register_class(WM_OT_brush_keyboard_shortcuts_iterate_value_brush_strength)
    bpy.utils.register_class(WM_OT_brush_keyboard_shortcuts_iterate_radius)

def unregister():
    bpy.utils.unregister_class(WM_OT_brush_keyboard_shortcuts_iterate_radius)
    bpy.utils.unregister_class(WM_OT_brush_keyboard_shortcuts_toggle_add_subtract_brush_blend)
    bpy.utils.unregister_class(WM_OT_brush_keyboard_shortcuts_toggle_brush_strength)
    bpy.utils.unregister_class(WM_OT_brush_keyboard_shortcuts_iterate_value_brush_strength)

if __name__ == "__main__":
    register()
