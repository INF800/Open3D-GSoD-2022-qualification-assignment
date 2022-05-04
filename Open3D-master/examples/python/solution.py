import os
import open3d as o3d

def write_to_file(list_of_lists, file_path):
    output = ""
    for lst in list_of_lists:
        for ele in lst:
            output += f"{ele}\t"
        output += "\n"
    with open(file_path, "w") as fp:
        fp.write(output)

def main():
    MESH_PATH = "../test_mesh.ply"
    OUTPUT_FILE_PATH = "examples/result.txt"

    assert os.path.exists(MESH_PATH)
    mesh = o3d.io.read_triangle_mesh(MESH_PATH)

    if not mesh.has_adjacency_list(): 
        mesh.compute_adjacency_list()
        # Q1. Do I need to compute adjacency matrix inside core C++ `IdenticallyColoredConnectedComponents`
        # instead of `mesh.compute_adjacency_list()` as above.

    connected_components = mesh.identically_colored_connected_components()
    # Q2. Do I need to sort lists and their elements inside `connected_components`?
    #   - sort by size of lists inside `connected_components`
    #   - sort inside elements of lists inside `connected_components`
    #
    # If YES, do I need to make changes in core C++ code / example code?
    
    write_to_file(connected_components, OUTPUT_FILE_PATH)


if __name__ == "__main__":
    main()