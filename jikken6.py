import wiringpi as pi, time

count = 0 #タイヤの回転数を数える

a = [19,13,6,5]
OUTPUT_PIN1_1 = a[0]
OUTPUT_PIN1_2 = a[1]
OUTPUT_PIN1_3 = a[2]
OUTPUT_PIN1_4 = a[3]

b = [22,27,17,4]
OUTPUT_PIN2_1 = b[0]
OUTPUT_PIN2_2 = b[1]
OUTPUT_PIN2_3 = b[2]
OUTPUT_PIN2_4 = b[3]

TIME_SLEEP = 0.002
pi.wiringPiSetupGpio()
pi.pinMode(25, pi.INPUT) 
pi.pullUpDnControl(25,pi.PUD_UP)
pi.pinMode(21, pi.INPUT)
pi.pullUpDnControl(21,pi.PUD_UP)
pi.pinMode(26, pi.INPUT)
pi.pullUpDnControl(26,pi.PUD_UP)
pi.pinMode(12, pi.INPUT)
pi.pullUpDnControl(12,pi.PUD_UP)
pi.pinMode(16, pi.INPUT)
pi.pullUpDnControl(16,pi.PUD_UP)
pi.pinMode(OUTPUT_PIN1_1,pi.OUTPUT)
pi.pinMode(OUTPUT_PIN1_2,pi.OUTPUT)
pi.pinMode(OUTPUT_PIN1_3,pi.OUTPUT)
pi.pinMode(OUTPUT_PIN1_4,pi.OUTPUT)

pi.pinMode(OUTPUT_PIN2_1,pi.OUTPUT)
pi.pinMode(OUTPUT_PIN2_2,pi.OUTPUT)
pi.pinMode(OUTPUT_PIN2_3,pi.OUTPUT)
pi.pinMode(OUTPUT_PIN2_4,pi.OUTPUT)

import smbus
import time
import mcp3424

i2c = smbus.SMBus(1)
addr=0x68
while True:
    
    #400回に1回赤外センサーから値をもらう
    if(count %400  == 0): 
        print("a")
        while True:##stop
            config=mcp3424.cfg_read | mcp3424.cfg_ch4 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1
            data1=i2c.write_byte(addr, config) # 設定更新 & 変換開始
            time.sleep(1/mcp3424.sps_12bit)
            
            while True:
                data3=i2c.read_i2c_block_data(addr, 0, 3) # 読み出し
                if data3[2]>>7 == 0: # 値が更新されているかチェック: 更新時 0
                    break
                time.sleep(0.001) # 更新されていなければ少し待って再読み出し
            v=mcp3424.to_volt(data3,12)  

            config=mcp3424.cfg_read | mcp3424.cfg_ch1 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1
            data2=i2c.write_byte(addr, config) # 設定更新 & 変換開始
            time.sleep(1/mcp3424.sps_12bit)
            
            while True:
                data2=i2c.read_i2c_block_data(addr, 0, 3) # 読み出し
                if data2[2]>>7 == 0: # 値が更新されているかチェック: 更新時 0
                    break
                time.sleep(0.001) # 更新されていなければ少し待って再読み出し

            w=mcp3424.to_volt(data2,12)
            
            
            config=mcp3424.cfg_read | mcp3424.cfg_ch2 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1
            data3=i2c.write_byte(addr, config) # 設定更新 & 変換開始
            time.sleep(1/mcp3424.sps_12bit)
            while True:
                data1=i2c.read_i2c_block_data(addr, 0, 3) # 読み出し
                if data1[2]>>7 == 0: # 値が更新されているかチェック: 更新時 0
                    break
                time.sleep(0.001) # 更新されていなければ少し待って再読み出し

            x=mcp3424.to_volt(data1,12)
            print(v,w,x)
            count = 1
            break
                    
    ##左に曲がる
    if(x < 0.68):
        
        time.sleep(0.5)
        while True:
            pi.digitalWrite(a[0],pi.HIGH)
            pi.digitalWrite(a[1],pi.LOW)
            pi.digitalWrite(a[2],pi.LOW)
            pi.digitalWrite(a[3],pi.LOW)
            
            pi.digitalWrite(b[0],pi.LOW)
            pi.digitalWrite(b[1],pi.LOW)
            pi.digitalWrite(b[2],pi.LOW)
            pi.digitalWrite(b[3],pi.HIGH)
            time.sleep(TIME_SLEEP)
            
            pi.digitalWrite(a[0],pi.LOW)
            pi.digitalWrite(a[1],pi.HIGH)
            pi.digitalWrite(a[2],pi.LOW)
            pi.digitalWrite(a[3],pi.LOW)
            
            pi.digitalWrite(b[0],pi.LOW)
            pi.digitalWrite(b[1],pi.LOW)
            pi.digitalWrite(b[2],pi.HIGH)
            pi.digitalWrite(b[3],pi.LOW)
            
            time.sleep(TIME_SLEEP)
            pi.digitalWrite(a[0],pi.LOW)
            pi.digitalWrite(a[1],pi.LOW)
            pi.digitalWrite(a[2],pi.HIGH)
            pi.digitalWrite(a[3],pi.LOW)
            
            pi.digitalWrite(b[0],pi.LOW)
            pi.digitalWrite(b[1],pi.HIGH)
            pi.digitalWrite(b[2],pi.LOW)
            pi.digitalWrite(b[3],pi.LOW)
            time.sleep(TIME_SLEEP)
            
            pi.digitalWrite(a[0],pi.LOW)
            pi.digitalWrite(a[1],pi.LOW)
            pi.digitalWrite(a[2],pi.LOW)
            pi.digitalWrite(a[3],pi.HIGH)
            
            pi.digitalWrite(b[0],pi.HIGH)
            pi.digitalWrite(b[1],pi.LOW)
            pi.digitalWrite(b[2],pi.LOW)
            pi.digitalWrite(b[3],pi.LOW)
            
            time.sleep(TIME_SLEEP)
            print(v,w,x)
            count += 1

            #10回に1回赤外センサから値を受け取り、左に障害物があれば、左回転をやめる
            if(count % 10 == 0):
                config=mcp3424.cfg_read | mcp3424.cfg_ch4 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1
                data1=i2c.write_byte(addr, config) # 設定更新 & 変換開始
                time.sleep(1/mcp3424.sps_12bit)
                
                while True:
                    data3=i2c.read_i2c_block_data(addr, 0, 3) # 読み出し
                    if data3[2]>>7 == 0: # 値が更新されているかチェック: 更新時 0
                        break
                    time.sleep(0.001) # 更新されていなければ少し待って再読み出し
                v=mcp3424.to_volt(data3,12)  
                
                config=mcp3424.cfg_read | mcp3424.cfg_ch2 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1
                data3=i2c.write_byte(addr, config) # 設定更新 & 変換開始
                time.sleep(1/mcp3424.sps_12bit)
                while True:
                    data1=i2c.read_i2c_block_data(addr, 0, 3) # 読み出し
                    if data1[2]>>7 == 0: # 値が更新されているかチェック: 更新時 0
                        break
                    time.sleep(0.001) # 更新されていなければ少し待って再読み出し

                x=mcp3424.to_volt(data1,12)
                print("left")
                print(v,w,x)
                count = 0
                
                
                if(x > 0.8):
                    break

    ##右に曲がる
            
    if(v < 0.5 and x > 0.8):
        while True:
            pi.digitalWrite(b[0],pi.HIGH)
            pi.digitalWrite(b[1],pi.LOW)
            pi.digitalWrite(b[2],pi.LOW)
            pi.digitalWrite(b[3],pi.LOW)
            
            pi.digitalWrite(a[0],pi.LOW)
            pi.digitalWrite(a[1],pi.LOW)
            pi.digitalWrite(a[2],pi.LOW)
            pi.digitalWrite(a[3],pi.HIGH)
            
            time.sleep(TIME_SLEEP)
            
            pi.digitalWrite(b[0],pi.LOW)
            pi.digitalWrite(b[1],pi.HIGH)
            pi.digitalWrite(b[2],pi.LOW)
            pi.digitalWrite(b[3],pi.LOW)
            
            pi.digitalWrite(a[0],pi.LOW)
            pi.digitalWrite(a[1],pi.LOW)
            pi.digitalWrite(a[2],pi.HIGH)
            pi.digitalWrite(a[3],pi.LOW)
            time.sleep(TIME_SLEEP)
            pi.digitalWrite(b[0],pi.LOW)
            pi.digitalWrite(b[1],pi.LOW)
            pi.digitalWrite(b[2],pi.HIGH)
            pi.digitalWrite(b[3],pi.LOW)
            
            pi.digitalWrite(a[0],pi.LOW)
            pi.digitalWrite(a[1],pi.HIGH)
            pi.digitalWrite(a[2],pi.LOW)
            pi.digitalWrite(a[3],pi.LOW)
            time.sleep(TIME_SLEEP)
            
            pi.digitalWrite(b[0],pi.LOW)
            pi.digitalWrite(b[1],pi.LOW)
            pi.digitalWrite(b[2],pi.LOW)
            pi.digitalWrite(b[3],pi.HIGH)
            
            pi.digitalWrite(a[0],pi.HIGH)
            pi.digitalWrite(a[1],pi.LOW)
            pi.digitalWrite(a[2],pi.LOW)
            pi.digitalWrite(a[3],pi.LOW)
            
            time.sleep(TIME_SLEEP)
            count += 1
            
            #100回に1回赤外センサから値をもらい、右側に障害物があると、右回転をやめる
            if(count % 100 == 0):
                config=mcp3424.cfg_read | mcp3424.cfg_ch4 | mcp3424.cfg_once | mcp3424.cfg_12bit | mcp3424.cfg_PGAx1
                data1=i2c.write_byte(addr, config) # 設定更新 & 変換開始
                time.sleep(1/mcp3424.sps_12bit)
                
                while True:
                    data3=i2c.read_i2c_block_data(addr, 0, 3) # 読み出し
                    if data3[2]>>7 == 0: # 値が更新されているかチェック: 更新時 0
                        break
                    time.sleep(0.001) # 更新されていなければ少し待って再読み出し

                v=mcp3424.to_volt(data3,12)
                count = 0
                print(v,w,x)
                print("right")
                if(v >0.8):
                    break
    #前進
    if(v > 0):
        pi.digitalWrite(a[0],pi.HIGH)
        pi.digitalWrite(a[1],pi.LOW)
        pi.digitalWrite(a[2],pi.LOW)
        pi.digitalWrite(a[3],pi.LOW)
        
        pi.digitalWrite(b[0],pi.HIGH)
        pi.digitalWrite(b[1],pi.LOW)
        pi.digitalWrite(b[2],pi.LOW)
        pi.digitalWrite(b[3],pi.LOW)

        time.sleep(TIME_SLEEP)
        
        pi.digitalWrite(a[0],pi.LOW)
        pi.digitalWrite(a[1],pi.HIGH)
        pi.digitalWrite(a[2],pi.LOW)
        pi.digitalWrite(a[3],pi.LOW)
        
        pi.digitalWrite(b[0],pi.LOW)
        pi.digitalWrite(b[1],pi.HIGH)
        pi.digitalWrite(b[2],pi.LOW)
        pi.digitalWrite(b[3],pi.LOW)
        
        time.sleep(TIME_SLEEP)
        
        pi.digitalWrite(a[0],pi.LOW)
        pi.digitalWrite(a[1],pi.LOW)
        pi.digitalWrite(a[2],pi.HIGH)
        pi.digitalWrite(a[3],pi.LOW)
        
        pi.digitalWrite(b[0],pi.LOW)
        pi.digitalWrite(b[1],pi.LOW)
        pi.digitalWrite(b[2],pi.HIGH)
        pi.digitalWrite(b[3],pi.LOW)
        

        time.sleep(TIME_SLEEP)
        
        pi.digitalWrite(a[0],pi.LOW)
        pi.digitalWrite(a[1],pi.LOW)
        pi.digitalWrite(a[2],pi.LOW)
        pi.digitalWrite(a[3],pi.HIGH)
        
        pi.digitalWrite(b[0],pi.LOW)
        pi.digitalWrite(b[1],pi.LOW)
        pi.digitalWrite(b[2],pi.LOW)
        pi.digitalWrite(b[3],pi.HIGH)
        

        time.sleep(TIME_SLEEP)
        count += 1
        print(count)
        print("switch on")
        print(v,w,x)
