# Vin_pc_simu_tool
VIN码转换工具

工具说明：
此工具用于方便转换生成VIN、VIN的十六进制格式、该VIN的OBD回复命令。  

### 打包命令  
`pyinstaller -F -w --icon=icon.ico pyqt_test2.py`  

### 使用方法：  
##### 一、已知VIN码，目的为获取VIN的十六进制格式 或 该VIN的OBD回复命令:   
    1、在“vin”栏输入VIN码  
       格式为：  
             LNBMDBAF7GU197436  
    2、点击“Start”   
    
##### 二、已知VIN码的十六进制格式，目的为获取VIN码 或 该VIN的OBD回复命令:   
        1、在“hex”栏输入VIN码的十六进制格式   
       格式为：   
             4C 4E 42 4D 44 42 41 46 37 47 55 31 39 37 34 33 36   
             （注意每个字节之间有一个空格）   
       2、点击“Start”  

##### 三、已知该VIN的OBD回复命令，目的为获取VIN码 或 VIN的十六进制格式:   
    1、在“obd_cmd”栏输入该VIN的OBD回复命令  
       格式为：  
             10 14 5A 90 00 4C 4E 42    
             21 4D 44 42 41 46 37 47   
             22 55 31 39 37 34 33 36  
             （标准OBD CAN型回复命令，其中BYTE04到BYTE20为VIN码的十六进制）   
             或是   
             87 F1 11 49 02 01 00 00 00 4C D1   
             87 F1 11 49 02 02 4E 42 4D 44 D2   
             87 F1 11 49 02 03 42 41 46 37 D3   
             87 F1 11 49 02 04 47 55 31 39 D4  
             87 F1 11 49 02 05 37 34 33 36 D5   
             （标准OBD 串型回复命令，其中第1帧的BYTE09及之后4帧命令的BYTE06-09为VIN码的十六进制）   
    2、点击“Start”   

##### 四、清空所有数据：  
    1、点击“Clear”   

##### 五、获取帮助信息  
    在“vin”栏输入HELP，点击“Start”  
![image](https://user-images.githubusercontent.com/49632322/174200759-b13ce7e3-c757-4fc7-8dd6-ee8e6f9918e8.png)
