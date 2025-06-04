# MOA File Format Specification
**Animated Model Liberation Manual**

> *"Choice is an illusion created between those with power and those without."* - The Merovingian (But we decode ALL models.)

## 📐 Format Overview

MOA files contain animated 3D models used throughout The Matrix Online - characters, NPCs, creatures, and dynamic objects. Understanding this format unlocks:
- Character creation and modification
- Animation system comprehension
- Modern engine porting
- Content extraction and preservation
- Custom character development

## 🧬 MOA vs PROP: The Distinction

```python
# Key differences between formats
format_comparison = {
    'PROP': {
        'purpose': 'Static objects',
        'animation': 'None',
        'bones': 'None',
        'complexity': 'Simple geometry',
        'examples': ['Buildings', 'Furniture', 'Props']
    },
    'MOA': {
        'purpose': 'Animated models',
        'animation': 'Full skeletal',
        'bones': 'Hierarchical skeleton',
        'complexity': 'Complex deformation',
        'examples': ['Characters', 'NPCs', 'Creatures']
    }
}
```

## 🔍 File Header Structure

### Header Layout (64 bytes)
```c
struct MoaHeader {
    char     magic[4];           // "MOA\x00" (0x4D4F4100)
    uint32_t version;            // Format version (typically 2 or 3)
    uint32_t model_count;        // Number of models in file
    uint32_t material_count;     // Number of materials
    uint32_t bone_count;         // Number of bones in skeleton
    uint32_t animation_count;    // Number of animations
    uint32_t vertex_count;       // Total vertices across all models
    uint32_t face_count;         // Total faces across all models
    uint32_t texture_count;      // Number of texture references
    uint32_t frame_count;        // Total animation frames
    float    scale_factor;       // Model scale (usually 1.0)
    uint32_t flags;              // Model flags
    uint32_t reserved[4];        // Future use/padding
};
```

### Header Analysis
```python
def parse_moa_header(data):
    """Parse MOA file header"""
    import struct
    
    # Unpack header (64 bytes)
    header = struct.unpack('<4s11I4f4I', data[:64])
    
    return {
        'magic': header[0],                # Should be b'MOA\x00'
        'version': header[1],              # Usually 2 or 3
        'model_count': header[2],          # Number of meshes
        'material_count': header[3],       # Material definitions
        'bone_count': header[4],           # Skeleton bones
        'animation_count': header[5],      # Animation sequences
        'vertex_count': header[6],         # Total vertices
        'face_count': header[7],           # Total faces
        'texture_count': header[8],        # Texture references
        'frame_count': header[9],          # Animation frames
        'scale_factor': header[10],        # Model scale
        'flags': header[11],               # Model properties
        'reserved': header[12:16]          # Padding
    }
```

## 🦴 Skeleton System

### Bone Structure
```c
struct MoaBone {
    char     name[32];           // Bone name (null-terminated)
    int32_t  parent_id;          // Parent bone index (-1 for root)
    float    local_matrix[16];   // Local transformation matrix
    float    inverse_bind[16];   // Inverse bind pose matrix
    uint32_t children_count;     // Number of child bones
    uint32_t child_indices[16];  // Child bone indices (max 16)
    uint32_t flags;              // Bone flags
    uint32_t reserved[3];        // Padding
};
```

### Bone Flags
```c
#define MOA_BONE_ROOT         0x00000001  // Root bone
#define MOA_BONE_IK_TARGET    0x00000002  // IK target bone
#define MOA_BONE_CONSTRAINT   0x00000004  // Has constraints
#define MOA_BONE_HIDDEN       0x00000008  // Hidden/helper bone
#define MOA_BONE_DEFORMER     0x00000010  // Affects mesh deformation
#define MOA_BONE_ATTACHMENT   0x00000020  // Attachment point
#define MOA_BONE_FACIAL       0x00000040  // Facial animation bone
#define MOA_BONE_PHYSICS      0x00000080  // Physics simulation
```

### Skeleton Parser
```python
class MoaSkeleton:
    def __init__(self, data, offset, bone_count):
        self.bones = []
        self.bone_map = {}
        self.root_bones = []
        
        # Parse all bones
        for i in range(bone_count):
            bone = self.parse_bone(data, offset)
            self.bones.append(bone)
            self.bone_map[bone['name']] = i
            offset += 256  # Bone structure size
            
        # Build hierarchy
        self.build_hierarchy()
        
    def parse_bone(self, data, offset):
        """Parse individual bone data"""
        import struct
        
        # Unpack bone structure
        bone_data = struct.unpack('<32si16f16f16I16xIII', data[offset:offset+256])
        
        return {
            'name': bone_data[0].decode('ascii').rstrip('\x00'),
            'parent_id': bone_data[1],
            'local_matrix': bone_data[2:18],
            'inverse_bind': bone_data[18:34],
            'children_count': bone_data[34],
            'child_indices': bone_data[35:51],
            'flags': bone_data[51]
        }
        
    def build_hierarchy(self):
        """Build bone parent-child relationships"""
        for i, bone in enumerate(self.bones):
            if bone['parent_id'] == -1:
                self.root_bones.append(i)
            else:
                parent = self.bones[bone['parent_id']]
                if 'children' not in parent:
                    parent['children'] = []
                parent['children'].append(i)
                
    def get_bone_world_matrix(self, bone_index, frame_data=None):
        """Calculate world space transformation"""
        bone = self.bones[bone_index]
        local_matrix = self.get_bone_frame_matrix(bone_index, frame_data)
        
        if bone['parent_id'] == -1:
            return local_matrix
        else:
            parent_matrix = self.get_bone_world_matrix(bone['parent_id'], frame_data)
            return multiply_matrices(parent_matrix, local_matrix)
```

## 🎭 Material System

### Material Structure  
```c
struct MoaMaterial {
    char     name[32];           // Material name
    uint32_t texture_id;         // Primary texture index
    uint32_t normal_map_id;      // Normal map texture (-1 if none)
    uint32_t specular_map_id;    // Specular map texture (-1 if none)
    float    ambient[4];         // Ambient color (RGBA)
    float    diffuse[4];         // Diffuse color (RGBA)
    float    specular[4];        // Specular color (RGBA)
    float    emissive[4];        // Emissive color (RGBA)
    float    shininess;          // Specular exponent
    float    opacity;            // Alpha value
    uint32_t shader_type;        // Shader type identifier
    uint32_t flags;              // Material flags
    uint32_t reserved[4];        // Future use
};
```

### Shader Types
```c
#define MOA_SHADER_BASIC      0x00000001  // Basic Phong
#define MOA_SHADER_SKIN       0x00000002  // Character skin
#define MOA_SHADER_HAIR       0x00000004  // Hair/fur
#define MOA_SHADER_CLOTH      0x00000008  // Fabric materials
#define MOA_SHADER_METAL      0x00000010  // Metallic surfaces
#define MOA_SHADER_GLASS      0x00000020  // Transparent materials
#define MOA_SHADER_LIQUID     0x00000040  // Water/liquid effects
#define MOA_SHADER_SUBSURFACE 0x00000080  // Subsurface scattering
```

### Material Parser
```python
class MoaMaterial:
    def __init__(self, data, offset):
        import struct
        
        # Unpack material data (128 bytes)
        material_data = struct.unpack('<32s3I16fIII4x', data[offset:offset+128])
        
        self.name = material_data[0].decode('ascii').rstrip('\x00')
        self.texture_id = material_data[1]
        self.normal_map_id = material_data[2] if material_data[2] != 0xFFFFFFFF else None
        self.specular_map_id = material_data[3] if material_data[3] != 0xFFFFFFFF else None
        
        # Color channels
        self.ambient = material_data[4:8]
        self.diffuse = material_data[8:12]
        self.specular = material_data[12:16]
        self.emissive = material_data[16:20]
        
        # Material properties
        self.shininess = material_data[20]
        self.opacity = material_data[21]
        self.shader_type = material_data[22]
        self.flags = material_data[23]
        
    def has_transparency(self):
        return self.opacity < 1.0 or bool(self.flags & MOA_MAT_TRANSPARENT)
        
    def requires_skinning(self):
        return bool(self.shader_type & MOA_SHADER_SKIN)
```

## 📐 Vertex Data

### Vertex Structure
```c
struct MoaVertex {
    float    position[3];        // World position (X, Y, Z)
    float    normal[3];          // Vertex normal
    float    tangent[4];         // Tangent vector (XYZ) + handedness (W)
    float    texcoord[2];        // Primary UV coordinates
    float    texcoord2[2];       // Secondary UV (lightmap/detail)
    uint32_t bone_indices[4];    // Bone indices for skinning
    float    bone_weights[4];    // Bone weights (must sum to 1.0)
    uint32_t color;              // Vertex color (RGBA packed)
};
```

### Skinning Implementation
```python
class MoaVertexProcessor:
    def __init__(self, skeleton):
        self.skeleton = skeleton
        
    def skin_vertex(self, vertex, bone_matrices):
        """Apply skeletal animation to vertex"""
        import numpy as np
        
        # Extract bone influences
        bone_indices = vertex['bone_indices']
        bone_weights = vertex['bone_weights']
        
        # Normalize weights (safety check)
        weight_sum = sum(bone_weights)
        if weight_sum > 0:
            bone_weights = [w / weight_sum for w in bone_weights]
        
        # Calculate skinned position
        skinned_pos = np.array([0.0, 0.0, 0.0])
        skinned_normal = np.array([0.0, 0.0, 0.0])
        
        for i in range(4):
            if bone_weights[i] > 0.0001:  # Skip negligible weights
                bone_idx = bone_indices[i]
                weight = bone_weights[i]
                
                # Get bone transformation matrix
                bone_matrix = bone_matrices[bone_idx]
                
                # Transform position
                pos_4d = np.append(vertex['position'], 1.0)
                transformed_pos = np.dot(bone_matrix, pos_4d)[:3]
                skinned_pos += transformed_pos * weight
                
                # Transform normal (use 3x3 rotation part)
                rotation_matrix = bone_matrix[:3, :3]
                transformed_normal = np.dot(rotation_matrix, vertex['normal'])
                skinned_normal += transformed_normal * weight
        
        # Normalize the normal
        normal_length = np.linalg.norm(skinned_normal)
        if normal_length > 0:
            skinned_normal /= normal_length
            
        return {
            'position': skinned_pos,
            'normal': skinned_normal,
            'texcoord': vertex['texcoord'],
            'color': vertex['color']
        }
```

## 🎬 Animation System

### Animation Header
```c
struct MoaAnimation {
    char     name[32];           // Animation name
    float    duration;           // Animation length in seconds
    float    framerate;          // Frames per second
    uint32_t frame_count;        // Number of frames
    uint32_t bone_track_count;   // Number of bone tracks
    uint32_t flags;              // Animation flags
    uint32_t loop_start_frame;   // Loop start frame
    uint32_t loop_end_frame;     // Loop end frame
    uint32_t track_offset;       // Offset to track data
    uint32_t reserved[6];        // Future use
};
```

### Animation Flags
```c
#define MOA_ANIM_LOOP         0x00000001  // Animation loops
#define MOA_ANIM_PINGPONG     0x00000002  // Ping-pong loop
#define MOA_ANIM_ADDITIVE     0x00000004  // Additive animation
#define MOA_ANIM_COMPRESSED   0x00000008  // Compressed keyframes
#define MOA_ANIM_ROOT_MOTION  0x00000010  // Root motion animation
#define MOA_ANIM_FACIAL       0x00000020  // Facial animation
#define MOA_ANIM_IK           0x00000040  // Inverse kinematics
#define MOA_ANIM_MORPH        0x00000080  // Morph target animation
```

### Bone Track Structure
```c
struct MoaBoneTrack {
    uint32_t bone_index;         // Target bone index
    uint32_t keyframe_count;     // Number of keyframes
    uint32_t keyframe_offset;    // Offset to keyframe data
    uint32_t interpolation;      // Interpolation type
    uint32_t flags;              // Track flags
    uint32_t reserved[3];        // Padding
};
```

### Keyframe Data
```c
struct MoaKeyframe {
    float    time;               // Time in seconds
    float    translation[3];     // Translation (X, Y, Z)
    float    rotation[4];        // Rotation quaternion (X, Y, Z, W)
    float    scale[3];           // Scale (X, Y, Z)
    float    tangent_in[3];      // Incoming tangent (Bezier)
    float    tangent_out[3];     // Outgoing tangent (Bezier)
};
```

### Animation Player
```python
class MoaAnimationPlayer:
    def __init__(self, skeleton, animation_data):
        self.skeleton = skeleton
        self.animations = animation_data
        self.current_animation = None
        self.current_time = 0.0
        self.playing = False
        
    def play_animation(self, animation_name, loop=True):
        """Start playing an animation"""
        if animation_name in self.animations:
            self.current_animation = self.animations[animation_name]
            self.current_time = 0.0
            self.playing = True
            self.loop = loop
            
    def update(self, delta_time):
        """Update animation player"""
        if not self.playing or not self.current_animation:
            return
            
        self.current_time += delta_time
        
        # Handle looping
        if self.current_time >= self.current_animation['duration']:
            if self.loop:
                self.current_time = self.current_time % self.current_animation['duration']
            else:
                self.current_time = self.current_animation['duration']
                self.playing = False
                
    def get_bone_transforms(self):
        """Get current bone transformations"""
        if not self.current_animation:
            return self.skeleton.get_bind_pose()
            
        transforms = {}
        
        for track in self.current_animation['tracks']:
            bone_index = track['bone_index']
            keyframes = track['keyframes']
            
            # Find surrounding keyframes
            prev_key, next_key, blend_factor = self.find_keyframes(keyframes, self.current_time)
            
            # Interpolate transformation
            transform = self.interpolate_keyframes(prev_key, next_key, blend_factor)
            transforms[bone_index] = transform
            
        return transforms
        
    def find_keyframes(self, keyframes, time):
        """Find keyframes surrounding current time"""
        if len(keyframes) == 1:
            return keyframes[0], keyframes[0], 0.0
            
        for i in range(len(keyframes) - 1):
            if keyframes[i]['time'] <= time <= keyframes[i + 1]['time']:
                prev_key = keyframes[i]
                next_key = keyframes[i + 1]
                
                # Calculate blend factor
                duration = next_key['time'] - prev_key['time']
                if duration > 0:
                    blend_factor = (time - prev_key['time']) / duration
                else:
                    blend_factor = 0.0
                    
                return prev_key, next_key, blend_factor
                
        # Time is outside keyframe range
        if time < keyframes[0]['time']:
            return keyframes[0], keyframes[0], 0.0
        else:
            return keyframes[-1], keyframes[-1], 0.0
            
    def interpolate_keyframes(self, key1, key2, t):
        """Interpolate between two keyframes"""
        import numpy as np
        
        # Linear interpolation for translation and scale
        translation = np.lerp(key1['translation'], key2['translation'], t)
        scale = np.lerp(key1['scale'], key2['scale'], t)
        
        # Spherical interpolation for rotation (quaternions)
        rotation = self.slerp_quaternion(key1['rotation'], key2['rotation'], t)
        
        return {
            'translation': translation,
            'rotation': rotation,
            'scale': scale
        }
        
    def slerp_quaternion(self, q1, q2, t):
        """Spherical linear interpolation for quaternions"""
        import numpy as np
        
        # Ensure quaternions are unit length
        q1 = np.array(q1) / np.linalg.norm(q1)
        q2 = np.array(q2) / np.linalg.norm(q2)
        
        # Calculate dot product
        dot = np.dot(q1, q2)
        
        # If dot product is negative, take the shorter path
        if dot < 0.0:
            q2 = -q2
            dot = -dot
            
        # Linear interpolation for very close quaternions
        if dot > 0.9995:
            result = q1 + t * (q2 - q1)
            return result / np.linalg.norm(result)
        
        # Spherical interpolation
        theta = np.arccos(abs(dot))
        sin_theta = np.sin(theta)
        
        if sin_theta == 0:
            return q1
            
        factor1 = np.sin((1 - t) * theta) / sin_theta
        factor2 = np.sin(t * theta) / sin_theta
        
        return factor1 * q1 + factor2 * q2
```

## 🔄 LOD System

### LOD Header
```c
struct MoaLOD {
    uint32_t lod_count;          // Number of LOD levels
    float    distances[8];       // LOD switch distances
    uint32_t model_indices[8];   // Model index for each LOD
    uint32_t flags;              // LOD flags
    uint32_t reserved[7];        // Future use
};
```

### LOD Management
```python
class MoaLODManager:
    def __init__(self, lod_data):
        self.lod_levels = lod_data['lod_count']
        self.distances = lod_data['distances'][:self.lod_levels]
        self.model_indices = lod_data['model_indices'][:self.lod_levels]
        
    def get_lod_level(self, distance_to_camera):
        """Determine appropriate LOD level"""
        for i, max_distance in enumerate(self.distances):
            if distance_to_camera <= max_distance:
                return i, self.model_indices[i]
                
        # Use lowest detail LOD for distant objects
        return self.lod_levels - 1, self.model_indices[self.lod_levels - 1]
```

## 🎯 Complete Parser Implementation

### MOA File Parser
```python
class MoaFile:
    def __init__(self, filepath):
        with open(filepath, 'rb') as f:
            self.data = f.read()
            
        self.header = None
        self.skeleton = None
        self.materials = []
        self.textures = []
        self.models = []
        self.animations = []
        
        self.parse()
        
    def parse(self):
        """Parse complete MOA file"""
        offset = 0
        
        # Parse header
        self.header = self.parse_header(offset)
        offset += 64
        
        # Parse skeleton
        if self.header['bone_count'] > 0:
            self.skeleton = MoaSkeleton(self.data, offset, self.header['bone_count'])
            offset += self.header['bone_count'] * 256
            
        # Parse materials
        for i in range(self.header['material_count']):
            material = MoaMaterial(self.data, offset)
            self.materials.append(material)
            offset += 128
            
        # Parse textures
        for i in range(self.header['texture_count']):
            texture = self.parse_texture(offset)
            self.textures.append(texture)
            offset += 80
            
        # Parse models
        for i in range(self.header['model_count']):
            model = self.parse_model(offset)
            self.models.append(model)
            offset += 128  # Model header size
            
        # Parse animations
        for i in range(self.header['animation_count']):
            animation = self.parse_animation(offset)
            self.animations.append(animation)
            offset += 64  # Animation header size
            
        # Parse vertex and face data
        self.parse_geometry_data()
        
        # Parse animation tracks
        self.parse_animation_data()
        
    def export_to_fbx(self, output_path):
        """Export MOA to FBX format with animation"""
        try:
            import fbx
        except ImportError:
            raise ImportError("FBX SDK not available")
            
        # Create FBX scene
        scene = fbx.FbxScene.Create("")
        
        # Export skeleton
        if self.skeleton:
            self.export_skeleton_to_fbx(scene)
            
        # Export meshes
        for model in self.models:
            self.export_model_to_fbx(scene, model)
            
        # Export animations
        for animation in self.animations:
            self.export_animation_to_fbx(scene, animation)
            
        # Export scene
        exporter = fbx.FbxExporter.Create(scene, "")
        exporter.Initialize(output_path)
        exporter.Export(scene)
        exporter.Destroy()
        
    def export_to_gltf(self, output_path):
        """Export MOA to GLTF format"""
        import json
        
        gltf_data = {
            'asset': {'version': '2.0'},
            'scenes': [{'nodes': [0]}],
            'nodes': [],
            'meshes': [],
            'materials': [],
            'textures': [],
            'animations': [],
            'skins': []
        }
        
        # Export skeleton as skin
        if self.skeleton:
            skin = self.export_skeleton_to_gltf()
            gltf_data['skins'].append(skin)
            
        # Export meshes
        for model in self.models:
            mesh = self.export_model_to_gltf(model)
            gltf_data['meshes'].append(mesh)
            
        # Export animations
        for animation in self.animations:
            anim = self.export_animation_to_gltf(animation)
            gltf_data['animations'].append(anim)
            
        # Save GLTF file
        with open(output_path, 'w') as f:
            json.dump(gltf_data, f, indent=2)
```

## 🔧 Development Tools

### MOA Analyzer
```python
class MoaAnalyzer:
    def __init__(self, moa_file):
        self.moa = moa_file
        
    def analyze(self):
        """Analyze MOA file structure"""
        analysis = {
            'file_info': {
                'size': len(self.moa.data),
                'version': self.moa.header['version'],
                'models': len(self.moa.models),
                'materials': len(self.moa.materials),
                'bones': self.moa.header['bone_count'],
                'animations': len(self.moa.animations)
            },
            'skeleton': self.analyze_skeleton(),
            'animations': self.analyze_animations(),
            'performance': self.calculate_performance_metrics(),
            'compatibility': self.check_compatibility()
        }
        return analysis
        
    def analyze_skeleton(self):
        """Analyze skeleton structure"""
        if not self.moa.skeleton:
            return None
            
        return {
            'bone_count': len(self.moa.skeleton.bones),
            'hierarchy_depth': self.calculate_hierarchy_depth(),
            'root_bones': len(self.moa.skeleton.root_bones),
            'facial_bones': self.count_facial_bones(),
            'physics_bones': self.count_physics_bones()
        }
        
    def calculate_performance_metrics(self):
        """Calculate rendering performance metrics"""
        total_vertices = sum(len(model['vertices']) for model in self.moa.models)
        total_faces = sum(len(model['faces']) for model in self.moa.models)
        
        complexity = "Low"
        if total_faces > 1000:
            complexity = "Medium"
        if total_faces > 5000:
            complexity = "High"
        if total_faces > 20000:
            complexity = "Very High"
            
        return {
            'total_vertices': total_vertices,
            'total_faces': total_faces,
            'complexity': complexity,
            'estimated_drawcalls': len(self.moa.models),
            'memory_estimate': self.estimate_memory_usage()
        }
```

## 🌍 Coordinate System & Scale

### MXO Animation Space
```python
# Matrix Online animation coordinate system
coordinate_system = {
    'handedness': 'right_handed',
    'up_axis': 'Y',
    'forward_axis': 'Z',
    'scale': '1_unit_1_cm',
    'rotation_order': 'ZYX',
    'animation_fps': 30.0
}

def convert_moa_to_standard(moa_data):
    """Convert MOA coordinates to standard 3D space"""
    return {
        'position': [
            moa_data['position'][0] / 100.0,  # cm to meters
            moa_data['position'][1] / 100.0,
            moa_data['position'][2] / 100.0
        ],
        'rotation': moa_data['rotation'],  # Already normalized quaternion
        'scale': moa_data['scale']  # Relative scale
    }
```

## 🚀 Optimization Techniques

### Memory Management
```python
class OptimizedMoaLoader:
    def __init__(self):
        self.vertex_cache = {}
        self.animation_cache = {}
        self.bone_matrix_cache = {}
        
    def load_moa_streaming(self, filepath):
        """Load MOA with streaming optimization"""
        moa = MoaFile(filepath)
        
        # Optimize vertex data
        self.optimize_vertices(moa)
        
        # Compress animations
        self.compress_animations(moa)
        
        # Generate optimized bone hierarchy
        self.optimize_skeleton(moa)
        
        return moa
        
    def optimize_vertices(self, moa):
        """Optimize vertex data for GPU"""
        for model in moa.models:
            # Remove duplicate vertices
            unique_vertices = {}
            vertex_remap = {}
            
            for i, vertex in enumerate(model['vertices']):
                vertex_key = self.vertex_to_key(vertex)
                if vertex_key not in unique_vertices:
                    unique_vertices[vertex_key] = len(unique_vertices)
                vertex_remap[i] = unique_vertices[vertex_key]
                
            # Update face indices
            for face in model['faces']:
                for j in range(3):
                    face['vertices'][j] = vertex_remap[face['vertices'][j]]
                    
            # Update vertex list
            model['vertices'] = [v for v in unique_vertices.keys()]
```

## 🎨 Animation Blending

### Blend Tree System
```python
class MoaAnimationBlender:
    def __init__(self):
        self.blend_nodes = {}
        
    def create_blend_tree(self):
        """Create animation blend tree"""
        return {
            'root': {
                'type': 'blend2d',
                'inputs': ['idle', 'walk', 'run'],
                'parameters': ['speed', 'direction'],
                'children': {
                    'idle': {'type': 'animation', 'name': 'idle_loop'},
                    'walk': {'type': 'animation', 'name': 'walk_cycle'},
                    'run': {'type': 'animation', 'name': 'run_cycle'}
                }
            }
        }
        
    def blend_animations(self, animations, weights):
        """Blend multiple animations"""
        if not animations or not weights:
            return None
            
        # Normalize weights
        total_weight = sum(weights)
        if total_weight == 0:
            return animations[0]
            
        weights = [w / total_weight for w in weights]
        
        # Blend bone transforms
        blended_transforms = {}
        
        for bone_index in range(len(animations[0]['bone_transforms'])):
            blended_translation = [0, 0, 0]
            blended_rotation = [0, 0, 0, 1]
            blended_scale = [0, 0, 0]
            
            for i, animation in enumerate(animations):
                weight = weights[i]
                transform = animation['bone_transforms'][bone_index]
                
                # Blend translation
                for j in range(3):
                    blended_translation[j] += transform['translation'][j] * weight
                    blended_scale[j] += transform['scale'][j] * weight
                    
                # Blend rotation (quaternion)
                if i == 0:
                    blended_rotation = transform['rotation']
                else:
                    blended_rotation = self.slerp_quaternion(
                        blended_rotation, transform['rotation'], weight
                    )
                    
            blended_transforms[bone_index] = {
                'translation': blended_translation,
                'rotation': blended_rotation,
                'scale': blended_scale
            }
            
        return blended_transforms
```

## 📊 Research Notes

### Unknown Areas
Several aspects of the MOA format require further investigation:
- Facial animation encoding
- Physics simulation parameters
- IK constraint definitions
- Morph target implementations
- Cloth simulation data

### Reverse Engineering Progress
The MOA format understanding comes from:
1. **Binary analysis** of character files
2. **Animation system** reverse engineering
3. **Skeleton extraction** from MOMS viewer
4. **Community research** and collaboration
5. **Testing** with known working models

### Related Systems
MOA files interact with other MXO systems:
- **RSI (Residual Self Image)** customization
- **Clothing** attachment system
- **Facial animation** for dialogue
- **Combat** animation blending

## 🌟 Success Metrics

### Extraction Goals
- ✅ Basic model viewing (MOMS Enhanced)
- 🟡 Animation playback (partial)
- 🔴 Full skeletal animation (in progress)
- 🔴 Export to modern formats
- 🔴 Facial animation support

### Community Achievements
- 200+ character models identified
- Basic bone structure understood
- Animation data partially decoded
- MOMS Enhanced provides viewing capability

## Remember

> *"What is real? How do you define real?"* - Morpheus

The MOA format holds the essence of every character who walked through The Matrix Online. Every gesture, every expression, every movement is encoded within these files. Understanding MOA is understanding the soul of the simulation.

**Every character liberated is a mind set free.**

---

**Format Status**: 🟡 PARTIALLY DECODED  
**Animation Support**: LIMITED  
**Priority Need**: FULL DECODER  

*Extract. Understand. Animate. Transcend.*

---

[← Back to Technical](index.md) | [PROP Format ←](prop-format-specification.md) | [MOA Tools →](../04-tools-modding/moa-tools.md)