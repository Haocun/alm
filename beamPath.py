import numpy as np
import beamq
import component
from copy import deepcopy

class beamPath(object):

    """
    -- beamPath --

    A beam path object consists of a few things:
    
        * A seed beam. This defines the "input beam" of your system.
                When calculating the beam properties somewhere in a beam
                path, this is the origin of the beam which is propagated 
                around the system. It is defined by a beamq object which is
                stored in the beamPath.seedq property, also the location
                of the seed beam in the beam path is defined by the 
                beamPath.seedz property. This beam can be defined anywhere
                in the beam path and need not be at the "beginning."
     
        * A target beam. This defines the "output beam" of your system.
                This is the beam which you would like to match into.
                It is defined similarly to the seed beam by the properties
                beamPath.targetq and beamPath.targetz. It is also used by 
                the various optimization routines when trying to maximize 
                the mode overlap with the seed beam.
     
        * Components. These are the various optical components in the beam
                path which affect the propagation of beams in the path.
                It is a vector array of objects in the component class.
                Each component has a certain transfer matrix and position,
                these properties are stored in the component class.
                The beamPath class stores the array of components in the 
                beamPath.components array. The ordering of the elements in 
                this array is always by increasing z position. This means
                that the array index of components in the component array
                may change if the z positions are changed. The component
                class also has a 'label' property, which allows a component
                to be indexed unambiguously. See beamPath.component below.
     
    	The beamPath class also has methods which facilitate in calculating 
        beam propagation and laying out your beam path.
    """


    def __init__ (self, seedq, seedz, targetq, targetz):

        self.seedq = beamq
        self.seedz = []
        self.targetq = beamq
        self.targetz = []
            
        self.components_raw = component            
        #self.components_raw[1]=[]  #empty the component list



#
#    def __lossFuc (self, zVec, *args):
#        path2 = self.duplicate
#        path2.__batchMove(zVec)
#
#        losses = 1-path2self.targetOverlap
#        del(path2)
#
#        return losses
#
#
#
#    def __applyCostFunc (self, costFunc, zVec, *args):
#        path2 = self.duplicate
#        path2.__batchMove(zVec)
#
#        cost = costFunc(path2)
#        del(path2)
#
#        return losses
#
#
#
#    def __batchmove(self, moveVec):
#
#        comps = self.components
#
#        compCount = len(comps)
#        moveCount = len(moveVec)
#
#        if moveCount > compCount:
#            self.targetz = moveVec(compCount+1)
#
#        for j in rang(len(compCount)):
#            if comps[j].z == moveVec(j):
#                pass
#            comps[j].z = moveVec(j)
#
#
#
#    def __sortComponents(self):
#
#        complist = [self.components_raw]
#
#        zlist = [complist.z]
#        [zsorted,zindex] = zlist.sort
#
#        # if len(complist) < 1 or all(complist == complist(zindex))
#        #         return
#        
#        self.components = complist[zindex]
#
#
#
#    def __beamFitError(self, waistParams, zPred, widthPred, wavelength):
#
#        pathdup = self.duplicate
#        pathdup.seedq = beamq.beamWaistAndZ(waistParams[1], waistParams[2], wavelength)
#        qout = pathdup.qPropagate(zPred);
#
#        widthPred = reshape(widthPred,1,numel(widthPred))
#
#        width = [qout.beamWidth]
#            
#        error = sum((widthPred-width)**2)



    def duplicate(self):

        # -- beamPath.duplicate --
        #
        #    Creates a new beampath with the same properties as the original.
        #    Example:
        #    path1copy = path1.duplicate

        return deepcopy(self) #beamPath(self.seedq.duplicate, self.seedz, self.targetq.duplicate, self.targetz)



    def branchPath(self, zlink):

        # -- beamPath.branchPath --
        #
        #    create a new beamPath object which is identical to the calling object,
        #    but has a seed beam which is calculated from the seed beam in the first
        #    object but located in another place.
        # 
        #    this can be useful when you want to make a new path which has the same
        #    beam as the original path at a given location, and then allows you to 
        #    alter the componentsin the new path without changing the beam at the 
        #    location you chose.
        #
        #    syntax: path2 = path1.branchPath(zlink)
        #    zlink is the position of the beam you would like to be the seed beam of 
        #    the new path.

        qlink = self.qPropagate(zlink)
        self = self.duplicate()

        self.seedq = qlink
        self.seedz = zlink



    def set_components(self, comps):

        self.components_raw = comps

        return self


    @property
    def components(self):

        self.sortComponents
        return self.components_raw



#    def display(self):










    def addComponent(self, newComponent):
        
        # -- beamPath.addComponent --
        #
        #    add a component object to a beampath.
        #    Example:
        #    mylens = component.lens(2,0,'mylens')
        #    path1.addComponent(mylens)

        self.components = self.components.append(newComponent)



    def deleteComponent(self, delLabel):

        # -- beamPath.deleteComponent --
        #   
        #    remove a component object from a beampath
        #    Example:
        #    path1.deleteComponent('mylens');
            
        delIndex = self.findComponentIndex(delLabel)
        del self.components[delIndex-1]
            
        return self.components



    def moveComponent(self, componentLabel, displacement, isabsolute = ''):

        # -- beamPath.moveComponent --
        #   
        #    Change the z parameter of a component in a beam path by a given displacement.
        #    Example:
        #    path1.moveComponent('lens1',0.5)
        #    This will move 'lens1' 0.5m in the positive z direction.
        #    To move a component to an absolute position use the extra argument 'absolute.'
        #    Example:
        #    path1.moveComponent('lens1',2.5,'absolute')
        #    This will move 'lens1' to the position z = 2.5m

        componentIndex = self.findComponentIndex(componentLabel)
            
        componentToMove = self.components(componentIndex)
        zstart = componentToMove.z

        if isabsolute == 'absolute':
            displacement = displacement - zstart

        componentToMove.z = zstart + displacement



    def replaceCompnent(self, componentLabel, newComponent):

        # -- beamPath.replaceComponent --
        #
        #    Remove a component and replace it with another, the new component inherits the
        #    z position and label of the previous component being removed.
        #    Example:
        #    newlens = component.lens(1)
        #    path1.replaceComponent('lens1',newlens)
        #    This removes the old 'lens1' component and adds the new component at the 
        #    position where 'lens1' was. The name 'lens1' is inherited by the new component.

        componentIndex = self.findComponentIndex(componentLabel)
            
        newComponent.z = self.components(componentIndex).z
        newComponent.label = self.components(componentIndex).label            
        self.deleteComponent(componentIndex)
        self.addComponent(newComponent)



    def component(self, componentLabel):

        #  -- beamPath.component --
        #
        #     Allows access to component in a beam path by use of the component label.
        #     Example:
        #     To find out the z position of 'mylens' which might be the 
        #     third lens in the component list, one could either do:
        #    
        #     path1.components(3).z
        #     or
        #     path1.component('mylens').z  %%% <-- notice the use of the 
        #                                      singular word 'component' in this case
        #     which would yield the same result.
        #     However, the component index may change if new components are 
        #     added, the indexing is always in order of increasing z position,
        #     so this method allows one to access the desired component
        #     unambiguously.

        
















a = beamPath(0,0,0,0)
b = a.duplicate()
print (a, b)
print ('  next  ')
print (a.seedq, a.seedz, a.targetq, a.components_raw)



