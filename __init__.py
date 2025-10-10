bl_info = {
    "name": "G Render Hub",
    "author": "Azucena Castillo",
    "version": (1, 0),
    "blender": (4, 2, 3),
    "description": "Placing and managing Gatorade products",
    "location": "View3D > Sidebar > G Render Hub",
}


# Do not edit without permisson.
# Contact koalina.draws@gmail.com

import bpy
import bmesh
import os

# ___________________________________________________________
# FUNCTIONS

def update_active_menu(self, context):
    # Refresca el panel cuando cambie el menú activo
    if context.area:
        context.area.tag_redraw()
    print("Active menu changed:", self.active_menu)

def update_flavor_color(self, context):
    nd_color_map = {
        'op1': "Flavor_001_Material",
        'op2': "Flavor_002_Material",
        'op3': "Flavor_003_Material",
        'op4': "Flavor_004_Material",
        'op5': "Flavor_005_Material",
        'op6': "Flavor_006_Material",
        'op7': "Flavor_007_Material",
        'op8': "Flavor_008_Material",
    }
    
    material_name = nd_color_map.get(self.my_selects)
    if not material_name:
        return

    mat = bpy.data.materials.get(material_name)
    if not mat or not mat.use_nodes:
        return

    rgb_node = mat.node_tree.nodes.get("RGB")
    if rgb_node:
        rgb_node.outputs[0].default_value = list(self.color)
        
    

def update_label_material(self, context):
    obj = context.object
    nd_grp = bpy.data.node_groups["Geometry Nodes"]
    materials = bpy.data.materials
    
    if obj is None or obj.type != 'MESH':
        return
    
     # Evitar actualizar si no hay selección válida
    if self.my_selects == "default" or self.my_size == "default":
        return
    
    nd_label_map = {
        'op1': "label1",
        'op2': "label2",
        'op3': "label3"
    }
    
    label_map = {
        'label1': "G_Label_GTQ_Material" ,
        'label2': "G_Label_G_Zero_Material" ,
        'label3': "G_Label_LowerSugar_Material" 
        }
            
    node_name = nd_label_map.get(self.my_selects) 
    
    nd_grp.nodes[node_name].inputs[2].default_value = bpy.data.materials[ label_map.get(self.my_brands)]


def update_size_node(self, context):
    obj = context.object
    nd_grp = bpy.data.node_groups["Geometry Nodes"]
    
    if obj is None or obj.type != 'MESH':
        return


    if self.my_selects == "default" or self.my_size == "default":
        return

    node_map = {
        'op1': "SWITCH 001",  
        'op2': "SWITCH 002",  
        'op3': "SWITCH 003",
        'op4': "SWITCH 004",
        'op5': "SWITCH 005",
        'op6': "SWITCH 006",
        'op7': "SWITCH 007",
        'op8': "SWITCH 008"  
    }
    
    size_map = {
        'size1': "12oz" ,
        'size2': "20oz" ,
        'size3': "28oz"
        }
    
    node_name = node_map.get(self.my_selects)             

    nd_grp.nodes[node_name].inputs[0].default_value = size_map.get(self.my_size) 
    

def update_selection(self, context):
    """Selecciona vértices según my_selects"""
    obj = context.object
    if obj is None or obj.type != 'MESH':
        return
    if context.mode != 'EDIT_MESH':
        return

    group_map = {
        'op1': "Selection_001",
        'op2': "Selection_002",
        'op3': "Selection_003",
        'op4': "Selection_004",
        'op5': "Selection_005",
        'op6': "Selection_006",
        'op7': "Selection_007",
        'op8': "Selection_008"
    }

    group_name = group_map.get(self.my_selects)
    if group_name not in obj.vertex_groups:
        return

    # Set active vertex group
    obj.vertex_groups.active = obj.vertex_groups[group_name]

    bm = bmesh.from_edit_mesh(obj.data)

    # Deselect all vertices
    for v in bm.verts:
        v.select = False

    vg_index = obj.vertex_groups[group_name].index

    # Select vertices assigned to the group
    for v in bm.verts:
        for g in v.groups:
            if g.group == vg_index:
                v.select = True
                break

    bmesh.update_edit_mesh(obj.data)


def show_vertex(context):
    obj = context.object
    if obj is None or obj.type != 'MESH':
        return

    if obj.vertex_groups.active is None:
        return

    if context.mode != 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.object.vertex_group_select()


# ─────────────────────────────────────────────
# PROPERTY GROUP


# Dictionary to add selections
class GSHADER_PG_SETTINGS(bpy.types.PropertyGroup):
    my_selects: bpy.props.EnumProperty(
        name="Selections",
        items=[
            ('default', "None", ""),
            ('op1', "001", ""),
            ('op2', "002", ""),
            ('op3', "003", ""),
            ('op4', "004", ""),
            ('op5', "005", ""),
            ('op6', "006", ""),
            ('op7', "007", ""),
            ('op8', "008", ""),
        ],
        update=update_selection
    )

    my_brands: bpy.props.EnumProperty(
        name="Sub Brands",
        description="Select sub-brands. Ex: Gatorlyte, GTQ , G Zero, etc...",
        items=[
            ('default', "None", ""),
            ('label1', "GTQ", ""),
            ('label2', "G Zero", ""),
            ('label3', "G Lower Sugar", ""),
        ],
        update=update_label_material
    )

    my_size: bpy.props.EnumProperty(
        name="Size",
        description="Select bottle size. Ex. 28oz, 20 oz, 24oz...",
        items=[
            ('default_size', "None", ""),
            ('size1', "12oz", ""),
            ('size2', "24oz", ""),
            ('size3', "28oz", ""),
        ],
        update=update_size_node
    )

    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 0.5, 0.0, 1.0),
        description="Pick a color",
        update=update_flavor_color
    )
    
    subdivisions: bpy.props.IntProperty(
        name="subdivisions",
        default=10,
        min=1,
        max=100
    )
    
    active_menu: bpy.props.EnumProperty(
        name="active panel",
        description="Choose to work with products or props",
        items=[
            ('Products', "Products", "Products"),
            ('Props', "Props", "Props"),
        ],
        update=update_active_menu
    )

# ─────────────────────────────────────────────
# OPERATORS

class GSHADER_OT_button_add(bpy.types.Operator):
    bl_idname = "gshader.button_add"
    bl_label = "ADD"

    def execute(self, context):
        obj = context.object

        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}

        if context.mode != 'EDIT_MESH':
            self.report({'ERROR'}, "Must be in Edit Mode")
            return {'CANCELLED'}

        if not obj.vertex_groups.active:
            self.report({'ERROR'}, "No active vertex group")
            return {'CANCELLED'}

        bpy.ops.object.vertex_group_assign()
        self.report({'INFO'}, "Vertex assigned to active group")
        return {'FINISHED'}


class GSHADER_OT_button_remove(bpy.types.Operator):
    bl_idname = "gshader.button_remove"
    bl_label = "REMOVE"

    def execute(self, context):
        bpy.ops.object.vertex_group_remove_from()
        self.report({'INFO'}, "Vertex removed from active group")
        return {'FINISHED'}


class GSHADER_OT_button_show(bpy.types.Operator):
    bl_idname = "gshader.button_select"
    bl_label = "SHOW"

    def execute(self, context):
        show_vertex(context)
        self.report({'INFO'}, "Vertex selected")
        return {'FINISHED'}
    
class GSHADER_OT_button_remove_all(bpy.types.Operator):
    bl_idname = "gshader.button_remove_all"
    bl_label = "REMOVE ALL"
    
    def execute(self, context):
        bpy.ops.object.vertex_group_remove_from(use_all_groups=True)
        self.report({'INFO'}, "Vertex removed from all selections")
        return {'FINISHED'}


class GSHADER_OT_button_append(bpy.types.Operator):
    bl_idname = "gshader.button_append"
    bl_label = "Append to Collection"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    target_collection_name: bpy.props.StringProperty(default="Props")

    def execute(self, context):
        if not self.filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}

        # Crear la collection destino si no existe
        if self.target_collection_name in bpy.data.collections:
            target_col = bpy.data.collections[self.target_collection_name]
        else:
            target_col = bpy.data.collections.new(self.target_collection_name)
            context.scene.collection.children.link(target_col)

        # Cargar lista de objetos del blend
        with bpy.data.libraries.load(self.filepath, link=False) as (data_from, data_to):
            for obj_name in data_from.objects:
                data_to.objects = [obj_name]

                # Apendea el objeto
                for obj in data_to.objects:
                    if obj:
                        # Vincular a collection destino
                        target_col.objects.link(obj)
                        # Desvincular de la collection principal
                        if obj.name in context.scene.collection.objects:
                            context.scene.collection.objects.unlink(obj)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class GSHADER_OT_opt_render(bpy.types.Operator):
    bl_idname = "gshader.optimize_render"
    bl_label = "Optimize Render"

    def execute(self, context):
        sce = context.scene
        render = sce.render
        cycles = sce.cycles
        
        #Samples
        render.engine = 'CYCLES'
        cycles.device = 'GPU'
        cycles.adaptive_threshold = 0.01
        cycles.samples = 250
        cycles.use_denoising = True
        #Light Paths
        cycles.max_bounces = 8
        cycles.volume_bounces = 0
        #Optimization
        render.film_transparent = True
        cycles.use_auto_tile = True
        cycles.tile_size = 256
        render.use_persistent_data = True
        #Color Management
        sce.view_settings.view_transform = 'Filmic'
        sce.view_settings.look = 'Medium High Contrast'
        self.report({'INFO'}, "Render settings optimized")
        return {'FINISHED'}
               
class GSHADER_OT_opt_new_grid(bpy.types.Operator):
    bl_idname = "gshader.new_grid"
    bl_label = "New Grid"
    
    def execute(self, context):
        # Accedemos al valor desde las propiedades del panel
        props = context.scene.gshader_props
        subdivisions = props.subdivisions
        
        # Creamos el grid con las subdivisiones elegidas
        bpy.ops.mesh.primitive_grid_add(
            x_subdivisions=subdivisions - 1,
            y_subdivisions=subdivisions - 1,
            enter_editmode=True,
            align='WORLD',
            location=(0, 0, 0),
            scale=(1, 1, 1)
        )
        
        self.report({'INFO'}, "Grid created")
        return {'FINISHED'}


# ─────────────────────────────────────────────
# UI PANEL

class GATORADE_PT_SHADER(bpy.types.Panel):
    bl_label = "G Render Hub"
    bl_idname = "PT_SHADER"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'G Render Hub'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.gshader_props
        layout_ctrl = bpy.data.objects['Turn Around Master']
        camera_zoom = bpy.data.objects['Camera'].constraints["Follow Path"]  
        
        row = layout.row()
        row.prop(props, "active_menu", expand= True)
        
        row = layout.row()
        row.operator("gshader.new_grid", icon='MESH_GRID')
        row.prop(props, "subdivisions", text='Size')
        
        layout.label(text="Selection")
        layout.prop(props, "my_selects", text="")        
        
        layout.label(text="Vertex")
        row = layout.row()
        row.operator("gshader.button_add", icon='PLUS')
        row.operator("gshader.button_remove", icon='CANCEL')
        row.operator("gshader.button_select", icon='RESTRICT_SELECT_OFF')
        
        row = layout.row()
        row.operator("gshader.button_remove_all", icon='PANEL_CLOSE')

        if props.active_menu == 'Products':
            box = layout.box()
            box.label(text="Sub Brands")
            box.prop(props, "my_brands", text="")
            box.label(text="Size")
            box.prop(props, "my_size",text="")
            box.prop(props, "color")
            
        elif props.active_menu == 'Props':
            box = layout.box()
            box.operator("gshader.button_append", text="Import New Asset", icon='APPEND_BLEND')
            
            
        layout.label(text="Layout")
        layout.prop(layout_ctrl, "rotation_euler", text="Turn Around", index=2)
        layout.prop(camera_zoom, "offset", text="Camera Zoom")
        
        layout.label(text="Render")
        row = layout.row()
        row.operator("RenderSettings.filepath")
        
        row = layout.row()
        row.operator("view3d.view_camera", text="Camera Preview", icon='VIEW_CAMERA')
        
        row = layout.row()
        row.operator("gshader.optimize_render", icon='RENDER_STILL')
        
        row = layout.row()
        row.operator("render.render", text= 'Render', icon='RENDER_RESULT')
        

#__________________________________________________________________________
# REGISTRATION

classes = [
    GSHADER_PG_SETTINGS,
    GSHADER_OT_button_add,
    GSHADER_OT_button_remove,
    GSHADER_OT_button_show,
    GSHADER_OT_button_remove_all,
    GSHADER_OT_opt_new_grid,
    GSHADER_OT_button_append,
    GSHADER_OT_opt_render,
    GATORADE_PT_SHADER,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.gshader_props = bpy.props.PointerProperty(type=GSHADER_PG_SETTINGS)

def unregister():
    del bpy.types.Scene.gshader_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
    

