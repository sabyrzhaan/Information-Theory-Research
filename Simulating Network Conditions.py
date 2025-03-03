import ns.applications
import ns.core
import ns.network
import ns.internet
import ns.point_to_point


def simulate_packet_loss_and_jitter(loss_rate=5, jitter_ms=10, simulation_time=10):
    ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
    ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

    # Creating network nodes
    nodes = ns.network.NodeContainer()
    nodes.Create(2)

    # Setting up a point-to-point connection between nodes
    pointToPoint = ns.point_to_point.PointToPointHelper()
    pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
    pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue(f"{jitter_ms}ms"))

    devices = pointToPoint.Install(nodes)

    # Installing the Internet protocol stack on the nodes
    stack = ns.internet.InternetStackHelper()
    stack.Install(nodes)

    # Assigning IP addresses to the nodes
    address = ns.internet.Ipv4AddressHelper()
    address.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
    interfaces = address.Assign(devices)

    # Adding a packet loss error model
    errorModel = ns.network.RateErrorModel()
    errorModel.SetUnit(ns.network.RateErrorModel.ERROR_UNIT_PACKET)
    errorModel.SetRate(loss_rate / 100)  # Converting percentage to fraction
    devices.Get(1).SetAttribute("ReceiveErrorModel", ns.core.PointerValue(errorModel))

    # Setting up a UDP echo server
    echoServer = ns.applications.UdpEchoServerHelper(9)
    serverApp = echoServer.Install(nodes.Get(1))
    serverApp.Start(ns.core.Seconds(1.0))
    serverApp.Stop(ns.core.Seconds(simulation_time))

    # Setting up a UDP echo client
    echoClient = ns.applications.UdpEchoClientHelper(interfaces.GetAddress(1), 9)
    echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(10))
    echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
    echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))
    clientApp = echoClient.Install(nodes.Get(0))
    clientApp.Start(ns.core.Seconds(2.0))
    clientApp.Stop(ns.core.Seconds(simulation_time))

    # Running the simulation
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()


# Running the simulation with 5% packet loss and 10ms jitter
simulate_packet_loss_and_jitter(loss_rate=5, jitter_ms=10, simulation_time=10)
