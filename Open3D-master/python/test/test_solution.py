import open3d as o3d
import pytest


@pytest.fixture
def mesh():
    MESH_PATH = "../test_mesh.ply"
    mesh = o3d.io.read_triangle_mesh(MESH_PATH)
    if not mesh.has_adjacency_list(): 
        mesh.compute_adjacency_list()
    return mesh

def test_adj_list_creation(mesh):
    assert mesh.has_adjacency_list(), "Adjacency list creation failed!"

def test_identically_colored_connected_components(mesh):
    # a. check if tot num of vertices in connected components is same as total nodes
    # b. vertices must appear only once in whole output
    connected_components = mesh.identically_colored_connected_components()
    tot_nodes = len(mesh.adjacency_list)
    visited = set()
    tot_commponents = 0
    for i, components in enumerate(connected_components):
        for v in components:
            assert v not in visited, f"{v} appears more than once in connected components. There may be more such nodes."
            visited.add(v)
    assert len(visited)==tot_nodes, "Same node is appearing more than once."
