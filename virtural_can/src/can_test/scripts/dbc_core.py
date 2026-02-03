import can

class DBCEncoder:
    def __init__(self):
        pass
    def _to_int16(self,val):
        val = val & 0xFFFF
        if val > 0x7FFF:
            val -= 0x10000
        return val
        
    def parse_vehicle_spd(self, can_id, data, dlc):
        """
        解码 0x581底盘反馈 -> 算出车速
        """
        left_speed = 0.0
        right_speed = 0.0

        if can_id == 0x581 and dlc == 8:
            if data[0] == 0x43 and data[1] == 0x21:
                raw_left_unsigned = (data[5] << 8) | data[4]
                raw_left = self.to_int16(raw_left_unsigned)
                left_speed = raw_left / 10

                raw_right_unsigned = (data[7] << 8) | data[6]
                raw_right = self.to_int16(raw_right_unsigned)
                right_speed = (-raw_right) / 10

                return True , left_speed, right_speed
            
        return False, 0.0, 0.0


        
        
    def encode_0x20(self, linear_speed,angular_speed, fault_level):
        """
        编码 0x020 速度控制
        """

        #1、物理量转化为原始值
        linear_speed_raw = int(linear_speed / 0.001)
        angular_speed_raw = int(angular_speed / 0.01)

        linear_speed_raw &= 0xFFFF
        angular_speed_raw &= 0xFFFF

        data = [0] * 8

        data[2] = (linear_speed_raw >> 8) & 0xFF
        data[3] = linear_speed_raw & 0xFF

        data[0] = (angular_speed_raw >> 8) & 0xFF
        data[1] = angular_speed_raw & 0xFF

        data[4] = fault_level & 0xFF

        msg = can.Message(arbitration_id = 0x20,
                          data = data,
                          is_extended_id = False)
        return msg
        
        