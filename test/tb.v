`default_nettype none `timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();
  // Dump the signals to a VCD file. You can view it with gtkwave.
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

  // Replace tt_um_example with your module name:
  tt_um_opt_encryptor user_project (

      // Include power ports for the Gate Level test:
`ifdef GL_TEST
      .VPWR(1'b1),
      .VGND(1'b0),
`endif

      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // enable - goes high when design is selected
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // not reset
  );


    //clock
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // Generate a clock with a period of 10 ns
    end
   
initial begin
        // Initialize all signals
        rst_n = 0; ena = 0; ui_in = 0; uio_in = 0;
        #10;
        rst_n = 1;  // Release reset

        // encryption
        ena = 1; ui_in = 8'hFF; uio_in = 8'b00000010; // Set up encryption
        #20;

        //decryption
        ui_in = 8'h00; uio_in = 8'b10000010; // Set up decryption

        #100;
        $finish; // End simulation after 100 ns
end

initial $monitor($time,,"[%b]\t%b\tq=%b",clk,ui_in[0],uo_out);

always #2 clk=~clk;
   
endmodule


