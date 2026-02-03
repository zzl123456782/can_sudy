import cantools
import struct

try:
    db = cantools.database.load_file('virtual_can.dbc')
    print("成功打开文件")
except EnvironmentError as e:
    print("打开文件失败")
msg_tx = db.get_message_by_name('ControlCommand')
data_tx = msg_tx.encode(
    {
        'TargetAngularSpeed': 0.5,
        'TargetLinearSpeed' : 1.5,
        'FaultLevel' : 0
    }
)
print(f"发送数据：{data_tx.hex().upper()}")


raw_rx = bytes.fromhex("43 6C 00 00 E8 0 E8 03")
deconded_rx = db.decode_message(0x581, raw_rx)
print("接收解析：", deconded_rx)
