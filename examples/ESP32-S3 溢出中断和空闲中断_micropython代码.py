==============同时FIFO满中断和空闲中断示例=============================
from machine import UART
import time

class UartPacketReceiver:
    def __init__(self, uart_num=1, baudrate=115200, rx=39, tx=40):
        self.uart = UART(uart_num, baudrate, tx=tx, rx=rx)
        self.buffer = bytearray()
        
        # 设置中断触发器
        self.uart.irq(trigger=UART.IRQ_RXFIFO_FULL | UART.IRQ_RXIDLE, 
                     handler=self._uart_handler)
        print("UART初始化完成")
    
    def _uart_handler(self, uart):
        if not uart.any():
            return
            
        flags = uart.irq().flags()
        print("中断标志:", flags)  # 调试信息
        
        # FIFO 满中断或空闲中断都读取数据
        while uart.any():
            data = uart.read()
            if data:
                self.buffer.extend(data)
                print("接收到数据，当前buffer长度:", len(self.buffer))  # 调试信息
        
        # 在空闲中断时处理数据
        if flags & UART.IRQ_RXIDLE:
            if len(self.buffer) > 0:
                self._process_packet(bytes(self.buffer))
                self.buffer = bytearray()
    
    def _process_packet(self, packet):
        """处理完整的数据包"""
        print("收到完整数据包:", packet)
        
    def deinit(self):
        self.uart.irq(handler=None)
        self.uart.deinit()

# 使用示例
if __name__ == '__main__':
    receiver = UartPacketReceiver(uart_num=1, baudrate=115200)
    print("开始接收数据...")
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        receiver.deinit()
========================================================

======================只使用用空闲中断示例======================
from machine import UART
import time

class UartPacketReceiver:
    def __init__(self, uart_num=1, baudrate=115200, rx=39, tx=40):
        self.uart = UART(uart_num, baudrate, tx=tx, rx=rx)
        self.buffer = bytearray()
        
        # 只设置空闲中断
        self.uart.irq(trigger=UART.IRQ_RXIDLE, 
                     handler=self._uart_handler)
        print("UART初始化完成")
    
    def _uart_handler(self, uart):
        if not uart.any():
            return
            
        # 读取所有可用数据
        while uart.any():
            data = uart.read()
            if data:
                self.buffer.extend(data)
                print("接收到数据，当前buffer长度:", len(self.buffer))
        
        # 有数据就处理
        if len(self.buffer) > 0:
            self._process_packet(bytes(self.buffer))
            self.buffer = bytearray()
    
    def _process_packet(self, packet):
        """处理完整的数据包"""
        print("收到完整数据包:", packet)
        
    def deinit(self):
        self.uart.irq(handler=None)
        self.uart.deinit()

# 使用示例
if __name__ == '__main__':
    receiver = UartPacketReceiver(uart_num=1, baudrate=115200)
    print("开始接收数据...")
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        receiver.deinit()
=========================================================