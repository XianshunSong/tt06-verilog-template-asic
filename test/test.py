import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from cocotb.binary import BinaryValue

@cocotb.test()
async def test_otp_encryptor(dut):
    
    clock = Clock(dut.clk, 10, units="ns")
    ena = 0
    data = 0
    rnum = 0
    rst_n = 1
    decrypt = 0
    dut.ena.value = ena
    dut.ui_in.value = data
    dut.uio_in.value = (rnum << 1) + decrypt
    dut.rst_n.value = rst_n

    await(ClockCycles(dut.clk, 1))

    rst_n = 0
    dut.rst_n.value = rst_n

    await(ClockCycles(dut.clk, 1))

    rst_n = 1
    dut.rst_n.value = rst_n

    await(ClockCycles(dut.clk, 1))

    data = 0xab
    ena = 1
    decrypt = 0
    dut.ena.value = ena
    dut.ui_in.value = data
    dut.uio_in.value = (rnum << 1) + decrypt

    await(ClockCycles(dut.clk, 1))

    ena = 0
    dut.ena.value = ena
    data = dut.uo_out.value
    rnum = 0
    dut._log.info(f'Encrypted output: {data} ({rnum})')

    await(ClockCycles(dut.clk, 1))

    ena = 1
    decrypt = 1
    dut.ena.value = ena
    dut.ui_in.value = data
    dut.uio_in.value = (rnum << 1) + decrypt

    await(ClockCycles(dut.clk, 1))

    data = dut.uo_out.value
    dut._log.info(f'Decrypted output: {data}')

    for i in range(9):
        ena = 1
        decrypt = 0
        dut.ena.value = ena
        dut.ui_in.value = data
        dut.uio_in.value = (rnum << 1) + decrypt
    
        await(ClockCycles(dut.clk, 1))
    
        ena = 0
        dut.ena.value = ena
        data = dut.uo_out.value
        rnum = (dut.uio_out.value & 0x70) >> 4
        dut._log.info(f'Encrypted output: {data} ({rnum})')
    
        await(ClockCycles(dut.clk, 1))
    
        ena = 1
        decrypt = 1
        dut.ena.value = ena
        dut.ui_in.value = data
        dut.uio_in.value = (rnum << 1) + decrypt
    
        await(ClockCycles(dut.clk, 1))

        data = dut.uo_out.value
        dut._log.info(f'Decrypted output: {data}')
    
    

# @cocotb.test()
# async def test_otp_encryptor(dut):
#     # Start the clock
#     clock = Clock(dut.clk, 10, units="ns")  # Clock period of 10 ns
#     cocotb.start_soon(clock.start())

#     # start alex's changes, ensure that there is a falling edge to trigger reset
#     dut.rst_n.value = 1
#     await ClockCycles(dut.clk, 5)
#     #end alex's changes
    
#     # Reset the device
#     dut.rst_n.value = 0
#     dut.ena.value = 0
#     dut.ui_in.value = 0
#     dut.uio_in.value = 0
#     await ClockCycles(dut.clk, 5)
#     dut.rst_n.value = 1
#     await ClockCycles(dut.clk, 5)

#     # moved code for single test into for loop
#     for num in range(9):
#         # Scenario: Encryption
#         # Set up for encryption
#         dut.ena.value = 1
#         dut.ui_in.value = 0xFF & num  # Example plaintext
    
#         # start alex's changes, comment value and replace
#         # dut.uio_in.value = BinaryValue("00000010")  # Encryption setup
#         dut.uio_in.value = BinaryValue("00000000") 
#         # end alex's changes (this is unnecessary but rnum is only an input for decryption, cannot manually set register to be stored in)
        
#         await ClockCycles(dut.clk, 2)
    
#         # Capture the output from encryption
#         encrypted_value = dut.uo_out.value
#         dut._log.info(f'Encrypted output: {encrypted_value}')
    
#         # start alex's changes, save register number
#         rout = (dut.uio_out.value & 0x70) >> 4
#         dut._log.info(f'Register number: {rout}')
#         # end alex's changes
    
#         # Scenario: Decryption
#         # Assuming the device can decrypt its own output
#         dut.ui_in.value = encrypted_value  # Feed the encrypted value as input
    
#         # start alex's changes - don't drive uio pins 4-7 as they are output pins
#         # instead, drive pins 0-3 with 1 for decrypt for bit 0 and bits 1-3 to match the register num
#         # dut.uio_in.value = BinaryValue("10000010")  # Decryption setup
#         dut.uio_in.value = (0xFF & ((rout << 1) + 1))
#         # end alex's changes
        
#         await ClockCycles(dut.clk, 2)
    
#         # Check if the decrypted output matches the original input (0xFF)
#         decrypted_value = dut.uo_out.value
#         ## assert decrypted_value == (0xFF & num), f"Decryption failed: expected {num}, got {decrypted_value}"
#         dut._log.info(f'Decrypted output: {decrypted_value}')


