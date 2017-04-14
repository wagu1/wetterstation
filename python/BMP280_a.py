#coding: utf-8
import Adafruit_GPIO.I2C as I2C
import time
##i2c = I2C
##device=i2c.get_i2c_device(0x77) # address of BMP
   
class BMP280():
    
    # initialize BMP085 sensor
    def __init__(self, i2c, address):
        self.i2c      = i2c
        self.address  = address

        self.device=i2c.get_i2c_device(0x77) # address of BMP

        self.temp     = 0
        self.pressure = 0
        self.altitude = 0

        self.POWER_MODE = 3 # normal mode
        # this value is necessary to calculate the correct height above sealevel
        # its also included in airport wheather information ATIS named as QNH
        # unit is hPa
        self.QNH = 1020
        self.OSRS_T = 5  # 20 Bit temperature resolution
        self.OSRS_P = 5  # 20 Bit ultra high resolution pressure resolution
        self.FILTER = 4  # Filter-settings
        self.T_SB   = 4  # 100 500ms standby settings
        self.CONFIG = (self.T_SB <<5) + (self.FILTER <<2) # combine bits for config
        self.CTRL_MEAS = (self.OSRS_T <<5) + (self.OSRS_P <<2) + self.POWER_MODE # combine bits for ctrl_meas

        # Read the calibration data
        # self.readCalibrationData()

        self.BMP280_REGISTER_DIG_T1 = 0x88
        self.BMP280_REGISTER_DIG_T2 = 0x8A
        self.BMP280_REGISTER_DIG_T3 = 0x8C
        self.BMP280_REGISTER_DIG_P1 = 0x8E
        self.BMP280_REGISTER_DIG_P2 = 0x90
        self.BMP280_REGISTER_DIG_P3 = 0x92
        self.BMP280_REGISTER_DIG_P4 = 0x94
        self.BMP280_REGISTER_DIG_P5 = 0x96
        self.BMP280_REGISTER_DIG_P6 = 0x98
        self.BMP280_REGISTER_DIG_P7 = 0x9A
        self.BMP280_REGISTER_DIG_P8 = 0x9C
        self.BMP280_REGISTER_DIG_P9 = 0x9E
        self.BMP280_REGISTER_CHIPID = 0xD0
        self.BMP280_REGISTER_VERSION = 0xD1
        self.BMP280_REGISTER_SOFTRESET = 0xE0
        self.BMP280_REGISTER_CONTROL = 0xF4
        self.BMP280_REGISTER_CONFIG  = 0xF5
        self.BMP280_REGISTER_STATUS = 0xF3
        self.BMP280_REGISTER_TEMPDATA_MSB = 0xFA
        self.BMP280_REGISTER_TEMPDATA_LSB = 0xFB
        self.BMP280_REGISTER_TEMPDATA_XLSB = 0xFC
        self.BMP280_REGISTER_PRESSDATA_MSB = 0xF7
        self.BMP280_REGISTER_PRESSDATA_LSB = 0xF8
        self.BMP280_REGISTER_PRESSDATA_XLSB = 0xF9
        self.calibrate()

    def calibrate(self):
        if (self.device.readS8(self.BMP280_REGISTER_CHIPID) == 0x58): # check sensor id 0x58=BMP280
            self.device.write8(self.BMP280_REGISTER_SOFTRESET,0xB6) # reset sensor
            time.sleep(0.2) # little break
            self.device.write8(self.BMP280_REGISTER_CONTROL, self.CTRL_MEAS) #
            time.sleep(0.2) # little break
            self.device.write8(self.BMP280_REGISTER_CONFIG, self.CONFIG)  #
            time.sleep(0.2)
            # register_control = device.readU8(BMP280_REGISTER_CONTROL) # check the controll register again
            # register_config = device.readU8(BMP280_REGISTER_CONFIG)# check the controll register again
            # print("config:",register_config)
            # print("control:",register_control)

            self.dig_T1 = self.device.readU16LE(self.BMP280_REGISTER_DIG_T1) # read correction settings
            self.dig_T2 = self.device.readS16LE(self.BMP280_REGISTER_DIG_T2)
            self.dig_T3 = self.device.readS16LE(self.BMP280_REGISTER_DIG_T3)
            self.dig_P1 = self.device.readU16LE(self.BMP280_REGISTER_DIG_P1)
            self.dig_P2 = self.device.readS16LE(self.BMP280_REGISTER_DIG_P2)
            self.dig_P3 = self.device.readS16LE(self.BMP280_REGISTER_DIG_P3)
            self.dig_P4 = self.device.readS16LE(self.BMP280_REGISTER_DIG_P4)
            self.dig_P5 = self.device.readS16LE(self.BMP280_REGISTER_DIG_P5)
            self.dig_P6 = self.device.readS16LE(self.BMP280_REGISTER_DIG_P6)
            self.dig_P7 = self.device.readS16LE(self.BMP280_REGISTER_DIG_P7)
            self.dig_P8 = self.device.readS16LE(self.BMP280_REGISTER_DIG_P8)
            self.dig_P9 = self.device.readS16LE(self.BMP280_REGISTER_DIG_P9)

            #print("dig_T1:",dig_T1," dig_T2:",dig_T2," dig_T3:",dig_T3)
            #print("dig_P1:",dig_P1," dig_P2:",dig_P2," dig_P3:",dig_P3)
            #print(" dig_P4:",dig_P4," dig_P5:",dig_P5," dig_P6:",dig_P6)
            #print(" dig_P7:",dig_P7," dig_P8:",dig_P8," dig_P9:",dig_P9)

    def readValues(self):
        raw_temp_msb   = self.device.readU8(self.BMP280_REGISTER_TEMPDATA_MSB) # read raw temperature msb
        raw_temp_lsb   = self.device.readU8(self.BMP280_REGISTER_TEMPDATA_LSB) # read raw temperature lsb
        raw_temp_xlsb  = self.device.readU8(self.BMP280_REGISTER_TEMPDATA_XLSB) # read raw temperature xlsb
        raw_press_msb  = self.device.readU8(self.BMP280_REGISTER_PRESSDATA_MSB) # read raw pressure msb
        raw_press_lsb  = self.device.readU8(self.BMP280_REGISTER_PRESSDATA_LSB) # read raw pressure lsb
        raw_press_xlsb = self.device.readU8(self.BMP280_REGISTER_PRESSDATA_XLSB) # read raw pressure xlsb

        raw_temp=(raw_temp_msb <<12)+(raw_temp_lsb<<4)+(raw_temp_xlsb>>4) # combine 3 bytes  msb 12 bits left, lsb 4 bits left, xlsb 4 bits right
        raw_press=(raw_press_msb <<12)+(raw_press_lsb <<4)+(raw_press_xlsb >>4) # combine 3 bytes  msb 12 bits left, lsb 4 bits left, xlsb 4 bits right
        # print("raw_press_msb:",raw_press_msb," raw_press_lsb:",raw_press_xlsb," raw_press_xlsb:",raw_press_xlsb)
        # print("raw_temp_msb:",raw_temp_msb,"  raw_temp_lsb:",raw_temp_lsb," raw_temp_xlsb:",raw_temp_xlsb)
        # print("raw_press",raw_press)

        # the following values are from the calculation example in the datasheet
        # this values can be used to check the calculation formulas
        # dig_T1=27504
        # dig_T2=26435
        # dig_T3=-1000
        # dig_P1=36477
        # dig_P2=-10685
        # dig_P3=3024
        # dig_P4=2855
        # dig_P5=140
        # dig_P6=-7
        # dig_P7=15500
        # dig_P8=-14600
        # dig_P9=6000
        # t_fine=128422.2869948
        # raw_temp=519888
        # raw_press=415148

        # Temperaturbestimmung
        var1=(raw_temp/16384.0-self.dig_T1/1024.0)*self.dig_T2 # formula for temperature from datasheet
        var2=(raw_temp/131072.0-self.dig_T1/8192.0)*(raw_temp/131072.0-self.dig_T1/8192.0)*self.dig_T3 # formula for temperature from datasheet
        self.temp=(var1+var2)/5120.0 # formula for temperature from datasheet
        
        # Druckbestimmung
        t_fine=(var1+var2) # need for pressure calculation
        var1=t_fine/2.0-64000.0 # formula for pressure from datasheet
        var2=var1*var1*self.dig_P6/32768.0 # formula for pressure from datasheet
        var2=var2+var1*self.dig_P5*2 # formula for pressure from datasheet
        var2=var2/4.0+self.dig_P4*65536.0 # formula for pressure from datasheet
        var1=(self.dig_P3*var1*var1/524288.0+self.dig_P2*var1)/524288.0 # formula for pressure from datasheet
        var1=(1.0+var1/32768.0)*self.dig_P1 # formula for pressure from datasheet
        self.press=1048576.0-raw_press # formula for pressure from datasheet
        self.press=(self.press-var2/4096.0)*6250.0/var1 # formula for pressure from datasheet
        var1=self.dig_P9*self.press*self.press/2147483648.0 # formula for pressure from datasheet
        var2=self.press*self.dig_P8/32768.0 # formula for pressure from datasheet
        self.press=self.press+(var1+var2+self.dig_P7)/16.0 # formula for pressure from datasheet
        self.pressure = self.press/100.0
        # Höhenbestimmung
        self.altitude= 44330.0 * (1.0 - pow(self.press / (self.QNH*100), (1.0/5.255))) # formula for altitude from airpressure
        #print("temperature:{:.2f}".format(temp)+" C  pressure:{:.2f}".format(press/100)+" hPa   altitude:{:.2f}".format(altitude)+" m")

    def getTemperature(self):
        self.readValues()
        return self.temp

    def getPressure(self):
        self.readValues()
        return self.pressure

    def getAltitude(self):
        self.readValues()
        return self.altitude

# Test 
# -------------------------------------------------------
#bmp280 = BMP280(I2C,"")
#print ("T :{:.2f} C".format(bmp280.getTemperature()))
#print ("p :{:.2f} hPa".format(bmp280.getPressure()))
#print ("h :{:.2f} m".format(bmp280.getAltitude()))
# -------------------------------------------------------
