import hou

def make_smoke_setup():

    ### base nodes ###
    # get obj 
    root = hou.node("/obj")
    # create geo node called FX
    container = root.createNode("geo","FX")
    
    ### add SOP ###
    # create add SOP in "FX" geo node
    add_node = container.createNode("add")
    # set parm to add 1 point
    add_node.parm('points').set(1)
    
    ### VDB SOP ###
    # make a vdbfromparticles SOP 
    vdb_node = container.createNode("vdbfromparticles")
    
    # disable sdf, enable fog
    vdb_node.parm('builddistance').set(0)
    vdb_node.parm('buildfog').set(1)
    
    # connect with add node
    vdb_node.setFirstInput(add_node,0)
    
    ### pyro solver SOP ###
    pyro_solver = container.createNode("pyrosolver")
    
    # change temperature source to density
    pyro_solver.parm("source_volume2").set("density")
    
    # enable turbulence and set
    pyro_solver.parm("enable_turbulence").set(1)
    pyro_solver.parm("turbulence").set(5)
    
    # connect to vdb SOP
    pyro_solver.setFirstInput(vdb_node,0)
    
    # set flags to pyro solver
    pyro_solver.setRenderFlag(1)
    pyro_solver.setDisplayFlag(1)
    
    ### organise ###
    children = container.children()
    for child in children:
        child.moveToGoodPosition()
