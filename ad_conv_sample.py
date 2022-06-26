import smbus
import time
import mcp3424

i2c = smbus.SMBus(1)
addr=0x6e

while True:
    config=mcp3424.cfg_read | mcp3424.cfg_ch1 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1
    data=i2c.write_byte(addr, config) # 設定更新 & 変換開始
    time.sleep(1/mcp3424.sps_12bit)
    while True:
        data=i2c.read_i2c_block_data(addr, 0, 3) # 読み出し
        if data[2]>>7 == 0: # 値が更新されているかチェック: 更新時 0
            break
        time.sleep(0.001) # 更新されていなければ少し待って再読み出し

    v=mcp3424.to_volt(data,12)
    print(v)
    time.sleep(0.005)
