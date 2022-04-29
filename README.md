# Open3D-GSoD-2022-qualification-assignment

**Deadline:** May 06, 23:59 UTC / May 07, 05:29 AM IST

### Tasks

You’re expected to:

- [ ] 1. Compile Open3D from source: http://www.open3d.org/docs/latest/compilation.html.

  <details open>
  <summary>Compilation steps</summary>
    <br>

    <h3>System Specs</h3>

    Note: this is a CPU only machine from github codespaces.

    ```shell
    OS: Ubuntu 20.04.4 LTS (Focal Fossa)                # cat /etc/os-release
    gcc: gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0      # gcc --version
    clang: clang version 10.0.0-4ubuntu1                # clang --version
    cmake: cmake version 3.23.1                         # cfollow steps from `https://apt.kitware.com/` 
    ```
    
  </details>

- [ ] 2. Write C++ function `open3d::geometry::TriangleMesh::IdenticallyColoredConnectedComponents`
- [ ] 3. Write Python binding `open3d.geometry.TriangleMesh.identically_colored_connected_components`.
- [ ] 4. Write `examples/cpp/Solution.cpp` to read the input mesh `test_mesh.ply`, find identically-colored connected components. **Change the build system** so that an executable can be build.
- [ ] 5. Write `examples/python/solution.py` to read the input mesh `test_mesh.ply`, find identically-colored connected components and print results.
- [ ] 6. Output the result of task 3 or 4 (their results shall be the same) to `examples/result.txt`.
- [ ] 7. Write C++ and Python unit tests integrated with Open3D’s unit test system.
- [ ] 8. Document your code, the algorithm used, how to build and run, and etc.

### Reference
Here are some links for your reference:

• Open3D repository: https://github.com/isl-org/Open3D. <br/>
• Open3D docs: http://www.open3d.org/docs. <br/>
• Pybind11: https://github.com/pybind/pybind11. <br/>
• Send an email to us. <br/>

### Submission

To submit your code:

1. Push the code to a private git repository, share the repository with us and ping us via email.<br/>
2. Include all the necessary files. The git history should indicate the files you changed.<br/>
