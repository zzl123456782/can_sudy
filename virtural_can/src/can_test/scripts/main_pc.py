import time
import can
from dbc_core import DBCEncoder

def main():
    print("=== pc控制端启动 ===")
    #初始化can总线
    try:
        bus = can.interface.Bus(channel='vcan0', interface='socketcan')

    except Exception as e:
        print("Can总线初始化失败:", e)
        return
    
    encoder = DBCEncoder()

    try:

        while True:
            #发送部分
            target_v = 1.5
            target_w = 0.5
            fault_level = 0

            #编码并发送
            msg_tx = encoder.encode_0x20(target_v, target_w, fault_level)
            bus.send(msg_tx)
            print("发送 0x20 速度控制:", "线速度:", target_v, "角速度:", target_w, "故障等级:", fault_level)

            #接收部分
            msg_rx = bus.recv(timeout=0.1)

            if msg_rx is not None:
                success, left_speed, right_speed = encoder.parse_vehicle_spd(msg_rx.arbitration_id, 
                                                                            msg_rx.data, 
                                                                            msg_rx.dlc)
                if success:
                    print("收到反馈")
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序终止")
        bus.shutdown()

if __name__ == "__main__":
    main()