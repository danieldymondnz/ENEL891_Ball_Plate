module pwmClkGen (input clk50MHz,
						output reg pwmClk);
						
	reg [8:0] count;
		
		always @ (posedge clk50MHz) begin
			
			// Servo operates at 333Hz
			// For 0.5*/tick, requires 360 ticks per frame
			// PSK = 417
			if (count > 416) begin
				count = 9'd0;
				pwmClk = !pwmClk;
			end
			else
				count = count + 9'd1;
		end
		
endmodule 