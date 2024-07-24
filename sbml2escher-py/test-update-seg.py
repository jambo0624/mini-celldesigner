# 定义检查点是否在线段上的函数
def is_point_on_segment(px, py, x1, y1, x2, y2):
    # 计算叉积来判断点是否在线段上
    cross_product = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
    if abs(cross_product) > 1e-6:
        return False

    # 检查点是否在x范围内
    if px < min(x1, x2) or px > max(x1, x2):
        return False

    # 检查点是否在y范围内
    if py < min(y1, y2) or py > max(y1, y2):
        return False

    return True

# 删除目标 segment 并插入新的 node 和 segments
def update_segments_with_node(segments, nodes, start_x, start_y):
    segment_to_remove = None
    from_node_id = None
    to_node_id = None

    # 找到包含 start_x 和 start_y 的 segment
    for seg_id, segment in segments.items():
        from_node = nodes[segment['from_node_id']]
        to_node = nodes[segment['to_node_id']]
        if is_point_on_segment(start_x, start_y, from_node['x'], from_node['y'], to_node['x'], to_node['y']):
            segment_to_remove = seg_id
            from_node_id = segment['from_node_id']
            to_node_id = segment['to_node_id']
            break

    if segment_to_remove is None:
        print("No segment found containing the point.")
        return

    # 删除目标 segment
    del segments[segment_to_remove]

    # 创建新的 node
    new_node_id = max(nodes.keys()) + 1
    nodes[new_node_id] = {
        'node_type': 'multimarker',
        'x': start_x,
        'y': start_y,
    }

    # 创建两个新的 segments
    if segments:
        new_segment_1_id = max(segments.keys()) + 1
    else:
        new_segment_1_id = 1
    new_segment_2_id = new_segment_1_id + 1

    segments[new_segment_1_id] = {
        'from_node_id': from_node_id,
        'to_node_id': new_node_id,
        'b1': None,
        'b2': None,
    }

    segments[new_segment_2_id] = {
        'from_node_id': new_node_id,
        'to_node_id': to_node_id,
        'b1': None,
        'b2': None,
    }

# 示例用法
nodes = {
    1: {'node_type': 'multimarker', 'x': 0, 'y': 0},
    2: {'node_type': 'multimarker', 'x': 10, 'y': 10}
}

segments = {
    1: {'from_node_id': 1, 'to_node_id': 2, 'b1': None, 'b2': None}
}

start_x = 5
start_y = 5

update_segments_with_node(segments, nodes, start_x, start_y)

print(nodes)
print(segments)
