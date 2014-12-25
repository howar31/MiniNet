"""FatTree topology by Howar31

Configurable K-ary FatTree topology
Only edit K should work

Pass '--topo=fattree' from the command line
"""

from mininet.topo import Topo

class FatTree( Topo ):

    def __init__( self ):

        # Topology settings
        K = 4                           # K-ary FatTree
        podNum = K                      # Pod number in FatTree
        coreSwitchNum = pow((K/2),2)    # Core switches 
        aggrSwitchNum = ((K/2)*K)       # Aggregation switches
        edgeSwitchNum = ((K/2)*K)       # Edge switches
        hostNum = (K*pow((K/2),2))      # Hosts in K-ary FatTree

        # Initialize topology
        Topo.__init__( self )

        coreSwitches = []
        aggrSwitches = []
        edgeSwitches = []

        # Core
        for core in range(0, coreSwitchNum):
            coreSwitches.append(self.addSwitch("cs_"+str(core)))
        # Pod
        for pod in range(0, podNum):
        # Aggregate
            for aggr in range(0, aggrSwitchNum/podNum):
                aggrThis = self.addSwitch("as_"+str(pod)+"_"+str(aggr))
                aggrSwitches.append(aggrThis)
                for x in range((K/2)*aggr, (K/2)*(aggr+1)):
#                    self.addLink(aggrSwitches[aggr+(aggrSwitchNum/podNum*pod)], coreSwitches[x])
                    self.addLink(aggrThis, coreSwitches[x])
        # Edge
            for edge in range(0, edgeSwitchNum/podNum):
                edgeThis = self.addSwitch("es_"+str(pod)+"_"+str(edge))
                edgeSwitches.append(edgeThis)
                for x in range((edgeSwitchNum/podNum)*pod, ((edgeSwitchNum/podNum)*(pod+1))):
                    self.addLink(edgeThis, aggrSwitches[x])
        # Host
                for x in range(0, (hostNum/podNum/(edgeSwitchNum/podNum))):
                    self.addLink(edgeThis, self.addHost("h_"+str(pod)+"_"+str(edge)+"_"+str(x)))

topos = { 'fattree': ( lambda: FatTree() ) }
