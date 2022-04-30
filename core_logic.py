from pprint import pprint
import numpy as np
import plotly.graph_objects as go


def dfs(visited, graph, node, accumulator):
    if node not in visited:
        accumulator.append(node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour, accumulator)

def create_same_color_connected_graph(adjacency_list, vertex_colors):
    # only edges with same colored vertices are connected in new graph
    # warning: `new_adjacency_list = [set()]*len(adjacency_list)` will keep the reference to the same set object
    new_adjacency_list = []
    for n in range(len(adjacency_list)):
        new_adjacency_list.append(set())
    for i, adjs in enumerate(adjacency_list):
        for j in adjs:
            if i > j:
                continue
            if vertex_colors[i] == vertex_colors[j]:
                new_adjacency_list[i].add(j)
                new_adjacency_list[j].add(i)
    return new_adjacency_list

def identically_colored_connected_compontents_dfs(adjacency_list, vertex_colors):
    # convert to unique string ids
    for i in range(len(vertex_colors)):
        vertex_colors[i] = f'rgba({int(vertex_colors[i][0]*255)}, {int(vertex_colors[i][1]*255)}, {int(vertex_colors[i][2]*255)}, 255)'
    # create new graph
    new_adjacency_list = create_same_color_connected_graph(adjacency_list, vertex_colors)
    # find connected components using bfs
    connected_components = []
    visited = set()
    for v in range(len(new_adjacency_list)):
        if v in visited:
            continue
        accumulator = []
        dfs(visited, new_adjacency_list, v, accumulator)
        connected_components.append(accumulator)
    return connected_components

def identically_colored_connected_compontents_laplacian(adjacency_list, vertex_colors, debug=False):
    # convert to unique string ids
    for i in range(len(vertex_colors)):
        vertex_colors[i] = f'rgba({int(vertex_colors[i][0]*255)}, {int(vertex_colors[i][1]*255)}, {int(vertex_colors[i][2]*255)}, 255)'
    # create laplacian matrix L = D - A
    laplacian_matrix = np.zeros((len(adjacency_list), len(adjacency_list)))
    for i, adjs in enumerate(adjacency_list):
        degree = 0
        for j in adjs:
            if vertex_colors[i] == vertex_colors[j]:
                degree += 1
        laplacian_matrix[i][i] = degree
        for j in adjs:
            if i>j:
                continue
            if vertex_colors[i] == vertex_colors[j]:
                laplacian_matrix[i, j] = -1
                laplacian_matrix[j,i] = -1
    # find eigen values and eigen vectors
    evals, evecs = np.linalg.eig(laplacian_matrix)
    evals = evals.round(14)
    evecs = evecs.round(14)

    # find connected components
    connected_components = []
    idxs = np.arange(len(evals))[(evals==0.)]
    components = evecs[:, idxs].T
    for component in  components:
        connected_component = np.where(component != 0.)[0]
        connected_components.append(connected_component.tolist())
    return connected_components


def identically_colored_connected_compontents(strategy, **kwargs):
    if strategy=='dfs':
        return identically_colored_connected_compontents_dfs(**kwargs)
    elif strategy=='laplacian':
        return identically_colored_connected_compontents_laplacian(**kwargs)
    else:
        raise ValueError('unknown strategy: {}'.format(strategy))

def get_unique_plotly_colors(n):
    colors = []
    for i in range(n):
        c = np.random.rand(3)
        colors.append(f"rgba({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)}, 255)")
    return colors

def visualize_graph_objects(vertices, adjacency_list, vertex_colors, connected_components):
    fig = go.Figure()
    # original graph
    fig.add_trace(go.Scatter3d(
        x=vertices[:,0],
        y=vertices[:,1],
        z=vertices[:,2],
        mode='markers+text',
        text=['{}'.format(i) for i in range(len(vertices))],
        marker=dict(size=2, color=vertex_colors),
    ))
    for i, adj in enumerate(adjacency_list):
        for j in adj:
            if i>j:
                continue
            if vertex_colors[i] == vertex_colors[j]:
                fig.add_trace(go.Scatter3d(
                    x=[vertices[i][0], vertices[j][0]],
                    y=[vertices[i][1], vertices[j][1]],
                    z=[vertices[i][2], vertices[j][2]],
                    mode='lines',
                    line=dict(color=vertex_colors[i]),
                ))
            else:
                fig.add_trace(go.Scatter3d(
                    x=[vertices[i][0], vertices[j][0]],
                    y=[vertices[i][1], vertices[j][1]],
                    z=[vertices[i][2], vertices[j][2]],
                    mode='lines',
                    line=dict(color='rgba(0,0,0,0.1)'),
                ))
    # new graph where only edges with same colored vertices are connected
    fig.add_trace(go.Scatter3d(
        x=vertices[:,0]+3,
        y=vertices[:,1]+3,
        z=vertices[:,2],
        mode='markers+text',
        text=['{}'.format(i) for i in range(len(vertices))],
        marker=dict(size=2, color=vertex_colors),
    ))
    shift = 3
    for i, adj in enumerate(adjacency_list):
        for j in adj:
            if i>j:
                continue
            fig.add_trace(go.Scatter3d(
                x=[vertices[i][0]+shift, vertices[j][0]+shift],
                y=[vertices[i][1]+shift, vertices[j][1]+shift],
                z=[vertices[i][2], vertices[j][2]],
                mode='lines',
                line=dict(color='rgba(0,0,0,0.1)'),
            ))
    # connected components
    n_components = len(connected_components)
    unique_colors = get_unique_plotly_colors(n_components)
    colors = [None]*len(vertices)
    for i, c in enumerate(connected_components):
        for v in c:
            colors[v] = unique_colors[i]
    fig.add_trace(go.Scatter3d(
        x=vertices[:,0]+3,
        y=vertices[:,1]-3,
        z=vertices[:,2],
        mode='markers+text',
        text=['{}'.format(i) for i in range(len(vertices))],
        marker=dict(size=2, color=colors),
    ))

    fig.show()


def get_inputs1():
    adjacency_list = [
        {1,3,2},
        {0,3,4},
        {0,3,5},
        {0,1,4,6,5,2},
        {1,3,6},
        {2,3,6},
        {5,3,4},
    ]
    vertex_colors = [
        # 'R', 'G', 'B', 'R', 'G', 'R', 'R'
        [1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.],
        [1., 0., 0.],
        [0., 1., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
    ]
    vertices = np.array([
        [1, 2, 0],
        [3, 2, 0],
        [0, 1, 0],
        [2, 1, 0],
        [4, 1, 0],
        [1, 0, 0],
        [3, 0, 0],
    ])
    return adjacency_list, vertex_colors, vertices

def get_inputs2():
    import open3d as o3d
    mesh = o3d.io.read_triangle_mesh("./test_mesh.ply")
    # visualize
    # o3d.visualization.draw_geometries([mesh])
    # print("Has vertex colors:", mesh.has_vertex_colors())
    # traingles = np.asarray(mesh.triangles)
    vertices = np.asarray(mesh.vertices)
    vertex_colors = np.asarray(mesh.vertex_colors)
    mesh.compute_adjacency_list()
    return  mesh.adjacency_list, vertex_colors.tolist(), vertices


if __name__=='__main__':

    adjacency_list, vertex_colors, vertices = get_inputs1()
    ccs1 = identically_colored_connected_compontents(strategy='dfs', adjacency_list=adjacency_list, vertex_colors=vertex_colors)
    adjacency_list, vertex_colors, vertices = get_inputs1()
    ccs2 = identically_colored_connected_compontents(strategy='laplacian', adjacency_list=adjacency_list, vertex_colors=vertex_colors, debug=True)

    print("\nCASE 1:")
    print("Connected components using DFS:")
    print(ccs1)
    print("Connected components using Laplacian Matrix:")
    print(ccs2)

    visualize_graph_objects(vertices, adjacency_list, vertex_colors, connected_components=ccs1)

    adjacency_list, vertex_colors, vertices = get_inputs2()
    ccs1 = identically_colored_connected_compontents(strategy='dfs', adjacency_list=adjacency_list, vertex_colors=vertex_colors)
    adjacency_list, vertex_colors, vertices = get_inputs2()
    ccs2 = identically_colored_connected_compontents(strategy='laplacian', adjacency_list=adjacency_list, vertex_colors=vertex_colors, debug=False)

    # Note: may not work because eigen values of laplacian matrix are negative!
    print("\nCASE 2:")
    print("Connected components using DFS:")
    print(ccs1)
    print("Connected components using Laplacian Matrix:")
    print(ccs2)    

    visualize_graph_objects(vertices, adjacency_list, vertex_colors, connected_components=ccs1)
