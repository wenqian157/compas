import compas

from compas.datastructures import Mesh
from compas.geometry import smooth_area
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

vertices  = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
faces     = {fkey: mesh.face_vertices(fkey) for fkey in mesh.faces()}
adjacency = {key: mesh.vertex_faces(key) for key in mesh.vertices()}
fixed     = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

lines = []
for u, v in mesh.edges():
    lines.append({
        'start': mesh.vertex_coordinates(u, 'xy'),
        'end'  : mesh.vertex_coordinates(v, 'xy'),
        'color': '#cccccc',
        'width': 1.0,
    })

vertices = smooth_area(vertices, faces, adjacency, fixed=fixed, kmax=100)

for key, attr in mesh.vertices(True):
    attr['x'] = vertices[key][0]
    attr['y'] = vertices[key][1]
    attr['z'] = vertices[key][2]

plotter = MeshPlotter(mesh)

plotter.draw_lines(lines)
plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
plotter.draw_edges()

plotter.show()