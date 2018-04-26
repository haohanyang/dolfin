from dolfin import *

if MPI.size(MPI.comm_world) > 1:
    info("Sorry, this demo does not (yet) run in parallel.")
    exit(0)

# Generate meshes
background_mesh = UnitSquareMesh(16, 16)
annulus_mesh = Mesh("../donut.xml.gz")

center = Point(0.5, 0.5)
r_outer = 0.41
r_inner = 0.2

# Build the multimesh
multimesh = MultiMesh()
multimesh.add(background_mesh)
multimesh.add(annulus_mesh)
multimesh.build()

# Identify background cells within the hole
cell_markers = MeshFunction("size_t", background_mesh, 2)
additional_covered_cells = []
for cell_id in multimesh.cut_cells(0) + multimesh.uncut_cells(0):
    cell = Cell(multimesh.part(0), cell_id)
    r = (cell.midpoint() - center).norm()
    if abs(r_inner - r) < abs(r_outer - r):
        cell_markers[cell_id]= 1
        additional_covered_cells.append(cell_id)

# Mark cells as covered
multimesh.mark_covered(0, additional_covered_cells)

# Variational formulation
V = MultiMeshFunctionSpace(multimesh, "P", 1)
u, v = TrialFunction(V), TestFunction(V)
n = FacetNormal(multimesh)
h = 2*Circumradius(multimesh)

a = (inner(grad(u), grad(v)) * dX
        - inner(avg(grad(u)), jump(v, n)) * dI
        - inner(avg(grad(v)), jump(u, n)) * dI
        + Constant(10) / avg(h) * jump(u) * jump(v) * dI
        + inner(jump(grad(u)), jump(grad(v))) * dO)

L = Constant(1) * v * dX

# Assemble system
A = assemble_multimesh(a)
b = assemble_multimesh(L)

boundary = CompiledSubDomain("on_boundary")
bc = MultiMeshDirichletBC(V, Constant(0.0), boundary)

bc.apply(A, b)
V.lock_inactive_dofs(A, b)

# Solve and plot
uh = MultiMeshFunction(V)
x = uh.vector()

solve(A, x, b)

outfile0 = XDMFFile("output/u0.xdmf")
outfile1 = XDMFFile("output/u1.xdmf")

outfile0.write(uh.part(0, deepcopy=True), 0.0)
outfile1.write(uh.part(1, deepcopy=True), 0.0)

outfile0.close()
outfile1.close()
