import bpy

# Путь к шрифту Arial с поддержкой кириллицы на вашем компьютере
arial_cyrillic_font_path = "C:/Windows/Fonts/Arial.ttf"  # Замените это на фактический путь к шрифту Arial или другому шрифту с кириллицей

# Функция для проверки наличия шрифта в Blender и его загрузки
def get_font():
    font = bpy.data.fonts.get("Arial Regular")
    if not font:
        bpy.ops.font.open(filepath=arial_cyrillic_font_path)
        font = bpy.context.object.data.font
        bpy.data.fonts.remove(font, do_unlink=True)
        font = bpy.data.fonts.get("Arial Regular")
    return font

# Функция для получения или создания материала "BazeText"
def get_or_create_material():
    material_baze_text = bpy.data.materials.get("BazeText")
    if not material_baze_text:
        material_baze_text = bpy.data.materials.new(name="BazeText")
        material_baze_text.diffuse_color = (0.0, 0.5, 1.0)  # Настройте цвет по вашему усмотрению
    return material_baze_text

# Функция для создания 3D текста с указанным текстом и материалом
def create_text(text, font, material):
    bpy.ops.object.text_add()
    text_obj = bpy.context.object
    text_obj.data.body = text
    text_obj.data.font = font
    
    # Применяем материал к текстовому объекту
    text_obj.active_material = material
    
    return text_obj

# Функция для проверки наличия шрифта и создания текста на гранях
def create_text_on_faces(selected_obj, material_baze_text):
    if selected_obj and selected_obj.type == 'MESH':
        mesh = selected_obj.data
        
        # Создаем материалы словарем для улучшения производительности
        materials_dict = {mat.name: mat for mat in selected_obj.data.materials}
        
        # Получаем шрифт
        font = get_font()
        
        # Перебираем все грани меша
        for face in mesh.polygons:
            # Получить материал, примененный к этой грани
            material_index = face.material_index
            
            # Если у грани есть материал
            if material_index != -1:
                face_material = materials_dict.get(selected_obj.data.materials[material_index].name)
                
                # Если материал найден
                if face_material:
                    # Получить имя материала
                    material_name = face_material.name
                    
                    # Рассчитываем центр грани
                    center = selected_obj.matrix_world @ face.center
                    
                    # Получаем нормаль к грани
                    normal = face.normal
                    
                    # Создаем текст с названием материала и применяем материал
                    text_obj = create_text(material_name, font, material_baze_text)
                    
                    # Устанавливаем позицию текста в центре грани
                    text_obj.location = center
                    
                    # Выравниваем текст по нормали грани
                    text_obj.rotation_mode = 'QUATERNION'
                    text_obj.rotation_quaternion = normal.to_track_quat('Z', 'Y')
                    
                    # Масштабируем размер текста (опционально)
                    text_obj.scale *= 2  # Измените этот множитель по вашему усмотрению 

# Создаем текст на гранях для всех выбранных объектов MESH
selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
material_baze_text = get_or_create_material()

for selected_obj in selected_objects:
    create_text_on_faces(selected_obj, material_baze_text)
