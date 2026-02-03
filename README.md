# can_sudy
2026.02.03

  基于虚拟的Vcan0进行的数据接收程序的编写，其中 & 0xFF表示只取数据的低八位数据，对数据进行筛选 
  
  其中，can总线的初始化、can总线发布数据、接收数据分别为:
  
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')

    bus.send(msg_tx) 其中msg_tx需要进行数据的填充

    msg_rx = bus.recv(timeout=0.1) 表示阻塞0.1s接收一帧数据

  启动虚拟can接口的命令

    # 1. 加载内核模块
    sudo modprobe vcan
    
    # 2. 添加一个名为 vcan0 的接口
    sudo ip link add dev vcan0 type vcan
    
    # 3. 启用接口
    sudo ip link set up vcan0
    
    
  
