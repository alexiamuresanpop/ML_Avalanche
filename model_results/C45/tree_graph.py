import graphviz


dot = graphviz.Digraph('Weka_Tree', comment='Formatted Decision Tree', format='png')

dot.attr(rankdir='TB', size='16,10!', ratio='fill')
dot.attr('node', fontname='Helvetica', fontsize='10', shape='ellipse', style='filled', color='#333333')
dot.attr('edge', fontname='Helvetica', fontsize='9', color='#555555')

# Styling Helper
FEATURE_COLOR = '#EBF4F6'  # Soft light blue for decision nodes
CLASS_COLORS = {
    'Low': '#D4EDDA',       # Soft green
    'Medium': '#FFF3CD',    # Soft yellow
    'High': '#F8D7DA'       # Soft red
}

# Node definitions: (node_id, label, is_leaf, class_name, count_info)
nodes = [
    # Level 0
    ("n0", "rainfall_most_exposed_area", False, None, None),
    
    # Level 1
    ("n1", "temperature_max", False, None, None),
    ("n2", "rainfall_most_exposed_area", False, None, None),
    
    # Level 2
    ("n3", "publish_hour", False, None, None),
    ("n4", "publish_month", False, None, None),
    ("n5", "wind_speed", False, None, None),
    ("n6", "publish_month", False, None, None),
    
    # Level 3
    ("n7", "wind_speed", False, None, None),
    ("n8", "rainfall_most_exposed_area", False, None, None),
    ("n9", "wind_direction", False, None, None),
    ("l_low1", "Low (1446.0/366.0)", True, "Low", "1446.0/366.0"),
    ("l_med1", "Medium (237.0/85.0)", True, "Medium", "237.0/85.0"),
    ("n10", "wind_speed", False, None, None),
    ("l_high1", "High (773.0/112.0)", True, "High", "773.0/112.0"),
    ("n11", "temperature_min", False, None, None),
    
    # Level 4
    ("l_med2", "Medium (130.0/58.0)", True, "Medium", "130.0/58.0"),
    ("n12", "temperature_min", False, None, None),
    ("n13", "temperature_max", False, None, None),
    ("l_med3", "Medium (1278.0/416.0)", True, "Medium", "1278.0/416.0"),
    ("l_low2", "Low (127.0/33.0)", True, "Low", "127.0/33.0"),
    ("n14", "wind_shift_direction", False, None, None),
    ("l_med4", "Medium (471.0/189.0)", True, "Medium", "471.0/189.0"),
    ("n15", "temperature_max", False, None, None),
    ("l_high2", "High (362.0/90.0)", True, "High", "362.0/90.0"),
    ("n16", "rain_snow_line_start", False, None, None),
    
    # Level 5
    ("l_med5", "Medium (116.0/52.0)", True, "Medium", "116.0/52.0"),
    ("l_high3", "High (105.0/36.0)", True, "High", "105.0/36.0"),
    ("l_med6", "Medium (3468.0/1000.0)", True, "Medium", "3468.0/1000.0"),
    ("n17", "publish_month", False, None, None),
    ("l_low3", "Low (131.0/46.0)", True, "Low", "131.0/46.0"),
    ("n18", "cloud_cover", False, None, None),
    ("l_high4", "High (164.0/35.0)", True, "High", "164.0/35.0"),
    ("n19", "publish_month", False, None, None),
    ("l_med7", "Medium (148.0/61.0)", True, "Medium", "148.0/61.0"),
    ("l_high5", "High (145.0/61.0)", True, "High", "145.0/61.0"),
    
    # Level 6
    ("l_med8", "Medium (1480.0/570.0)", True, "Medium", "1480.0/570.0"),
    ("n20", "geographical_region", False, None, None),
    ("l_low4", "Low (123.0/55.0)", True, "Low", "123.0/55.0"),
    ("l_med9", "Medium (589.0/252.0)", True, "Medium", "589.0/252.0"),
    ("l_high6", "High (337.0/141.0)", True, "High", "337.0/141.0"),
    ("l_med10", "Medium (150.0/62.0)", True, "Medium", "150.0/62.0"),
    
    # Level 7
    ("l_low5", "Low (123.0/37.0)", True, "Low", "123.0/37.0"),
    ("n21", "wind_direction", False, None, None),
    
    # Level 8
    ("l_low6", "Low (112.0/41.0)", True, "Low", "112.0/41.0"),
    ("n22", "rain_snow_line_altitude_masl", False, None, None),
    
    # Level 9
    ("n23", "rainfall_average", False, None, None),
    ("n24", "publish_month", False, None, None),
    
    # Level 10
    ("n25", "temperature_max", False, None, None),
    ("l_med11", "Medium (256.0/78.0)", True, "Medium", "256.0/78.0"),
    ("l_med12", "Medium (241.0/111.0)", True, "Medium", "241.0/111.0"),
    ("l_low7", "Low (304.0/90.0)", True, "Low", "304.0/90.0"),
    
    # Level 11
    ("l_med13", "Medium (188.0/86.0)", True, "Medium", "188.0/86.0"),
    ("l_low8", "Low (186.0/83.0)", True, "Low", "186.0/83.0"),
]

# Add nodes to graph
for node_id, label, is_leaf, class_name, count_info in nodes:
    if is_leaf:
        dot.node(node_id, label=f"<b>{class_name}</b>\n<font point-size='8'>{count_info}</font>", 
                 shape='box', style='filled,rounded', 
                 fillcolor=CLASS_COLORS[class_name], color='#666666')
    else:
        dot.node(node_id, label=f"<b>{label}</b>", shape='ellipse', 
                 fillcolor=FEATURE_COLOR, color='#4B6584')

# Edges definition: (parent_id, child_id, label)
edges = [
    ("n0", "n1", "<= 14.0"),
    ("n0", "n2", "> 14.0"),
    
    ("n1", "n3", "<= 2.0"),
    ("n1", "n4", "> 2.0"),
    
    ("n2", "n5", "<= 24.0"),
    ("n2", "n6", "> 24.0"),
    
    ("n3", "n7", "<= 14.0"),
    ("n3", "n8", "> 14.0"),
    
    ("n4", "n9", "<= 4.0"),
    ("n4", "l_low1", "> 4.0"),
    
    ("n5", "l_med1", "= Breeze"),
    ("n5", "n10", "!= Breeze"),
    
    ("n6", "l_high1", "<= 3.0"),
    ("n6", "n11", "> 3.0"),
    
    ("n7", "l_med2", "= Breeze"),
    ("n7", "n12", "!= Breeze"),
    
    ("n8", "n13", "<= 8.0"),
    ("n8", "l_med3", "> 8.0"),
    
    ("n9", "l_low2", "= NW"),
    ("n9", "n14", "!= NW"),
    
    ("n10", "l_med4", "= Fresh breeze"),
    ("n10", "n15", "!= Fresh breeze"),
    
    ("n11", "l_high2", "<= -5.0"),
    ("n11", "n16", "> -5.0"),
    
    ("n12", "l_med5", "<= -12.0"),
    ("n12", "l_high3", "> -12.0"),
    
    ("n13", "l_med6", "<= -4.0"),
    ("n13", "n17", "> -4.0"),
    
    ("n14", "l_low3", "= W"),
    ("n14", "n18", "!= W"),
    
    ("n15", "l_high4", "<= -4.0"),
    ("n15", "n19", "> -4.0"),
    
    ("n16", "l_med7", "<= 0.0"),
    ("n16", "l_high5", "> 0.0"),
    
    ("n17", "l_med8", "<= 3.0"),
    ("n17", "n20", "> 3.0"),
    
    ("n18", "l_low4", "= Clear skies"),
    ("n18", "l_med9", "!= Clear skies"),
    
    ("n19", "l_high6", "<= 4.0"),
    ("n19", "l_med10", "> 4.0"),
    
    ("n20", "l_low5", "= Eastern Norway"),
    ("n20", "n21", "!= Eastern Norway"),
    
    ("n21", "l_low6", "= N"),
    ("n21", "n22", "!= N"),
    
    ("n22", "n23", "<= 300.0"),
    ("n22", "n24", "> 300.0"),
    
    ("n23", "n25", "<= 0.0"),
    ("n23", "l_med11", "> 0.0"),
    
    ("n24", "l_med12", "<= 4.0"),
    ("n24", "l_low7", "> 4.0"),
    
    ("n25", "l_med13", "<= -1.0"),
    ("n25", "l_low8", "> -1.0")
]

# Add edges to graph
for parent, child, label in edges:
    dot.edge(parent, child, label=label)

# Render diagram to file
output_path = dot.render('weka_tree_styled', cleanup=True)