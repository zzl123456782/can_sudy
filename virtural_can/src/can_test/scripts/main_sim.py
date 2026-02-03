import can
import time
from dbc_core import DBCEncoder

def to_bytes_little_endian(val):
    val = val & 0xFFFF
    low = val & 0xFF
    high = (val >> 8) & 0xFF
    return low, high

def main():
    print("===底盘模拟器启动===")
    try:
        bus = can.interface.Bus(channel='vcan0', interface='socketcan')
    except Exception as e:
        print("Can总线初始化失败:", e)
        return
    
    try:
        while True:
            msg = bus.recv()
            if msg is None:
                continue

            if msg.arbitration_id == 0x20:
                # 打印收到的原始数据
                hex_str = ' '.join([f'{b:02X}' for b in msg.data])
                print(f"[SIM] 收到指令 0x20: {hex_str}")

                #构造回复0x581
                left_raw = 1205
                right_raw = 1205

                reply_data = [0]*8

                reply_data[0] = 0x43
                reply_data[1] = 0x6C

                #左轮
                reply_data[4], reply_data[5] = to_bytes_little_endian(left_raw)
                #右轮
                reply_data[6], reply_data[7] = to_bytes_little_endian(-right_raw)

                reply_msg = can.Message(arbitration_id=0x581,
                                        data=reply_data,
                                        is_extended_id=False)
                
                bus.send(reply_msg)
                print(f"[SIM] 发送反馈 0x581: {' '.join([f'{b:02X}' for b in reply_data])}")
    except  KeyboardInterrupt:
        print("程序终止")
        bus.shutdown()

if __name__ == "__main__":
    main()            